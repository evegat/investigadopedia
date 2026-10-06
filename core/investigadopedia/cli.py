"""
CLI unificado de Investigadopedia.
Permite ejecutar pipelines de investigación desde la línea de comandos o desde agentes.
Zero dependencies (Python 3.8+ estándar).
"""

import argparse
import json
import sys
from pathlib import Path

from .harvest.redalyc import search_redalyc
from .harvest.scielo import search_scielo_by_issns
from .harvest.openalex import iterate_openalex_works
from .screen.dedup import merge_jsonl_files
from .screen.partition import partition_corpus
from .screen.jev import JevClassifier
from .epistemic.tripartition import audit_epistemic_text
from .report.prisma import generate_prisma_markdown
from .match.scramble import scramble_text
from .match.estimator import JournalEstimator, generate_match_report


def handle_harvest(args):
    print(f"[*] Iniciando cosecha con motor '{args.engine}' para query: '{args.query}'...")
    count = 0
    if args.engine == "redalyc":
        for _ in search_redalyc(args.query, max_records=args.max, out_path=args.out):
            count += 1
    elif args.engine == "scielo":
        for _ in search_scielo_by_issns(args.query, max_records=args.max, out_path=args.out):
            count += 1
    elif args.engine == "openalex":
        from .harvest.openalex import flatten_work, fetch_openalex_page
        out_file = Path(args.out)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as f:
            for item in iterate_openalex_works(filter_expr="type:article", search_query=args.query, max_records=args.max):
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                count += 1
    else:
        print(f"[!] Motor desconocido: {args.engine}", file=sys.stderr)
        sys.exit(1)

    print(f"[+] Cosecha finalizada: {count} registros guardados en {args.out}")


def handle_merge(args):
    print(f"[*] Fusionando y deduplicando {len(args.inputs)} archivos...")
    total = merge_jsonl_files(args.inputs, args.out)
    print(f"[+] Deduplicación completada: {total} registros únicos en {args.out}")


def handle_partition(args):
    print(f"[*] Particionando corpus de {args.input}...")
    report = partition_corpus(args.input, args.out_dir)
    print(f"[+] Partición completada:")
    print(f"    - Académico (revisado por pares): {report['academic_peer_reviewed']}")
    print(f"    - Literatura gris: {report['grey_literature']}")
    print(f"    - Descartados: {report['dropped_invalid']}")
    print(f"    - Reporte emitido en: {args.out_dir}/provenance_report.json")


def handle_screen(args):
    print(f"[*] Cribando corpus {args.input} con criterios: '{args.criteria}'...")
    classifier = JevClassifier()
    in_path = Path(args.input)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    included = 0
    total = 0
    with open(in_path, "r", encoding="utf-8") as f_in, open(out_path, "w", encoding="utf-8") as f_out:
        for line in f_in:
            if not line.strip():
                continue
            rec = json.loads(line)
            total += 1
            eval_res = classifier.screen_paper(rec.get("title", ""), rec.get("abstract"), args.criteria)
            rec["screening"] = eval_res
            if eval_res.get("include"):
                included += 1
            f_out.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"[+] Cribado completado: {included}/{total} registros incluidos ({round(included/max(1, total)*100, 1)}%)")


