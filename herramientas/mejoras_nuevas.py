#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aplica a las páginas nuevas de la revisión 1.2 los pasos comunes de mejoras.py (rayas, subíndices, bloques de
tipografía y de teclado) sin volver a pasar las páginas ya tratadas: el paso de recuadros de mejoras.py no es idempotente.
Uso: python3 mejoras_nuevas.py CARPETA archivo.html [archivo.html …]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mejoras as m
for f in sys.argv[2:]:
    p = os.path.join(sys.argv[1], f); s = open(p, encoding="utf-8").read()
    s = m.bloques(m.subindices(m.rayas(m.emojis(s))))
    open(p, "w", encoding="utf-8").write(s); print("bloques comunes en", f)
