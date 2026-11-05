"""Characters: a shared motion base, the letters of the name and the spark minions."""
import html

from metrics import BOLD
from smil import T, Track, wrap, animate, animate_transform, num, opacity_attr

SIZE = 32


class Actor:
    """Anything with a position, squash and stretch, a lean and a pair of eyes."""
    eyes_x = (-3, 3)
    eye_y = -12
    eye_r, pupil_r = 2.7, 1.35
    pivot = -10

    def __init__(self, x, y, alpha=1, awake=1):
        self.x = Track(x)
        self.y = Track((0, y))
        self.rot = Track((0, 0, self.pivot))
        self.sq = Track((1, 1))
        self.alpha = Track(alpha)
        self.awake = Track(awake)
        self.look = Track((0, 0))
        self.closed = []

    @property
    def last(self):
        return self.x.v, self.y.v[1]

    def pos_at(self, t):
        return self.x.value(t), self.y.value(t)[1]

    def head_at(self, t, top=18):
        x, y = self.pos_at(t)
        return x, y - top

    # ----------------------------------------------------------- moves
    def hop(self, t0, x1, y1, dur=0.5, h=24, anticip=0.1, land=True, lean=8):
        x0, y0 = self.last
        d = 1 if x1 > x0 + 0.5 else (-1 if x1 < x0 - 0.5 else 0)
        ta = t0 - anticip
        self.sq.hold(ta).at(t0 - 0.02, (1.14, 0.84), "out")
        self.sq.at(t0 + 0.08, (0.88, 1.14), "snap").at(t0 + dur * 0.5, (1, 1), "io")
        self.x.hold(t0).at(t0 + dur, x1, "lin")
        apex = min(y0, y1) - h
        k = (y0 - apex) / max(1e-6, (y0 - apex) + (y1 - apex))
        k = min(0.75, max(0.25, k))
        self.y.hold(t0).at(t0 + dur * k, (0, apex), "out").at(t0 + dur, (0, y1), "in")
        if d and lean:
            self.tilt(t0, t0 + dur * 0.3, lean * d, "out")
            self.tilt(t0 + dur * 0.3, t0 + dur * 0.75, -lean * 0.4 * d)
            self.tilt(t0 + dur * 0.75, t0 + dur, 0, "out")
        te = t0 + dur
        if land:
            self.sq.hold(te - 0.03).at(te + 0.05, (1.2, 0.8), "snap")
        if land == "chain":
            self.sq.at(te + 0.1, (1.1, 0.88), "io")
        elif land:
            self.sq.at(te + 0.16, (0.95, 1.06), "io").at(te + 0.28, (1, 1), "io")
        return te

    def walk(self, t0, t1, x1, step=0.16, bob=2.5):
        """Scurry along the ground with little bobs."""
        x0, y0 = self.last
        self.x.hold(t0).at(t1, x1, "lin")
        t = t0
        while t + step <= t1 + 1e-6:
            self.y.hold(t).at(t + step / 2, (0, y0 - bob), "out").at(t + step, (0, y0), "in")
            t += step
        self.y.hold(t1)
        return t1

    def fly(self, t0, t1, x1, y1, ease="io"):
        self.x.hold(t0).at(t1, x1, ease)
        self.y.hold(t0).at(t1, (0, y1), ease)
        return t1

    def tilt(self, t0, t1, angle, ease="io"):
        self.rot.hold(t0).at(t1, (angle, 0, self.pivot), ease)
        return self

    def bounce(self, t, k=1.0):
        self.sq.hold(t).at(t + 0.06, (1 + 0.16 * k, 1 - 0.16 * k), "snap")
        self.sq.at(t + 0.18, (1 - 0.06 * k, 1 + 0.07 * k), "io").at(t + 0.3, (1, 1), "io")
        return t + 0.3

    def bow(self, t, hold=0.3):
        self.sq.hold(t).at(t + 0.2, (1.1, 0.76), "io").hold(t + 0.2 + hold).at(t + 0.45 + hold, (1, 1), "out")
        self.close_eyes(t + 0.05, t + 0.3 + hold)
        return t + 0.45 + hold

    def stretch(self, t, k=1.0, dur=0.6):
        self.sq.hold(t).at(t + dur * 0.5, (1 - 0.1 * k, 1 + 0.18 * k), "io").at(t + dur, (1, 1), "io")
        return t + dur

    def shiver(self, t0, t1, amp=1.4, step=0.05):
        x0 = self.x.v
        self.x.hold(t0)
        t, s = t0, 1
        while t + step < t1:
            t += step
            self.x.at(t, x0 + amp * s, "io")
            s = -s
        self.x.at(t1, x0, "io")
        return self

    def wiggle(self, t, n=4, amp=8, step=0.1):
        self.rot.hold(t)
        a = amp
        for i in range(n):
            self.rot.at(t + step * (i + 1), (a if i % 2 == 0 else -a, 0, self.pivot), "io")
            a *= 0.7
        self.rot.at(t + step * (n + 1), (0, 0, self.pivot), "out")
        return t + step * (n + 1)

    def peek(self, t, dx, dy, dur=0.15):
        self.look.hold(t).at(t + dur, (dx, dy), "io")
        return self

    def close_eyes(self, t0, t1):
        self.closed.append((t0, t1))
        return self

    def appear(self, t):
        self.alpha.cut(t, 1)
        return self

    def vanish(self, t):
        self.alpha.cut(t, 0)
        return self

    # ----------------------------------------------------------- render
    def _blink(self, period, first):
        events = list(self.closed)
        t = first
        while t + 0.3 < T:
            if not any(a - 0.5 <= t <= b + 0.6 for a, b in self.closed):
                events.append((t, None))
            t += period
        tr = Track((1, 1))
        for a, b in sorted(events):
            if b is None:
                tr.hold(a).at(a + 0.06, (1, 0.1), "in").at(a + 0.15, (1, 1), "out")
            else:
                tr.hold(a).at(a + 0.12, (1, 0.1), "io").hold(b).at(b + 0.15, (1, 1), "out")
        return tr

    def body(self, pal):
        raise NotImplementedError

    def eyes(self, pal):
        whites = "".join(f'<circle cx="{num(x)}" cy="0" r="{self.eye_r}" fill="#ffffff" stroke="{pal["pupil"]}" '
                         f'stroke-width=".8"/>' for x in self.eyes_x)
        pupils = "".join(f'<circle cx="{num(x)}" cy="0" r="{self.pupil_r}" fill="{pal["pupil"]}"/>'
                         for x in self.eyes_x)
        return whites + f'<g>{animate_transform("translate", self.look)}{pupils}</g>'

    def outer(self):
        """Extra transform layers inside the lean, e.g. which way the actor faces."""
        return ()

    def render(self, pal, period=2.6, first=1.2):
        eyes = wrap(self.eyes(pal), ("scale", self._blink(period, first)))
        eyes = (f'<g opacity="{num(self.awake.keys[0][1])}" transform="translate(0 {num(self.eye_y)})">'
                f'{animate("opacity", self.awake)}{eyes}</g>')
        body = wrap(self.body(pal) + eyes, ("translate", self.x), ("translate", self.y), ("rotate", self.rot),
                    ("scale", self.sq), *self.outer())
        a_attr, a_anim = opacity_attr(self.alpha)
        return f"<g{a_attr}>{a_anim}{body}</g>" if (a_anim or a_attr) else body


