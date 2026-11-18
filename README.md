# Vibraciones: exploradores interactivos

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23422993.svg)](https://doi.org/10.5281/zenodo.23422993)

Colección de recursos educativos abiertos (REA) para el curso de **Vibraciones** de la licenciatura en **Ingeniería Aeroespacial**, ENES Juriquilla, UNAM. Cada explorador es una página HTML autónoma e interactiva: se mueve un control, o se escribe un valor, y se observa cómo responde el sistema.

**Versión 1.2 (2026)** · Portal en línea: https://elodiestrupiechonski.github.io/vibraciones-exploradores/

## Cómo usar

Abrir **`index.html`** en cualquier navegador actual. No se necesita conexión ni instalación: todo el código va incluido en cada archivo. El panel lateral permite recorrer los exploradores en el orden del programa (teclas ← y →) y buscar por nombre (tecla /). Para que las ligas funcionen, todos los archivos deben estar en la misma carpeta.

## Contenido

| Archivo | Contenido | Unidad · tema |
|---|---|---|
| `index.html` | Portada de la colección | |
| `edo3_interactivo.html` | Dinámica de la partícula: Al arrastrar la masa se ve el diagrama de cuerpo libre en vivo y se arma ΣF = ma → m·x″ + c·x′ + k·x = 0 | Fundamentos · Pilar 3 |
| `edo_interactivo.html` | EDO lineal de 2.º orden: Al mover los coeficientes o arrastrar las raíces en el plano s se observan Δ = b²−4ac y los cuatro regímenes | Fundamentos · Pilar 2 |
| `complejos_interactivo.html` | Números complejos: Al arrastrar z en el plano de Argand se leen |z| como amplitud, θ como desfase y sus raíces como régimen | Fundamentos · Pilar 1 |
| `analogias_interactivo.html` | Analogías entre sistemas: Al fijar masa, amortiguador y resorte se obtienen el circuito RLC análogo, el sistema de torsión y el hidráulico, con la misma frecuencia natural y el mismo amortiguamiento | U2 · 2.1 y 2.4 |
| `coulomb_interactivo.html` | Fricción de Coulomb: Al soltar el bloque se observa cómo la fricción seca Ff = μN hace que la amplitud caiga en línea recta (no exponencial) hasta detenerse dentro de una banda | U2 · 2.3 (fricción seca) |
| `forzada_interactivo.html` | Respuesta forzada y resonancia: Al barrer la frecuencia r = ω/ωn se observan el factor de amplificación M, la fase φ y el pico de resonancia | U3 · 3.1 |
| `mediapotencia_interactivo.html` | Media potencia y factor Q: Al variar el amortiguamiento se observa cómo el pico sube y se angosta. Los puntos donde la amplitud cae a Mmáx/√2 dan el ancho de banda Δf | U3 · 3.1–3.2 |
| `espectro_interactivo.html` | Del espectro a la carga de diseño: Tres paneles encadenados: lo que impone la norma W(f), lo que aporta la resonancia del equipo |H(f)|² y la respuesta que resulta | U4 · 4.1–4.2 |
| `normas.html` | Dónde consultar las normas: Las normas citadas en la Unidad 4, con el enlace oficial de cada una y el aviso de si la descarga es libre o hay que comprarla | U4 · 4.1 y 4.3 · apoyo |
| `mohr_interactivo.html` | Círculo de Mohr: El elemento diferencial y el círculo de Mohr, lado a lado y sincronizados: al girar el corte un ángulo θ, el punto recorre el círculo a 2θ. Incluye la roseta de galgas y los tres círculos | U5 · 5.3 |
| `fatiga_interactivo.html` | Fatiga: S–N, Haigh y Miner: Curva S–N en log–log y diagrama de Haigh con el estado de la pieza; Goodman, Soderberg y Gerber; daño acumulado de un ensayo de vibración aleatoria con las tres bandas de Steinberg | U5 · 5.4 |
| `sonido_interactivo.html` | Niveles sonoros y exposición al ruido: Espectro en bandas de octava editable, nivel total y ponderado A, ley de distancia, varias fuentes y tiempo permitido según la NOM-011-STPS-2001. Con micrófono relativo opcional | U6 · 6.1, 6.2 y 6.4 |
| `transmisibilidad_interactivo.html` | Transmisibilidad y aislamiento: Al variar masa, rigidez, amortiguamiento y frecuencia se lee cuánto movimiento o cuánta fuerza se transmite, y desde qué frecuencia el soporte aísla | U6 · 6.3 |
| `tutorial_phyphox.html` | Tutorial: medir con Phyphox y analizar en Python: Ligas para instalar Phyphox y descargar el cuaderno de Jupyter, instrucciones para Colab y Visual Studio Code, y un analizador que reproduce el tratamiento del decaimiento | U7 · 7.1 |
| `senales_interactivo.html` | Laboratorio de señales: Una señal sintética o un CSV de Phyphox se muestrea, se corta en segmentos y se promedia: aliasing, fuga, resolución y error aleatorio a la vista | U7 · 7.1–7.2 |
| `modal_interactivo.html` | Extracción de parámetros modales: Sobre una función de respuesta en frecuencia con dos modos y ruido se comparan tres métodos: media potencia, círculo de Nyquist y recta de la FRF inversa | U7 · 7.3 |
| `dosgdl_interactivo.html` | Dos grados de libertad y absorbedor: Al montar un segundo sistema sobre la estructura, la resonancia se divide en dos modos; un absorbedor sintonizado anula la respuesta en su frecuencia | U8 · 8.1–8.3 |

Otros archivos: `Tratamiento_decaimiento_Phyphox.ipynb` (cuaderno de Jupyter del tutorial), `segueta_10cm.csv` (registro de ejemplo), `Hoja_alumno_Pilar1_Complejos.docx`, `Hoja_alumno_Pilar2_EDO.docx` y `Hoja_alumno_Pilar3_Dinamica.docx` (hojas de trabajo), `normas.json` (referencias normativas), `temario.json` (fuente única del panel de navegación, del índice y de los metadatos), `sitemap.xml`, `CHANGELOG.md`.

## Reglas de estilo

Las mismas que en el sitio de Teoría Electromagnética: tipografía institucional (Century Gothic o equivalente en títulos, Arial en texto, Cambria en fórmulas); fórmulas en notación matemática con subíndices y superíndices reales, también en las gráficas; redacción impersonal, sin rayas ni emojis decorativos; todo valor se puede fijar con el deslizador o escribirse con el teclado; cada resultado numérico se verifica con un cálculo independiente; las referencias son libros de texto reconocidos o publicaciones con DOI comprobado.

## Mantenimiento

La carpeta `herramientas/` contiene los scripts de Python que generan y homologan las páginas (todos idempotentes salvo `mejoras.py`, que se aplicó una sola vez en la versión 1.1). Para añadir un explorador: registrarlo en `temario.json` dentro de su unidad, en el orden del programa, y ejecutar `integra2.py`. `construir.sh` reconstruye la versión actual a partir de la anterior; `rev12.py`, `teclado.py`, `nuevos.py` y `audit.py` son las pruebas automáticas (Playwright) que comparan las lecturas con cálculos independientes.

## Licencia

Creative Commons Attribution 4.0 International (**CC BY 4.0**).

## Cómo citar

Strupiechonski, E., & de Luna Bugallo, A. (2026). *Vibraciones: exploradores interactivos* (Versión 1.2) [Recurso educativo abierto]. UNAM, ENES Juriquilla. DOI: 10.5281/zenodo.23422993

## Autoría

- Elodie Strupiechonski: ENES Juriquilla, UNAM · ORCID [0000-0001-8991-8499](https://orcid.org/0000-0001-8991-8499)
- Andrés de Luna Bugallo: CFATA, UNAM · ORCID [0000-0002-7591-5235](https://orcid.org/0000-0002-7591-5235)

El historial de cambios está en [`CHANGELOG.md`](CHANGELOG.md).
