"""Shapes and the Sprite wrapper that moves, scales, spins and fades them."""
import html
import math

from metrics import measure
from smil import Track, opacity_attr, wrap, num


class Sprite:
    def __init__(self, inner, x=0, y=0, alpha=0.0, scale=1.0):
        self.inner = inner
        self.pos = Track((x, y))
        self.scale = Track((scale, scale))
        self.rot = Track(0)
        self.alpha = Track(alpha)

    def show(self, t):
        self.alpha.cut(t, 1)
        return self

    def hide(self, t):
        self.alpha.cut(t, 0)
        return self

    def fade(self, t0, t1, v):
        self.alpha.hold(t0).at(t1, v, "io")
        return self

    def pop_in(self, t, dur=0.28, peak=1.18):
        self.scale.cut(t, (0.05, 0.05))
        self.alpha.cut(t, 1)
        self.scale.at(t + dur * 0.6, (peak, peak), "out").at(t + dur, (1, 1), "io")
        return self

    def pop_out(self, t, dur=0.22):
        self.scale.hold(t).at(t + dur * 0.4, (1.12, 1.12), "out").at(t + dur, (0.05, 0.05), "in")
        self.alpha.cut(t + dur, 0)
        return self

    def go(self, t0, t1, x, y, ease="io"):
        self.pos.hold(t0).at(t1, (x, y), ease)
        return self

    def arc(self, t0, t1, x, y, h=30, ease_up="out", ease_down="in"):
        x0, y0 = self.pos.v
        tm = (t0 + t1) / 2
        self.pos.hold(t0).at(tm, ((x0 + x) / 2, min(y0, y) - h), ease_up).at(t1, (x, y), ease_down)
        return self

    def render(self):
        a_attr, a_anim = opacity_attr(self.alpha)
        body = wrap(self.inner, ("translate", self.pos), ("rotate", self.rot), ("scale", self.scale))
        return f"<g{a_attr}>{a_anim}{body}</g>"


def text(s, x, y, size, fill, weight=None, anchor=None, italic=False, length=True, mono=False):
    w = measure(s, size, bool(weight)) if not mono else len(s) * size * 0.6
    attrs = f'x="{num(x)}" y="{num(y)}" font-size="{size}" fill="{fill}"'
    if weight:
        attrs += f' font-weight="{weight}"'
    if anchor:
        attrs += f' text-anchor="{anchor}"'
    if italic:
        attrs += ' font-style="italic"'
    if mono:
        attrs += ' font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"'
    if length:
        attrs += f' textLength="{num(w)}" lengthAdjust="spacingAndGlyphs"'
    return f"<text {attrs}>{html.escape(s)}</text>"


def bubble(s, pal, tail_dx=0, below=False):
    """A speech bubble whose tail tip sits on the local origin, above it or below it."""
    w = measure(s, 12) + 16
    h = 21
    x0 = -w / 2 + tail_dx
    y0 = 7 if below else -h - 7
    edge = y0 + 0.5 if below else y0 + h - 0.5
    cover = y0 - 0.2 if below else y0 + h - 2.2
    tail = f"M{num(-4 + tail_dx * 0.3)} {num(edge)} L0 0 L{num(4 + tail_dx * 0.3)} {num(edge)}Z"
    return (f'<rect x="{num(x0)}" y="{num(y0)}" width="{num(w)}" height="{h}" rx="10.5" fill="{pal["bg"]}" '
            f'stroke="{pal["line"]}" stroke-width="1.2"/>'
            f'<path d="{tail}" fill="{pal["bg"]}" stroke="{pal["line"]}" stroke-width="1.2" stroke-linejoin="round"/>'
            f'<rect x="{num(-5 + tail_dx * 0.3)}" y="{num(cover)}" width="10" height="2.4" fill="{pal["bg"]}"/>'
            + text(s, x0 + w / 2, y0 + 14.5, 12, pal["fg"], anchor="middle"))


def star(r, k=0.28):
    q = r * k
    return (f"M0 {num(-r)} Q{num(q)} {num(-q)} {num(r)} 0 Q{num(q)} {num(q)} 0 {num(r)} "
            f"Q{num(-q)} {num(q)} {num(-r)} 0 Q{num(-q)} {num(-q)} 0 {num(-r)}Z")


def sparkle(pal, r=6, color=None):
    return f'<path d="{star(r)}" fill="{color or pal["gold"]}"/>'


def puff(pal):
    dots = []
    for i in range(6):
        a = i * math.pi / 3 + 0.3
        dots.append(f'<circle cx="{num(math.cos(a) * 9)}" cy="{num(math.sin(a) * 6 - 4)}" r="{num(3.2 + (i % 2))}"/>')
    return f'<g fill="{pal["smoke"]}">{"".join(dots)}</g>'


def ai_defs(pal):
    return (f'<linearGradient id="ai" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{pal["ai1"]}"/><stop offset=".55" stop-color="{pal["ai2"]}"/>'
            f'<stop offset="1" stop-color="{pal["ai3"]}"/></linearGradient>'
            f'<radialGradient id="aiglow"><stop offset="0" stop-color="{pal["ai2"]}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{pal["ai2"]}" stop-opacity="0"/></radialGradient>')


