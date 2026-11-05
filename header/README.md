# The header

`header-light.svg` and `header-dark.svg` are 31-second animated SVGs that look like a plain README at first.
An orange AI sparkle types "wake up my name, please", the letters of "Tanmay" open their eyes and go off to play, its spark minions help (badly), and two ninjas duel on the rooftops nearby.
Everything is SMIL: no JavaScript, no CSS, no web fonts, so GitHub's image proxy shows it as-is.

Regenerate after any change (Python 3, no dependencies):

```
python3 header/make_header.py
```

`python3 header/make_header.py --check` fails if the committed SVGs are out of date, and CI runs it on every push.

| File | What lives there |
| --- | --- |
| `page.py` | The README copy (`H1_TEXT`, `PARAS`) and the word-by-word layout |
| `story.py` | The letters' story: wake up, badminton, rain, flowers, goodbye |
| `ninjas.py` | The rooftop duel |
| `minions.py` | The spark minions' gags |
| `layout.py` | Where everything happens, shared by the three casts |
| `actor.py` | The shared motion base, the letters and the minions |
| `ninja.py` | The ninja and its poses |
| `stage.py` | The stage, the orb's chat bubbles, speech bubbles and other shared effects |
| `props.py` | Shapes: orb, shuttle, crate, rooftops, shuriken, cloud, rain, umbrella, flowers |
| `smil.py` | Keyframe tracks and the SMIL markup that plays them |
| `metrics.py` | Arial / Liberation Sans glyph widths, so every word gets a fixed `textLength` |

The intro lines in `PARAS` can change freely; the story only uses the letters of the name.
The ninjas are original characters, not anyone's from an existing series.