def handle_audit_text(args):
    path = Path(args.file)
    if not path.exists():
        print(f"[!] Archivo no encontrado: {args.file}", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    report = audit_epistemic_text(text)
    print(f"=== Auditoría Epistemológica: {args.file} ===")
    print(f"Estado: {report['status']}")
    print(f"Cumplimiento: {report['compliance_score']}%")
    print(f"Conteos rotulados: {report['labeled_counts']}")
    if report["findings"]:
        print("\nHallazgos que requieren revisión:")
        for finding in report["findings"]:
            print(f"- [Párrafo {finding['paragraph_index']}]: {finding['issue']}")
            print(f"  Extracto: \"{finding['excerpt']}\"")


def handle_review_manuscript(args):
    from .epistemic.peer_review import evaluate_manuscript_peer_review, generate_peer_review_report
    path = Path(args.file)
    if not path.exists():
        print(f"[!] Archivo no encontrado: {args.file}", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    eval_res = evaluate_manuscript_peer_review(text)
    report_md = generate_peer_review_report(eval_res, path.name)

    print(f"=== Arbitraje Editorial Simulado: {path.name} ===")
    print(f"Dictamen: {eval_res['editorial_recommendation']}")
    print(f"Índice de Madurez: {eval_res['overall_readiness_score']}%")
    print(f"Extensión: {eval_res['total_words']} palabras")

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report_md, encoding="utf-8")
        print(f"[+] Informe completo guardado en: {args.out}")


def handle_match(args):
    raw_text = ""
    if args.text:
        raw_text = args.text
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"[!] Archivo no encontrado: {args.file}", file=sys.stderr)
            sys.exit(1)
        raw_text = file_path.read_text(encoding="utf-8")
    else:
        print("[!] Debe proporcionar --text o --file con el abstract del trabajo.", file=sys.stderr)
        sys.exit(1)

    eval_text = scramble_text(raw_text) if args.scramble else raw_text
    estimator = JournalEstimator()
    matches = estimator.match_journals(text=eval_text, top_n=args.top, diamond_only=args.diamond_only)

    print(f"=== Recomendación de Revistas JANE Latam (Ciencias Sociales) ===")
    print(f"Filtro: Acceso Abierto Diamante (Sin APC: {args.diamond_only})")
    print(f"Modo privacidad (Scramble): {args.scramble}")
    print(f"Revistas encontradas: {len(matches)}\n")

    for idx, m in enumerate(matches, start=1):
        j = m["journal"]
        badges = "/".join(k.upper() for k in j.indexing)
        print(f"{idx}. {j.title} ({j.country}) - Afinidad: {m['confidence_pct']}% [{badges}] [ISSN: {j.issn}]")
        print(f"   Términos: {', '.join(m['matched_terms'])}")

    author_matches = None
    if getattr(args, "live_authors", False):
        print("\n[*] Consultando OpenAlex para extraer revisores/autores recientes en estas revistas...")
        target_issns = [m["journal"].issn for m in matches]
        author_matches = estimator.fetch_live_reviewers(text=eval_text, target_issns=target_issns, top_n=args.top)
        if author_matches:
            print(f"[+] Autores/Revisores potenciales identificados ({len(author_matches)}):")
            for a in author_matches:
                country_str = f"({a['country']})" if a.get('country') else ""
                journals_str = ", ".join(a.get("journals", []))
                print(f"   - {a['name']} {country_str}: {a['occurrences']} artículos afines [{journals_str}]")
        else:
            print("[-] No se pudieron extraer autores en vivo (modo offline o sin publicaciones recientes coincidentes).")

    report_md = generate_match_report(text_query=raw_text, journal_matches=matches, author_matches=author_matches)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report_md, encoding="utf-8")
        print(f"\n[+] Reporte completo guardado en: {args.out}")


def main():
    parser = argparse.ArgumentParser(prog="investigadopedia", description="Investigadopedia Autonomous Research Toolkit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Harvest
    p_harvest = subparsers.add_parser("harvest", help="Cosecha de literatura (SciELO, Redalyc, OpenAlex)")
    p_harvest.add_argument("--engine", choices=["scielo", "redalyc", "openalex"], required=True)
    p_harvest.add_argument("--query", required=True)
    p_harvest.add_argument("--max", type=int, default=100)
    p_harvest.add_argument("--out", required=True)
    p_harvest.set_defaults(func=handle_harvest)

    # Merge
    p_merge = subparsers.add_parser("merge", help="Fusión y deduplicación segura")
    p_merge.add_argument("--inputs", nargs="+", required=True)
    p_merge.add_argument("--out", required=True)
    p_merge.set_defaults(func=handle_merge)

    # Partition
    p_part = subparsers.add_parser("partition", help="Partición en literatura académica vs gris")
    p_part.add_argument("--input", required=True)
    p_part.add_argument("--out-dir", required=True)
    p_part.set_defaults(func=handle_partition)

    # Screen
    p_screen = subparsers.add_parser("screen", help="Cribado de títulos/abstracts con Jev / Heurística")
    p_screen.add_argument("--input", required=True)
    p_screen.add_argument("--criteria", required=True)
    p_screen.add_argument("--out", required=True)
    p_screen.set_defaults(func=handle_screen)

    # Audit
    p_audit = subparsers.add_parser("audit-text", help="Auditoría de tripartición epistemológica en texto")
    p_audit.add_argument("--file", required=True)
    p_audit.set_defaults(func=handle_audit_text)

    # Review Manuscript
    p_review = subparsers.add_parser("review-manuscript", help="Simulación de arbitraje editorial por pares")
    p_review.add_argument("--file", required=True)
    p_review.add_argument("--out", required=False)
    p_review.set_defaults(func=handle_review_manuscript)

    # Match (JANE Latam Ciencias Sociales)
    p_match = subparsers.add_parser("match", help="Estimador de revistas y autores en Ciencias Sociales (JANE Latam)")
    p_match.add_argument("--text", help="Texto directo del abstract o título")
    p_match.add_argument("--file", help="Ruta a archivo de texto/markdown con el abstract")
    p_match.add_argument("--top", type=int, default=5, help="Cantidad máxima de revistas sugeridas")
    p_match.add_argument("--diamond-only", action="store_true", default=True, help="Filtrar solo revistas Acceso Abierto Diamante (sin APC)")
    p_match.add_argument("--scramble", action="store_true", help="Anonimizar y desordenar palabras antes de evaluar")
    p_match.add_argument("--live-authors", action="store_true", help="Consultar OpenAlex en vivo para extraer autores y revisores recientes en esas revistas")
    p_match.add_argument("--out", help="Ruta de salida para guardar reporte Markdown")
    p_match.set_defaults(func=handle_match)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