def orb():
    """The AI helper: a sparkle with a soft glow that bobs on its own."""
    return ('<g><animateTransform attributeName="transform" type="translate" values="0 -1.6;0 1.6;0 -1.6" '
            'dur="2.2s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/>'
            '<circle r="17" fill="url(#aiglow)"/>'
            f'<path d="{star(9.5, 0.24)}" fill="url(#ai)"/>'
            f'<g transform="translate(9 -8)"><path d="{star(3.6, 0.3)}" fill="url(#ai)">'
            '<animate attributeName="opacity" values="1;.35;1" dur="1.6s" repeatCount="indefinite"/></path></g></g>')


def dots(pal):
    out = []
    for i in range(3):
        out.append(f'<circle cx="{i * 7}" cy="0" r="2.2" fill="url(#ai)">'
                   f'<animate attributeName="opacity" values=".25;1;.25" dur=".9s" begin="{i * 0.15:.2f}s" '
                   f'repeatCount="indefinite"/></circle>')
    return "".join(out)


def ai_bubble(w, pal, h=22):
    """A chat bubble whose left-centre sits on the origin, with an AI-gradient edge."""
    return (f'<rect x="0" y="{num(-h / 2)}" width="{num(w)}" height="{h}" rx="{num(h / 2)}" fill="{pal["bg"]}" '
            f'stroke="url(#ai)" stroke-width="1.5"/>')


def shuttle(pal):
    return (f'<path d="M-1.9 -1.4 L-4.6 -10 L4.6 -10 L1.9 -1.4Z" fill="{pal["bg"]}" stroke="{pal["fg"]}" '
            f'stroke-width="0.9" stroke-linejoin="round"/>'
            f'<path d="M0 -1.4 V-10 M-1 -1.4 L-2.4 -10 M1 -1.4 L2.4 -10" stroke="{pal["fg"]}" stroke-width="0.6"/>'
            f'<circle cx="0" cy="0" r="2.4" fill="{pal["fg"]}"/>')


def net(pal, h=30):
    mesh = "".join(f'<path d="M-5 {-h + 3 + i * 5} H5" stroke="{pal["muted"]}" stroke-width=".6"/>'
                   for i in range(4))
    return (f'<rect x="-1" y="{-h}" width="2" height="{h}" rx="1" fill="{pal["muted"]}"/>'
            f'<rect x="-5" y="{-h}" width="10" height="19" fill="none" stroke="{pal["muted"]}" stroke-width=".8"/>'
            + mesh)


def cloud(pal):
    c = pal["cloud"]
    return (f'<g fill="{c}"><circle cx="-38" cy="0" r="16"/><circle cx="-12" cy="-12" r="22"/>'
            f'<circle cx="18" cy="-8" r="19"/><circle cx="42" cy="2" r="14"/>'
            f'<rect x="-52" y="0" width="106" height="16" rx="8"/></g>'
            f'<path d="M-46 14 H50" stroke="{pal["cloud_dark"]}" stroke-width="3" stroke-linecap="round" opacity=".5"/>')


def rain(pal, x0, x1, y0, y1, n=26, seed=0):
    drops = []
    for i in range(n):
        x = x0 + (x1 - x0) * ((i * 0.618 + seed) % 1)
        begin = (i * 0.137) % 0.6
        dur = 0.5 + (i % 4) * 0.04
        drops.append(
            f'<path d="M{num(x)} {num(y0)} l-2 7" stroke="{pal["rain"]}" stroke-width="1.6" stroke-linecap="round">'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;-10 {num(y1 - y0)}" '
            f'dur="{dur:.2f}s" begin="{begin:.2f}s" repeatCount="indefinite"/></path>')
    return "".join(drops)


def sun(pal):
    rays = "".join(
        f'<path d="M0 -19 V-25" stroke="{pal["gold"]}" stroke-width="2.4" stroke-linecap="round" '
        f'transform="rotate({i * 45})"/>' for i in range(8))
    return (f'<g>{rays}<animateTransform attributeName="transform" type="rotate" values="0;360" dur="12s" '
            f'repeatCount="indefinite"/></g><circle r="13" fill="{pal["gold"]}"/>')


def umbrella(pal, w):
    """T, opened up. The handle sits on the local origin."""
    r = w / 2
    scallops = "".join(
        f'<path d="M{num(-r + i * w / 5)} -46 q{num(w / 10)} 7 {num(w / 5)} 0" fill="{pal["fg"]}"/>'
        for i in range(5))
    return (f'<path d="M0 -46 V-6 q0 6 -5 6 q-5 0 -5 -5" fill="none" stroke="{pal["fg"]}" stroke-width="3.2" '
            f'stroke-linecap="round"/>'
            f'<path d="M{num(-r)} -46 Q{num(-r)} -84 0 -84 Q{num(r)} -84 {num(r)} -46Z" fill="{pal["fg"]}"/>'
            + scallops)


