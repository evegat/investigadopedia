# Investigadopedia Match Web — Despliegue en `investigadopedia.evegat.cl`

Buscador y recomendador de revistas diamantinas para Ciencias Sociales e Iberoamérica.

## Arquitectura
- **Frontend**: HTML5, Tailwind CSS CDN, Inter/Merriweather, FontAwesome.
- **Lógica**: JavaScript nativo puro en `app.js` (zero-build, zero npm dependencies).
- **Datos**: Catálogo compilado en `data/journals.json` (21 revistas de SciELO/Redalyc/Latindex 2.0).
- **APIs externas**: Consulta opcional client-side directa a OpenAlex Works API para extracción en vivo de revisores pares.

## Despliegue en `investigadopedia.evegat.cl`

### Opción A: Cloudflare Pages (Recomendada / Cero costo de servidor)
1. Subir la carpeta `web/` al repositorio en GitHub (o como rama/directorio).
2. En Cloudflare Dashboard > Pages:
   - Conectar repositorio GitHub.
   - Build output directory: `web`
   - Build command: *(dejar vacío, es HTML estático puro)*.
3. Custom Domain: Asignar `investigadopedia.evegat.cl`. SSL y CDN global automáticos.

### Opción B: Coolify / VPS Hostinger
1. Crear una aplicación estática (Nginx Alpine) en Coolify apuntando a la carpeta `web/`.
2. Asignar dominio: `https://investigadopedia.evegat.cl`.

## Prueba Local Inmediata
```bash
python -m http.server 8080 --directory "2 - Project/EDI001 - Investigadopedia/web"
# Abrir en el navegador: http://localhost:8080
```
