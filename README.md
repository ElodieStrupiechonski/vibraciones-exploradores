# Vibraciones — Exploradores interactivos

Material de apoyo del curso de **Vibraciones** · UNAM · ENES Juriquilla · Ingeniería Aeroespacial.

Tres exploradores interactivos que repasan los pilares de conocimiento previo del curso,
cada uno visto desde la ingeniería aeronáutica. Son la misma historia en tres pasos:

**Pilar 3 · Dinámica** (armar ΣF = ma) → **Pilar 2 · EDO** (resolver) → **Pilar 1 · Números complejos** (interpretar).

## 🌐 Sitio en vivo

Una vez publicado con GitHub Pages, el portal queda en:

```
https://TU-USUARIO.github.io/vibraciones-exploradores/
```

Comparte ese enlace en Google Classroom. El alumno trabaja en el navegador (Chromebook, tablet o PC), sin instalar nada.

## 📂 Contenido

| Archivo | Qué es |
|---|---|
| `index.html` | Portal / menú de entrada (empieza aquí) |
| `edo3_interactivo.html` | Pilar 3 · Dinámica de la partícula (ΣF = ma) |
| `edo_interactivo.html` | Pilar 2 · EDO lineal de 2.º orden |
| `complejos_interactivo.html` | Pilar 1 · Números complejos |
| `Hoja_alumno_Pilar3_Dinamica.docx` | Hoja de trabajo del alumno (Pilar 3) |
| `Hoja_alumno_Pilar2_EDO.docx` | Hoja de trabajo del alumno (Pilar 2) |
| `Hoja_alumno_Pilar1_Complejos.docx` | Hoja de trabajo del alumno (Pilar 1) |

## 🚀 Cómo publicarlo (GitHub Pages)

1. Crea un repositorio **público** (p. ej. `vibraciones-exploradores`) y sube estos archivos a la raíz.
2. En el repositorio: **Settings → Pages**.
3. En **Build and deployment → Source**, elige **Deploy from a branch**.
4. En **Branch**, selecciona `main` y la carpeta `/ (root)`; pulsa **Save**.
5. Espera 1–2 minutos y recarga: aparecerá la URL pública del sitio.

Para actualizar el contenido después, vuelve a subir los archivos (commit) y GitHub Pages
se vuelve a publicar solo.

## 🧩 Notas

- Funcionan **sin conexión** y **sin servidor**: son archivos autocontenidos (HTML + JS en un solo archivo, sin base de datos ni llamadas externas).
- Los valores aeronáuticos son **órdenes de magnitud ilustrativos**; los datos de diseño se toman de la normativa (CS-25 / FAR-25) y de la bibliografía citada en cada explorador.
- El archivo `.nojekyll` evita que GitHub Pages procese el sitio con Jekyll (no es necesario para estos archivos, pero se incluye por seguridad).

## Licencia / uso

Material educativo del curso. Adáptalo libremente para tu grupo.