def rooftops(pal, spans, y):
    """Pagoda roofs whose eaves sit on y. spans: (x0, x1) per building."""
    out = []
    for i, (x0, x1) in enumerate(spans):
        w = x1 - x0
        out.append(
            f'<rect x="{num(x0 + 6)}" y="{num(y + 2)}" width="{num(w - 12)}" height="40" fill="{pal["roof"]}"/>'
            f'<path d="M{num(x0 - 4)} {num(y + 4)} Q{num(x0 + 8)} {num(y + 2)} {num(x0 + 14)} {num(y - 6)} '
            f'H{num(x1 - 14)} Q{num(x1 - 8)} {num(y + 2)} {num(x1 + 4)} {num(y + 4)}Z" fill="{pal["roof_dark"]}"/>'
            f'<rect x="{num(x0 + w / 2 - 5)}" y="{num(y + 14)}" width="10" height="9" rx="1.5" '
            f'fill="{pal["window"]}"/>')
    return "".join(out)


def shuriken(pal, r=5):
    return (f'<g><animateTransform attributeName="transform" type="rotate" values="0;360" dur=".35s" '
            f'repeatCount="indefinite"/><path d="{star(r, 0.2)}" fill="{pal["steel"]}"/>'
            f'<circle r="{num(r * 0.22)}" fill="{pal["bg"]}"/></g>')


def ring(pal, r=10):
    return f'<circle r="{r}" fill="none" stroke="{pal["gold"]}" stroke-width="2"/>'


def crate(pal):
    """A box with a shuttle stencil, origin at its bottom centre."""
    return (f'<rect x="-14" y="-16" width="28" height="16" rx="2" fill="{pal["wood"]}" '
            f'stroke="{pal["wood_dark"]}" stroke-width="1.2"/>'
            f'<path d="M-14 -8 H14" stroke="{pal["wood_dark"]}" stroke-width=".8"/>'
            f'<g transform="translate(0 -4) scale(.7)">{shuttle(pal)}</g>')


def hammer(pal):
    """Handle pivots on the origin; the head points up."""
    return (f'<path d="M0 0 V-9" stroke="{pal["wood_dark"]}" stroke-width="1.6" stroke-linecap="round"/>'
            f'<rect x="-3.5" y="-12" width="7" height="4" rx="1" fill="{pal["steel"]}"/>')


def popcorn(pal):
    kernels = "".join(
        f'<circle cx="{x}" cy="-9" r="1.4" fill="#fff3c4" stroke="{pal["wood_dark"]}" stroke-width=".3">'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;{dx} -7;{dx * 1.6} 0" '
        f'dur=".8s" begin="{b}s" repeatCount="indefinite"/></circle>'
        for x, dx, b in ((-1.5, -2, 0), (1, 2, 0.35), (0, 1, 0.6)))
    return (kernels + '<path d="M-4 -9 L-3 0 H3 L4 -9Z" fill="#ffffff" stroke="#cf222e" stroke-width=".8"/>'
            '<path d="M-2 -9 L-1.5 0 M1.5 -9 L1 0" stroke="#cf222e" stroke-width="1"/>'
            '<path d="M-4 -9 q1 -3 2.5 -1 q1.5 -3 3 0 q1.5 -2 2.5 1Z" fill="#fff3c4"/>')


def leaf(pal):
    return (f'<path d="M-9 0 Q0 -9 9 0 Q0 -3 -9 0Z" fill="{pal["leaf"]}"/>'
            f'<path d="M0 -3 V6" stroke="{pal["leaf_dark"]}" stroke-width="1.1" stroke-linecap="round"/>')


def watering_can(pal):
    drops = "".join(
        f'<circle cx="0" cy="0" r="1.1" fill="{pal["rain"]}">'
        f'<animateTransform attributeName="transform" type="translate" values="11 -9;17 -2;19 6" dur=".45s" '
        f'begin="{b}s" repeatCount="indefinite"/></circle>' for b in (0, 0.15, 0.3))
    return (drops + f'<rect x="-5" y="-11" width="10" height="9" rx="2" fill="{pal["can"]}"/>'
            f'<path d="M5 -9 L11 -12" stroke="{pal["can"]}" stroke-width="2" stroke-linecap="round"/>'
            f'<path d="M-5 -9 q-4 1 -2 5" fill="none" stroke="{pal["can"]}" stroke-width="1.4"/>')


def stem(pal, h):
    return (f'<path d="M0 0 V{-h}" stroke="{pal["leaf_dark"]}" stroke-width="1.6" stroke-linecap="round"/>'
            f'<path d="M0 {-h * 0.45} q4 -3 6 0 q-3 2 -6 0Z" fill="{pal["leaf"]}"/>')


def bloom(color, center="#f6c343"):
    petals = "".join(f'<circle cx="0" cy="-3.6" r="2.6" fill="{color}" transform="rotate({a})"/>'
                     for a in range(0, 360, 72))
    return petals + f'<circle r="2" fill="{center}"/>'
