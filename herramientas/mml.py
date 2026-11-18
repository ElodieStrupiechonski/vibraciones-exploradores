# -*- coding: utf-8 -*-
r"""Convertidor mínimo de un subconjunto de LaTeX a MathML de presentación (MathML Core).
Uso: from mml import M;  M(texto_latex)  -> <math display="block">…</math>
                         M(r"\zeta", inline=True)                       -> <math>…</math>
Sin dependencias: el MathML se incrusta en el HTML y los navegadores actuales lo dibujan sin conexión."""
import re, html

GREEK = dict(alpha="α", beta="β", gamma="γ", delta="δ", epsilon="ε", varepsilon="ε", zeta="ζ", eta="η", theta="θ", kappa="κ", lambda_="λ", mu="μ", nu="ν",
             xi="ξ", pi="π", rho="ρ", sigma="σ", tau="τ", phi="φ", varphi="φ", chi="χ", psi="ψ", omega="ω", Gamma="Γ", Delta="Δ", Theta="Θ", Lambda="Λ",
             Sigma="Σ", Phi="Φ", Psi="Ψ", Omega="Ω")
GREEK["lambda"] = "λ"
OPS = dict(cdot="·", times="×", pm="±", mp="∓", approx="≈", leq="≤", le="≤", geq="≥", ge="≥", neq="≠", to="→", rightarrow="→", Rightarrow="⇒",
           propto="∝", lesssim="≲", gtrsim="≳", ll="≪", gg="≫", sim="∼", equiv="≡", in_="∈", partial="∂", infty="∞", ldots="…", cdots="⋯", angle="∠", degree="°", prime="′")
BIG = dict(sum="∑", int="∫", prod="∏")
FUNCS = ["cos", "sin", "sen", "tan", "arctan", "atan", "log", "ln", "exp", "max", "min", "lim", "det", "erf", "Re", "Im", "atan2"]
SPACES = {",": "0.17em", ";": "0.28em", ":": "0.22em", "quad": "1em", "qquad": "2em", " ": "0.25em", "!": "0em"}
ACCENTS = dict(bar="‾", dot="˙", ddot="¨", hat="^", vec="→", tilde="~", overline="‾")

def tokenize(s):
    return re.findall(r"\\[a-zA-Z]+\*?|\\.|[0-9]+(?:\.[0-9]+)?|\s+|.", s, flags=re.S)

