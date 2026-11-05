"""The README text, laid out word by word with fixed widths."""
import html

from metrics import measure
from smil import Track, opacity_attr, wrap, num

FONT_STACK = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
X0 = 1
H1_Y, RULE_Y = 33, 50.5
P_Y = [84, 124, 164]
SIZE, H1_SIZE = 16, 32

H1_TEXT = "Hi, I'm Tanmay"
PARAS = [
    "Software Engineer @ UiPath. MCA from NIT Trichy, class of 2025.",
    "I build backend systems that scale and still behave at 3 a.m.",
    "Off the clock: chess, badminton, and one more cup of coffee.",
]


class Word:
    def __init__(self, text, x, y, size, bold=False):
        self.text, self.x, self.y, self.size, self.bold = text, x, y, size, bold
        self.w = measure(text, size, bold)
        self.move = Track((0, 0))
        self.scale = Track((1, 1))
        self.rot = Track(0)
        self.alpha = Track(1)

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y - self.size * 0.34

    def _text(self, x, y):
        weight = ' font-weight="600"' if self.bold else ""
        return (f'<text x="{num(x)}" y="{num(y)}" font-size="{self.size}"{weight} '
                f'textLength="{num(self.w)}" lengthAdjust="spacingAndGlyphs">{html.escape(self.text)}</text>')

    def render(self):
        tracks = (self.move, self.scale, self.rot, self.alpha)
        if all(t.constant() for t in tracks):
            return self._text(self.x, self.y)
        a_attr, a_anim = opacity_attr(self.alpha)
        inner = self._text(-self.w / 2, self.y - self.cy)
        body = wrap(inner, ("scale", self.scale), ("rotate", self.rot))
        body = f'<g transform="translate({num(self.cx)} {num(self.cy)})">{body}</g>'
        return f"<g{a_attr}>{a_anim}{wrap(body, ('translate', self.move))}</g>"


class Page:
    def __init__(self):
        self.lines = []
        self.h1 = self._line(H1_TEXT, H1_Y, H1_SIZE, True)
        for text, y in zip(PARAS, P_Y):
            self._line(text, y, SIZE, False)
        self.emoji_x = X0 + sum(w.w for w in self.h1) + measure(" ", H1_SIZE, True) * (len(self.h1) - 1) + 8

    def _line(self, text, y, size, bold):
        words, x = [], X0
        space = measure(" ", size, bold)
        for token in text.split(" "):
            word = Word(token, x, y, size, bold)
            words.append(word)
            x += word.w + space
        self.lines.append(words)
        return words

    def word(self, text, line=None):
        lines = self.lines if line is None else [self.lines[line]]
        hits = [w for ln in lines for w in ln if w.text == text]
        if len(hits) != 1:
            raise KeyError(f"{text!r} matched {len(hits)} words")
        return hits[0]

    def render_paras(self):
        return "".join(w.render() for ln in self.lines[1:] for w in ln)
