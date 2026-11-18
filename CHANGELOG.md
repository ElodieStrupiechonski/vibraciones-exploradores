# Historial de versiones

La numeración sigue las etiquetas (*tags*) de GitHub, que son las versiones archivadas en Zenodo. El DOI de concepto [10.5281/zenodo.23422993](https://doi.org/10.5281/zenodo.23422993) (citar «todas las versiones») resuelve siempre a la más reciente.

## [1.3] · 2026-11-18 · DOI de versión: se anota al publicar la *release* v1.3 en Zenodo

Quince exploradores y un tutorial. Reúne todo lo posterior a la v1.2 del 16 de octubre.

### Tutorial de medición y análisis
- `tutorial_phyphox.html` (U7 · 7.1): recorrido de siete pasos, del teléfono a la frecuencia natural y al amortiguamiento. Ligas de descarga de Phyphox (sitio oficial, Google Play, App Store), del cuaderno de Jupyter y del registro de ejemplo; instrucciones para Google Colab y para Visual Studio Code con tabla de errores frecuentes; analizador en el navegador (registro de ejemplo, archivo CSV propio o señal sintética) con espectro, envolvente de Hilbert y decremento logarítmico; lista de verificación. El avance por pasos se conserva en el navegador.
- `Tratamiento_decaimiento_Phyphox.ipynb`: cuaderno con el tratamiento completo en once pasos; `segueta_10cm.csv`: registro real de una hoja de segueta de 10 cm en voladizo (2390 muestras a 198.9 Hz). El cuaderno descarga el ejemplo si no lo encuentra.

### Exploradores nuevos
- `analogias_interactivo.html` (Pilar 14 · U2 · 2.1 y 2.4): analogías fuerza-tensión y fuerza-corriente, torsión e hidráulica; escala de impedancia; esquema del sistema y del circuito, respuesta al escalón superpuesta y tabla de equivalencias con los valores actuales; analogías con sistemas espaciales.
- `transmisibilidad_interactivo.html` (Pilar 13 · U6 · 6.3): base móvil, fuerza armónica y desbalance rotatorio; deflexión estática, desfase, máximo de la curva y cálculo de la frecuencia natural necesaria para un aislamiento dado.
- `modal_interactivo.html` (Pilar 15 · U7 · 7.3): extracción de la frecuencia natural y del amortiguamiento de una función de respuesta en frecuencia con dos modos y ruido por media potencia, círculo de Nyquist y recta de la FRF inversa, con el error de cada método frente al valor verdadero.

### Orden y navegación
- Los exploradores se recorren en el orden del programa: pilares de fundamentos (dinámica, EDO, números complejos) y unidades 2 a 8. Analogías abre la unidad 2; transmisibilidad cierra la 6; la unidad 7 sigue la secuencia tutorial, señales, extracción modal. La unidad 1 remite a los pilares y a transmisibilidad (sistemas rotatorios).
- El menú superior pasa a un panel lateral fijo, igual al del sitio de Teoría Electromagnética: anterior y siguiente con el nombre del explorador vecino, buscador (tecla /), lista por unidades con la página actual marcada y atajos ← →; en pantallas de menos de 1360 px se abre con «☰ Temario» (en el sitio de Teoría Electromagnética el umbral es 1100 px; aquí es mayor para que las gráficas de dos columnas no se reduzcan).
- Metadatos por página (descripción, URL canónica, Open Graph y JSON-LD como *LearningResource*) y `sitemap.xml`.

### Revisión con tres perfiles de lector
Tres revisiones independientes (estudiante de 7.º semestre, docente de la asignatura y autor de libro de texto) probaron el sitio completo. Cambios derivados:

- **Extracción modal.** La recta de la FRF inversa ajusta ahora la parte imaginaria por el origen, como exige el modelo; antes el ajuste con ordenada libre sobrestimaba ζ entre 20 y 70 %. La fórmula del círculo de Nyquist se declara aproximada para amortiguamiento viscoso (exacta para la movilidad o con amortiguamiento histerético). Preajuste «Un solo modo», botón «Nueva realización del ruido», avisos cuando la banda no contiene un modo o tiene menos de cinco puntos, glosario e hipótesis. El preajuste de resolución insuficiente coloca el pico entre dos líneas espectrales, donde la media potencia falla cerca de 30 %.
- **Transmisibilidad.** El último preajuste parte de ζ = 0.05 para que la comparación del texto se pueda seguir; los preajustes restablecen todo el estado; el límite de la fuerza transmitida por desbalance se enuncia correctamente; nota sobre la fase y sobre la rigidez dinámica de los elastómeros; rótulo del desfase según el caso; lecturas en notación de ingeniería.
- **Analogías.** Columnas «análoga de la fuerza» y «análoga de la velocidad» y nota corregida sobre las analogías de impedancia y de movilidad; ecuación e hipótesis del sistema hidráulico; esquema apilado en pantallas angostas; el amortiguador llega a 1000 N·s/m para alcanzar el régimen crítico con cualquier rigidez; referencia del control de actitud.
- **Tutorial y cuaderno.** Una sola lista de criterios en ambos (pico por debajo de 0.8 f_s/2, al menos 20 ciclos, R² ≥ 0.97, métodos a menos de 30 %, tres repeticiones dentro de 2 %); el cuaderno imprime «cumple» o «NO cumple». Se distingue el teléfono junto al empotramiento del teléfono sobre la viga y se añade la fórmula con masa en la punta (Rayleigh). El cuaderno usa la misma ventana que el analizador (media ventana de Hann decreciente) y el decremento por regresión sobre todos los máximos: los dos métodos coinciden ahora en ζ = 0.0034 para el ejemplo. El analizador avisa si se eligió la aceleración absoluta, si el filtro es estrecho o si no hay archivo cargado.
- **Tres páginas con modo práctica** («Ocultar lecturas») para usarlas como ejercicio.
- **Navegación.** Las flechas ← → ya no cambian de página cuando el foco está en un botón; el buscador también busca en temas y palabras clave y avisa cuando no hay coincidencias.
- **Páginas anteriores.** Del espectro a la carga de diseño: la respuesta se calcula con la transmisibilidad (excitación por la base) en lugar del factor de amplificación; con ζ = 0.05 la diferencia es de 0.5 %, con ζ = 0.20 llega a 8 %. Dos grados de libertad: el botón «Óptimo de Den Hartog» fija el amortiguamiento con la referencia correcta (el pico coincide con √(1 + 2/μ)) y las lecturas sin amortiguamiento muestran ∞. Respuesta forzada: «sin pico de resonancia (ζ ≥ 1/√2)» en lugar de «sobreamortiguado». Laboratorio de señales: unidades en m/s² con archivos de Phyphox. Unidades en los controles de Mohr y de fatiga; redacción impersonal y términos en español en ocho páginas; referencias bibliográficas en cinco páginas que no las tenían. La casilla numérica marca en rojo una entrada no válida.
- **Índice.** Cada unidad indica dónde se trabajan los subtemas que no tienen explorador propio y cuáles siguen sin explorador (1.1, 4.4, 5.1, 5.2, parte acústica de 6.3, 6.4 y 7.4).

Pendiente de esta revisión: variables en cursiva dentro de las gráficas, una tabla de notación común a todas las páginas, la unificación de x″ y ẍ, y textos de gráfica más grandes en fatiga.

### Verificación
- Pruebas automáticas en navegador (`qa/`): cada lectura de los exploradores nuevos se compara con un cálculo independiente en Python (NumPy y SciPy), incluida la integración temporal de la transmisibilidad, la respuesta al escalón y los tres métodos de extracción modal; entrada por teclado; orden de navegación; ausencia de desbordamiento a 390 px y de ligas locales rotas.

### Cambios del 11 al 13 de noviembre (publicados en la rama principal sin etiqueta; los archivos decían «Versión 1.1»)
- Exploradores nuevos: `senales_interactivo.html` (Pilar 11 · U7: muestreo, aliasing, ventanas y método de Welch, con lectura de archivos CSV de Phyphox) y `dosgdl_interactivo.html` (Pilar 12 · U8: dos grados de libertad, formas modales y absorbedor dinámico).
- Entrada por teclado: cada deslizador tiene una casilla numérica contigua; el valor escrito no queda limitado al paso del deslizador y se valida contra su intervalo.
- Fórmulas en notación matemática (MathML incrustado, sin bibliotecas externas), también en las etiquetas de las gráficas.
- Tipografía institucional (Century Gothic o equivalente en títulos, Arial en texto, Cambria en fórmulas), redacción impersonal y sin rayas.
- Correcciones: botones principales de los Pilares 1 a 5, aproximaciones marcadas con ≈ en media potencia y Miles, criterio de Gerber, formato del daño de Miner.


## [1.2] · 2026-10-16 y [1.1]

Versiones etiquetadas y archivadas en Zenodo en octubre de 2026 (diez exploradores: tres pilares de fundamentos y unidades 2 a 6, guía de normas, índice por unidades y barra de navegación). El detalle de cada una está en la página de *releases* del repositorio. Nota: entre el 11 y el 17 de noviembre los pies de página mostraron por error «Versión 1.1» y «Versión 1.2» para contenido posterior a la etiqueta v1.2; la versión 1.3 corrige la numeración.