LETTER_EYES = {
    "T": ((-3.4, 3.4), -20.2),
    "a": ((-3.2, 3.2), -11.5),
    "n": ((-3.6, 3.6), -12),
    "m": ((-5, 5), -12),
    "y": ((-3.3, 3.5), -12.5),
}


class Letter(Actor):
    def __init__(self, ch, x, y, fg):
        self.ch = ch
        self.w = BOLD[ch] * SIZE
        self.home = (x + self.w / 2, y)
        self.eyes_x, self.eye_y = LETTER_EYES[ch]
        super().__init__(self.home[0], y, alpha=1, awake=0)
        self.fill = Track(fg)

    def head_at(self, t, top=None):
        return super().head_at(t, 25 if self.ch == "T" else 18)

    def body(self, pal):
        return (f'<text x="{num(-self.w / 2)}" y="0" font-size="{SIZE}" font-weight="600" '
                f'fill="{self.fill.keys[0][1]}" textLength="{num(self.w)}" lengthAdjust="spacingAndGlyphs">'
                f'{animate("fill", self.fill)}{html.escape(self.ch)}</text>')


class Minion(Actor):
    """A little spark from the AI orb: chubby, orange, always busy."""
    eyes_x = (-2.3, 2.3)
    eye_y = -8.5
    eye_r, pupil_r = 1.9, 1.0
    pivot = -7

    def __init__(self, x, y):
        super().__init__(x, y, alpha=0, awake=1)
        self.arms = {"down": Track(1), "up": Track(0), "push": Track(0)}

    def pose(self, t, name):
        for k, tr in self.arms.items():
            v = 1 if k == name else 0
            if tr.v != v:
                tr.cut(t, v)
        return self

    def head_at(self, t, top=17):
        return super().head_at(t, top)

    def body(self, pal):
        c, edge = pal["spark"], pal["spark_edge"]
        rays = "".join(
            f'<path d="M0 -15 V{num(-19 - (2 if a == 0 else 0))}" stroke="{c}" stroke-width="2.4" '
            f'stroke-linecap="round" transform="rotate({a} 0 -8)"/>' for a in (-28, 0, 28))
        arms = {
            "down": "M-5 -6 L-8 -3 M5 -6 L8 -3",
            "up": "M-5 -8 L-7 -14 M5 -8 L7 -14",
            "push": "M-4 -8 L3 -10 M4 -7 L9 -9",
        }
        arm_svg = "".join(
            f'<path d="{arms[k]}" stroke="{edge}" stroke-width="1.6" stroke-linecap="round" '
            f'opacity="{num(tr.keys[0][1])}">{animate("opacity", tr)}</path>' for k, tr in self.arms.items())
        return (rays + f'<ellipse cx="0" cy="-7.6" rx="7.4" ry="6.8" fill="{c}" stroke="{edge}" stroke-width="1"/>'
                + arm_svg
                + f'<path d="M-2.4 -1.2 V0.4 M2.4 -1.2 V0.4" stroke="{edge}" stroke-width="1.8" stroke-linecap="round"/>')
