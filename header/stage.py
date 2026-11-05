"""The stage: the page, the letters, the ninjas, the minions, the AI orb and shared effects."""
from actor import Letter
from metrics import measure
from page import Page, FONT_STACK, H1_Y, H1_SIZE, RULE_Y
from props import Sprite, bubble, puff, sparkle, text, ai_defs, orb, ai_bubble, dots
from smil import Track, animate, animate_transform, num, T

W, H = 830, 290
FLOOR = 280
NAME = "Tanmay"


class Stage:
    def __init__(self, pal):
        self.pal = pal
        self.page = Page()
        name = self.page.h1[-1]
        assert name.text == NAME
        self.letters, x = [], name.x
        for ch in NAME:
            letter = Letter(ch, x, H1_Y, pal["fg"])
            self.letters.append(letter)
            x += letter.w
        self.sky, self.back, self.front = [], [], []
        self.ninjas, self.minions = [], []
        self.defs = [ai_defs(pal)]
        self.wave = Track((0, self.page.emoji_x + 21, H1_Y - 2))
        self.orb = Sprite(orb(), x=300, y=22)
        self._clips = 0

    # ----------------------------------------------------------- effects
    def sprite(self, inner, layer="front", **kw):
        s = Sprite(inner, **kw)
        getattr(self, layer).append(s)
        return s

    def say(self, t0, t1, msg, x, y, tail_dx=0, below=False):
        s = self.sprite(bubble(msg, self.pal, tail_dx, below), x=x, y=y)
        s.pop_in(t0, 0.3)
        s.pop_out(t1 - 0.22)
        return s

    def say_letter(self, letter, t0, t1, msg, tail_dx=0):
        x, y = letter.head_at(t0)
        return self.say(t0, t1, msg, x, y - 4, tail_dx)

    def bang(self, t, x, y, mark="!", color=None, dur=0.7):
        s = self.sprite(text(mark, 0, 0, 15, color or self.pal["red"], weight="700", anchor="middle",
                             length=False), x=x, y=y)
        s.pop_in(t, 0.22, 1.35)
        s.pop_out(t + dur)
        return s

    def puff(self, t, x, y, k=1.0):
        s = self.sprite(puff(self.pal), x=x, y=y, scale=0.4 * k)
        s.alpha.cut(t, 0.9)
        s.scale.cut(t, (0.4 * k, 0.4 * k)).at(t + 0.35, (1.2 * k, 1.2 * k), "out")
        s.fade(t + 0.05, t + 0.4, 0)
        return s

    def sparkle(self, t, x, y, r=6, color=None, dur=0.5):
        s = self.sprite(sparkle(self.pal, r, color), x=x, y=y)
        s.pop_in(t, dur * 0.45, 1.3)
        s.rot.hold(t).at(t + dur, 90, "out")
        s.pop_out(t + dur * 0.55, dur * 0.45)
        return s

    def float_text(self, t, x, y, s, size=11, color=None, rise=16, dur=0.9, italic=True, weight=None):
        sp = self.sprite(text(s, 0, 0, size, color or self.pal["muted"], weight=weight, anchor="middle",
                              italic=italic, length=False), x=x, y=y)
        sp.alpha.cut(t, 0).at(t + 0.15, 1, "out").hold(t + dur * 0.6).at(t + dur, 0, "in")
        sp.go(t, t + dur, x + 4, y - rise, "out")
        return sp

    def clip(self, x, y, w, h, t0, t1, t_off):
        """A clip that reveals left to right between t0 and t1, shut again at t_off."""
        self._clips += 1
        cid = f"reveal{self._clips}"
        tr = Track(0)
        tr.hold(t0).at(t1, w, "lin").hold(t_off).cut(t_off, 0)
        self.defs.append(f'<clipPath id="{cid}"><rect x="{num(x)}" y="{num(y)}" height="{num(h)}" width="0">'
                         f'{animate("width", tr)}</rect></clipPath>')
        return f"url(#{cid})"

    # ----------------------------------------------------------- the AI orb
    def orb_type(self, t0, t1, t_out, msg, left=False):
        """A chat bubble next to the orb that types `msg` out between t0 and t1."""
        ox, oy = self.orb.pos.value(t0)
        w = measure(msg, 12) + 22
        x = ox - 18 - w if left else ox + 18
        clip = self.clip(11, -10, w - 18, 20, t0 + 0.15, t1, t_out + 0.3)
        inner = (ai_bubble(w, self.pal)
                 + f'<g clip-path="{clip}">' + text(msg, 11, 4.2, 12, self.pal["fg"]) + "</g>")
        s = self.sprite(inner, x=x, y=oy)
        s.pop_in(t0, 0.28)
        s.pop_out(t_out)
        return s

    def orb_think(self, t0, t1, label="generating", left=False):
        ox, oy = self.orb.pos.value(t0)
        w = measure(label, 11) + 50
        x = ox - 18 - w if left else ox + 18
        inner = (ai_bubble(w, self.pal) + text(label, 11, 3.8, 11, self.pal["muted"], italic=True)
                 + f'<g transform="translate({num(w - 28)} 0)">{dots(self.pal)}</g>')
        s = self.sprite(inner, x=x, y=oy)
        s.pop_in(t0, 0.25)
        s.pop_out(t1)
        return s

    def orb_pulse(self, t, k=1.35):
        self.orb.scale.hold(t).at(t + 0.12, (k, k), "out").at(t + 0.35, (1, 1), "io")
        return t + 0.35

    def stream(self, t0, step, tokens, x, y, size, color, weight=None):
        """Tokens appear one after another like a streamed reply. Returns (sprites, x_end, t_end)."""
        out, t = [], t0
        for tok in tokens:
            lead = measure(tok[:len(tok) - len(tok.lstrip())], size, bool(weight))
            s = self.sprite(text(tok.strip(), x + lead, y, size, color, weight=weight))
            s.show(t)
            out.append(s)
            x += measure(tok, size, bool(weight))
            t += step
        return out, x, t

    # ----------------------------------------------------------- render
    def render(self):
        p = self.pal
        hello = "".join(w.render() for w in self.page.h1[:-1])
        letters = "".join(lt.render(p, 2.6, 1.2 + i * 0.37) for i, lt in enumerate(self.letters))
        others = "".join(a.render(p, 2.3 + (i % 3) * 0.4, 0.8 + i * 0.29)
                         for i, a in enumerate(self.ninjas + self.minions))
        emoji = (f'<g>{animate_transform("rotate", self.wave)}'
                 f'<text x="{num(self.page.emoji_x)}" y="{H1_Y}" font-size="{H1_SIZE * 0.9:g}">\U0001F44B</text></g>')
        layers = [
            f'<rect width="{W}" height="{H}" fill="{p["bg"]}"/>',
            f'<rect x="0" y="{RULE_Y}" width="{W}" height="1" fill="{p["rule"]}"/>',
            "".join(s.render() for s in self.sky), "".join(s.render() for s in self.back),
            f'<g fill="{p["fg"]}">{hello}{self.page.render_paras()}</g>', emoji, letters, others,
            "".join(s.render() for s in self.front), self.orb.render(),
        ]
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
                f'font-family="{FONT_STACK}"><defs>{"".join(self.defs)}</defs>{"".join(layers)}</svg>\n')


__all__ = ["Stage", "W", "H", "FLOOR", "T"]
