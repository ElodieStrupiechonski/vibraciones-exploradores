#!/bin/sh
# Construye la versión 1.2 a partir de la copia publicada de la versión 1.1 (rama main del repositorio).
# Uso: sh construir.sh ORIGEN_v1.1 DESTINO RUTA_cuaderno.ipynb RUTA_segueta_10cm.csv
# Las páginas de la v1.1 no se vuelven a pasar por mejoras.py (su paso de recuadros no es idempotente).
set -e
H=$(cd "$(dirname "$0")" && pwd); O=$(cd "$1" && pwd); mkdir -p "$2"; B=$(cd "$2" && pwd)
rm -rf "$B"; mkdir -p "$B"; (cd "$O" && find . -maxdepth 1 -type f ! -name '.git*' -exec cp {} "$B"/ \;)
cd "$H"
NUEVAS="analogias_interactivo.html transmisibilidad_interactivo.html modal_interactivo.html tutorial_phyphox.html choque_interactivo.html"
python3 gen_analog.py "$B"; python3 gen_trans.py "$B"; python3 gen_modal.py "$B"; python3 gen_choque.py "$B"; python3 gen_tutorial.py "$B" "$4"
python3 mejoras_nuevas.py "$B" $NUEVAS
[ -f retoques12.py ] && python3 retoques12.py "$B"
python3 integra2.py "$B"
cp "$3" "$4" "$B"/
if [ -d "$H/../extra" ]; then cp "$H"/../extra/* "$B"/; fi
mkdir -p "$B/herramientas"; cp "$H"/*.py "$H"/construir.sh "$B/herramientas"/; [ -d "$H/../qa" ] && cp "$H"/../qa/rev12.py "$H"/../qa/teclado.py "$H"/../qa/nuevos.py "$H"/../qa/audit.py "$B/herramientas"/ || true
