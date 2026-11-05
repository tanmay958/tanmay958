"""A small original ninja: headband with a blank plate, a scarf, four poses."""
from actor import Actor
from smil import Track, animate, num

ARMS = {
    "idle": "M-3 -13 L-5 -8 M3 -13 L5 -8",
    "sign": "M-3 -13 L3.5 -11.5 M3 -13 L4 -11",
    "throw": "M-3 -13 L-6.5 -10 M3 -13 L9.5 -15.5",
    "catch": "M-3 -13 L-5 -8 M3 -13 L6.5 -21",
}


class Ninja(Actor):
    eyes_x = (0.6, 3.2)
    eye_y = -19.4
    eye_r, pupil_r = 1.05, 0
    pivot = -11

    def __init__(self, x, y, scarf, face=1, alpha=0):
        super().__init__(x, y, alpha=alpha, awake=1)
        self.scarf = scarf
        self.face_tr = Track((face, 1))
        self.poses = {k: Track(1 if k == "idle" else 0) for k in ARMS}

    @property
    def face(self):
        return self.face_tr.v[0]

    def turn(self, t, face):
        if self.face != face:
            self.face_tr.at(t, (face, 1))
        return self

    def pose(self, t, name):
        for k, tr in self.poses.items():
            v = 1 if k == name else 0
            if tr.v != v:
                tr.cut(t, v)
        return self

    def head_at(self, t, top=27):
        return super().head_at(t, top)

    def outer(self):
        return (("scale", self.face_tr, True),)

    def eyes(self, pal):
        return "".join(f'<ellipse cx="{num(x)}" cy="0" rx="{self.eye_r}" ry=".75" fill="{pal["bg"]}"/>'
                       for x in self.eyes_x)

    def body(self, pal):
        c = pal["ninja"]
        arms = "".join(
            f'<path d="{d}" stroke="{c}" stroke-width="2.1" stroke-linecap="round" fill="none" '
            f'opacity="{num(self.poses[k].keys[0][1])}">{animate("opacity", self.poses[k])}</path>'
            for k, d in ARMS.items())
        scarf = (f'<path d="M-2.5 -15.5 q-6 0.5 -10.5 4 q4.5 -1.5 9.5 -1Z" fill="{self.scarf}">'
                 '<animateTransform attributeName="transform" type="rotate" values="0 -2.5 -15.5;-12 -2.5 -15.5;0 -2.5 -15.5" '
                 'dur=".5s" repeatCount="indefinite"/></path>')
        return (scarf
                + f'<path d="M-2 -6 L-3 0 M2 -6 L3 0" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/>'
                + f'<rect x="-4" y="-15.5" width="8" height="10" rx="3" fill="{c}"/>'
                + f'<circle cx="0" cy="-19.5" r="4.7" fill="{c}"/>'
                + f'<rect x="-4.9" y="-23.2" width="9.8" height="2.2" rx="1" fill="{self.scarf}"/>'
                + f'<rect x="0.4" y="-23.6" width="3.6" height="3" rx=".6" fill="{pal["plate"]}"/>'
                + arms)
