"""Keyframe tracks and the SMIL markup that plays them on one shared loop."""
T = 31.0
EPS = 0.004

SPLINES = {
    "lin": (0, 0, 1, 1),
    "in": (0.55, 0, 1, 1),
    "out": (0, 0, 0.45, 1),
    "io": (0.45, 0, 0.55, 1),
    "snap": (0, 0, 0.15, 1),
    "soft": (0.3, 0, 0.3, 1),
}


def num(v):
    s = f"{v:.2f}" if abs(v) < 2 else f"{v:.1f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s.startswith("0.") or s.startswith("-0."):
        s = s.replace("0.", ".", 1)
    return "0" if s in ("-0", "") else s


def fmt(v):
    if isinstance(v, str):
        return v
    if isinstance(v, (tuple, list)):
        return " ".join(num(x) for x in v)
    return num(v)


def ease_at(name, x):
    x1, y1, x2, y2 = SPLINES[name]
    if (x1, y1, x2, y2) == (0, 0, 1, 1):
        return x
    lo, hi = 0.0, 1.0
    for _ in range(40):
        s = (lo + hi) / 2
        bx = 3 * (1 - s) ** 2 * s * x1 + 3 * (1 - s) * s * s * x2 + s ** 3
        if bx < x:
            lo = s
        else:
            hi = s
    s = (lo + hi) / 2
    return 3 * (1 - s) ** 2 * s * y1 + 3 * (1 - s) * s * s * y2 + s ** 3


def lerp(a, b, k):
    if isinstance(a, (tuple, list)):
        return tuple(lerp(x, y, k) for x, y in zip(a, b))
    return a + (b - a) * k


class Track:
    """Values over the loop. Each key says what the value is at time t and
    how the segment leading into it is eased."""

    def __init__(self, v0):
        self.keys = [[0.0, v0, "lin"]]

    @property
    def t(self):
        return self.keys[-1][0]

    @property
    def v(self):
        return self.keys[-1][1]

    def at(self, t, v, ease="io"):
        if t < self.t - 1e-6:
            raise ValueError(f"key at {t:.3f} is before {self.t:.3f}")
        t = max(t, self.t)
        if t - self.t < 1e-6 and len(self.keys) > 1:
            self.keys[-1][1] = v
            return self
        self.keys.append([t, v, ease])
        return self

    def hold(self, t):
        if t > self.t + 1e-6:
            self.at(t, self.v, "lin")
        return self

    def cut(self, t, v):
        self.hold(t)
        self.keys.append([max(t, self.t) + EPS, v, "lin"])
        return self

    def value(self, t):
        keys = self.keys
        if t >= keys[-1][0]:
            return keys[-1][1]
        for i in range(1, len(keys)):
            t1, v1, e = keys[i]
            if t <= t1:
                t0, v0, _ = keys[i - 1]
                if isinstance(v0, str):
                    return v0
                k = 0 if t1 == t0 else (t - t0) / (t1 - t0)
                return lerp(v0, v1, ease_at(e, k))
        return keys[-1][1]

    def constant(self):
        first = fmt(self.keys[0][1])
        return all(fmt(k[1]) == first for k in self.keys)


def _times(track):
    keys = [list(k) for k in track.keys]
    if keys[-1][0] < T - 1e-6:
        keys.append([T, keys[-1][1], "lin"])
    if keys[-1][0] > T + 1e-6:
        raise ValueError(f"track runs past the loop: {keys[-1][0]:.3f}")
    out, last = [], -1.0
    for t, v, e in keys:
        kt = round(t / T, 5)
        if kt <= last:
            kt = round(last + 0.00001, 5)
        out.append((min(kt, 1.0), v, e))
        last = kt
    fixed = list(out)
    fixed[-1] = (1.0, fixed[-1][1], fixed[-1][2])
    return fixed


def _attrs(track, discrete):
    keys = _times(track)
    values = ";".join(fmt(v) for _, v, _ in keys)
    times = ";".join(f"{kt:.5f}".rstrip("0").rstrip(".") or "0" for kt, _, _ in keys)
    s = f'dur="{T:g}s" repeatCount="indefinite" values="{values}" keyTimes="{times}"'
    if discrete:
        return s + ' calcMode="discrete"'
    splines = ";".join(" ".join(f"{c:g}" for c in SPLINES[e]) for _, _, e in keys[1:])
    return s + f' calcMode="spline" keySplines="{splines}"'


def animate(attr, track, discrete=False):
    if track is None or track.constant():
        return ""
    return f'<animate attributeName="{attr}" {_attrs(track, discrete)}/>'


def animate_transform(kind, track, discrete=False):
    if track is None or track.constant():
        return ""
    return f'<animateTransform attributeName="transform" type="{kind}" {_attrs(track, discrete)}/>'


def static_transform(kind, track):
    v = track.keys[0][1]
    if kind == "translate":
        return f"translate({fmt(v)})"
    if kind == "rotate":
        return f"rotate({fmt(v)})"
    return f"scale({fmt(v)})"


def wrap(inner, *layers):
    """Nest `inner` in one group per (kind, track[, discrete]) layer, outermost first.
    Constant layers collapse into a static transform; identity layers vanish."""
    identity = {"translate": "0 0", "rotate": "0", "scale": "1 1"}
    for layer in reversed(layers):
        kind, track = layer[0], layer[1]
        discrete = len(layer) > 2 and layer[2]
        if track is None:
            continue
        if track.constant():
            v = fmt(track.keys[0][1])
            if v in (identity[kind], "1") or (kind == "rotate" and v.split(" ")[0] == "0"):
                continue
            inner = f'<g transform="{static_transform(kind, track)}">{inner}</g>'
        else:
            inner = f"<g>{animate_transform(kind, track, discrete)}{inner}</g>"
    return inner


def opacity_attr(track):
    """Static opacity attribute plus an animate child, as a (attr, child) pair."""
    v0 = track.keys[0][1]
    attr = "" if v0 == 1 else f' opacity="{num(v0)}"'
    return attr, animate("opacity", track)



def wobble(track, t, base, amp, n=4, step=0.09, decay=0.55):
    """Damped oscillation around `base` starting at t (numbers only)."""
    track.hold(t)
    a = amp
    for i in range(n):
        track.at(t + step * (i + 1), base + (a if i % 2 == 0 else -a), "io")
        a *= decay
    track.at(t + step * (n + 1), base, "out")
    return track