class P:
    def __init__(self, s): self.t = tokenize(s); self.i = 0
    def peek(self):
        while self.i < len(self.t) and self.t[self.i].isspace(): self.i += 1
        return self.t[self.i] if self.i < len(self.t) else None
    def next(self): x = self.peek(); self.i += 1; return x
    def group(self):
        """Lee un argumento: {…} o un solo átomo."""
        if self.peek() == "{":
            self.next(); out = self.seq(stop=("}",)); self.next(); return row(out)
        return self.atom()
    def raw_group(self):
        assert self.next() == "{"; d = 1; out = []
        while True:
            x = self.t[self.i] if self.i < len(self.t) else None; self.i += 1
            if x is None: break
            if x == "{": d += 1
            if x == "}":
                d -= 1
                if d == 0: break
            out.append(x)
        return "".join(out)
    def seq(self, stop=()):
        out = []
        while self.peek() is not None and self.peek() not in stop:
            a = self.atom()
            if a is None: continue
            # sub / superíndices
            while self.peek() in ("_", "^", "'"):
                sub = sup = None
                while self.peek() in ("_", "^", "'"):
                    op = self.next()
                    if op == "_": sub = self.group()
                    elif op == "^": sup = self.group()
                    else: sup = "<mo>′</mo>" if sup is None else row([sup, "<mo>′</mo>"])
                big = a.startswith("<mo largeop")
                if sub and sup: a = ("<munderover>%s%s%s</munderover>" if big else "<msubsup>%s%s%s</msubsup>") % (a, sub, sup)
                elif sub: a = ("<munder>%s%s</munder>" if big else "<msub>%s%s</msub>") % (a, sub)
                else: a = ("<mover>%s%s</mover>" if big else "<msup>%s%s</msup>") % (a, sup)
            out.append(a)
            if 'data-fn="1"' in a and a.count("<mi") + a.count("<mn") <= 3 and self.peek() not in ("(", "\\left", None, "}"): out.append('<mspace width="0.17em"></mspace>')
        return out
    def atom(self):
        x = self.next()
        if x is None: return None
        if x == "{":
            out = self.seq(stop=("}",)); self.next(); return row(out)
        if re.fullmatch(r"[0-9]+(\.[0-9]+)?", x): return "<mn>%s</mn>" % x
        if x.startswith("\\"):
            c = x[1:]
            if c in GREEK: return "<mi>%s</mi>" % GREEK[c]
            if c in OPS: return "<mo>%s</mo>" % OPS[c]
            if c == "in": return "<mo>∈</mo>"
            if c in BIG: return '<mo largeop="true" movablelimits="false">%s</mo>' % BIG[c]
            if c in FUNCS: return '<mi mathvariant="normal" data-fn="1">%s</mi>' % c
            if c in SPACES: return '<mspace width="%s"></mspace>' % SPACES[c]
            if c == "frac": a = self.group(); b = self.group(); return "<mfrac>%s%s</mfrac>" % (a, b)
            if c == "tfrac": a = self.group(); b = self.group(); return '<mstyle displaystyle="false"><mfrac>%s%s</mfrac></mstyle>' % (a, b)
            if c == "sqrt":
                if self.peek() == "[":
                    self.next(); n = row(self.seq(stop=("]",))); self.next(); return "<mroot>%s%s</mroot>" % (self.group(), n)
                return "<msqrt>%s</msqrt>" % self.group()
            if c in ("text", "mathrm", "operatorname"):
                r = self.raw_group()
                if c == "text": return "<mtext>%s</mtext>" % html.escape(r.replace("~", "\u00a0"))
                return '<mi mathvariant="normal">%s</mi>' % html.escape(r.replace(r"\,", "\u2009"))
            if c in ("mathbf", "boldsymbol"):
                r = self.raw_group(); return '<mi mathvariant="bold">%s</mi>' % html.escape(GREEK.get(r.lstrip("\\"), r))
            if c in ACCENTS: return '<mover accent="true">%s<mo>%s</mo></mover>' % (self.group(), ACCENTS[c])
            if c == "left":
                DL = {"\\{": "{", "\\}": "}", ".": "", "\\|": "‖", "\\lceil": "⌈", "\\rceil": "⌉", "\\lfloor": "⌊", "\\rfloor": "⌋"}
                a = self.next(); a = DL.get(a, a); inner = self.seq(stop=("\\right",)); self.next(); b = self.next(); b = DL.get(b, b)
                f = lambda d: ('<mo stretchy="true" fence="true">%s</mo>' % html.escape(d)) if d else ""
                return "<mrow>%s%s%s</mrow>" % (f(a), "".join(inner), f(b))
            if c == "begin":
                env = self.raw_group(); rows = [[[]]]
                while True:
                    if self.peek() == "\\end": self.next(); self.raw_group(); break
                    if self.peek() == "&": self.next(); rows[-1].append([]); continue
                    if self.peek() == "\\\\": self.next(); rows.append([[]]); continue
                    rows[-1][-1] += self.seq(stop=("&", "\\\\", "\\end"))
                body = "".join("<mtr>%s</mtr>" % "".join("<mtd>%s</mtd>" % row(c_) for c_ in r_) for r_ in rows if any(r_))
                l, r = {"bmatrix": ("[", "]"), "pmatrix": ("(", ")"), "vmatrix": ("|", "|"), "Bmatrix": ("{", "}"), "cases": ("{", "")}.get(env, ("", ""))
                al = ' columnalign="left"' if env in ("cases", "aligned") else ""
                t = "<mtable%s>%s</mtable>" % (al, body)
                return row(([('<mo stretchy="true" fence="true">%s</mo>' % l)] if l else []) + [t] + ([('<mo stretchy="true" fence="true">%s</mo>' % r)] if r else []))
            if c in ("{", "}", "%", "&", "#", "_"): return "<mo>%s</mo>" % html.escape(c)
            if c == "\\": return ""
            raise ValueError("comando no soportado: " + x)
        if x.isalpha(): return "<mi>%s</mi>" % x
        if x in "()[]|": return '<mo stretchy="false" lspace="0" rspace="0">%s</mo>' % x
        if x == "/": return '<mo lspace="0.05em" rspace="0.05em">/</mo>'
        if x in "+-=<>,;:!*.": return "<mo>%s</mo>" % {"-": "−", "<": "&lt;", ">": "&gt;", "*": "·"}.get(x, x)
        if x == "~": return '<mspace width="0.33em"></mspace>'
        return "<mo>%s</mo>" % html.escape(x)

def row(items):
    items = [i for i in items if i]
    return items[0] if len(items) == 1 and items[0].count("<m") == items[0].count("</m") and re.match(r"^<(m\w+)[^>]*>.*</\1>$", items[0], flags=re.S) and _single(items[0]) else "<mrow>%s</mrow>" % "".join(items)

def _single(s):
    """Verdadero si s es un único elemento MathML (no varios hermanos)."""
    depth = 0
    for m in re.finditer(r"<(/?)(m\w+)[^>]*?(/?)>", s):
        if m.group(3): continue
        depth += -1 if m.group(1) else 1
        if depth == 0 and m.end() != len(s): return False
    return True

def M(tex, inline=False, cls=None):
    body = row(P(tex).seq())
    attrs = "" if inline else ' display="block"'
    if cls: attrs += ' class="%s"' % cls
    return "<math%s>%s</math>" % (attrs, body)

if __name__ == "__main__":
    import sys
    print(M(sys.argv[1] if len(sys.argv) > 1 else r"M=\frac{1}{\sqrt{(1-r^2)^2+(2\zeta r)^2}}"))
