"""The letters' story, one function per scene. Times are seconds on the 31 s loop.

 1.0  An orange AI sparkle types: "wake up my name, please".
 2.8  "Tanmay" shimmers and the letters open their eyes.
 5.0  They hop down. The minions bring a shuttle; T and y rally.
      T's wild shot flies into the ninja fight; the red ninja catches it,
      bows and flicks it back. y smashes, T dives. "Nice shot!"
13.2  They politely ask for sunshine. The orb makes rain. T opens up into an
      umbrella over everyone. "Oops, sorry! Regenerating..."
19.9  Sun. The rain was good for something: flowers bloom.
22.0  Everyone hops home. y is still staring at the flowers, runs late: "Sorry!"
25.4  The orb streams the goodbye, the letters bow, the eyes close.
"""
from layout import (COURT, HUDDLE, CANOPY_W, RED_HOME, ORB_COURT, ORB_SKY, CLOUD, RAIN, SUN)
from metrics import measure
from props import shuttle, cloud, rain, sun, umbrella, stem, bloom
from stage import FLOOR

HIT_T, HIT_Y = (COURT["T"] + 7, FLOOR - 36), (COURT["y"] - 6, FLOOR - 36)
CATCH_AT = (RED_HOME[0] - 6.5, RED_HOME[1] - 21)
FLOWERS = ((482, 13), (521, 17), (573, 12), (618, 19), (652, 14), (703, 18), (742, 12), (780, 16), (815, 14))
TALL = 7


def opening_wave(st):
    _wave(st, 0.3)


def wake(st):
    p = st.pal
    L = st.letters
    st.orb.pop_in(1.0, 0.4)
    st.sparkle(1.1, 314, 10, 4, color=p["ai2"])
    st.orb_type(1.35, 2.55, 3.7, "wake up my name, please ✨")
    st.orb_pulse(2.75)
    for i, lt in enumerate(L):
        t = 2.85 + i * 0.09
        lt.fill.hold(t).at(t + 0.16, p["ai1"], "io").at(t + 0.32, p["ai2"], "io").at(t + 0.55, p["fg"], "io")
    for i, (sx, sy) in enumerate(((112, 4), (168, 0), (218, 8))):
        st.sparkle(3.0 + i * 0.15, sx, sy, 5, color=p["ai2"])
    for i, lt in enumerate(L):
        t = 3.6 + i * 0.07
        lt.awake.hold(t).at(t + 0.12, 1, "out")
        lt.bounce(t, 0.6)
        lt.peek(4.0 + i * 0.03, -1.2, 0).peek(4.4, 1.2, 0).peek(4.75, 0, 0)
    y = L[5]
    y.stretch(4.35, 1.0, 0.55)
    st.float_text(4.4, y.home[0] + 2, 12, "*yawn*", size=9, rise=6)


def badminton(st):
    p = st.pal
    T_, a1, n, m, a2, y = st.letters
    spectators = (a1, n, m, a2)
    T_.hop(5.0, COURT["T"], FLOOR, dur=0.8, h=8)
    for i, lt in enumerate(spectators):
        lt.hop(5.12 + i * 0.12, COURT["spectators"][i], FLOOR, dur=0.7, h=8)
    y.hop(5.6, COURT["y"], FLOOR, dur=0.85, h=8)
    st.puff(5.8, COURT["T"], FLOOR, 0.6)
    st.puff(6.45, COURT["y"], FLOOR, 0.6)
    st.orb.go(5.3, 6.0, *ORB_COURT, "io")
    st.say_letter(T_, 6.3, 7.2, "Shuttle, please?")
    st.orb_think(6.45, 7.1)

    sh = st.sprite(shuttle(p), x=480, y=FLOOR - 18)
    sh.pop_in(7.75, 0.2)
    sh.arc(7.75, 8.05, *HIT_T, h=14)
    rally = [(8.1, HIT_Y, 70, -1), (8.75, HIT_T, 70, 1)]
    for t0, (x, yy), h, side in rally:
        hitter = T_ if side < 0 else y
        hitter.tilt(t0 - 0.1, t0, 14 * -side, "out").tilt(t0, t0 + 0.25, 0, "io")
        hitter.bounce(t0 - 0.02, 0.6)
        sh.rot.hold(t0).at(t0 + 0.05, 70 * side, "out").at(t0 + 0.6, 110 * side, "io")
        sh.arc(t0, t0 + 0.62, x, yy, h=h)
        for lt in spectators:
            lt.peek(t0, -1.2 * side, -0.4)

    wild = 9.4
    T_.tilt(wild - 0.1, wild, -16, "out").tilt(wild, wild + 0.3, 0, "io")
    T_.bounce(wild - 0.02, 0.8)
    sh.rot.hold(wild).at(wild + 0.05, -40, "out")
    sh.arc(wild, 9.85, *CATCH_AT, h=40)
    st.float_text(9.5, COURT["T"] - 6, FLOOR - 40, "Oops!", size=11, weight="600")
    for lt in spectators + (T_, y):
        lt.peek(9.45, 1.2, -1.2)
    sh.rot.hold(10.15).at(10.2, 180, "out")
    sh.arc(10.15, 10.6, *HIT_Y, h=10)
    for lt in spectators:
        lt.peek(10.2, 1.2, 0.2)

    smash = 10.6
    y.tilt(smash - 0.1, smash, 18, "out").tilt(smash, smash + 0.3, 0, "io")
    y.bounce(smash - 0.02, 1.0)
    sh.rot.hold(smash).at(smash + 0.05, 60, "snap")
    sh.go(smash, smash + 0.22, COURT["T"] - 38, FLOOR - 2, "in")
    sh.rot.at(smash + 0.3, 80, "out")
    T_.x.hold(10.62).at(10.8, COURT["T"] - 12, "out")
    T_.tilt(10.62, 10.8, -58, "out").tilt(11.1, 11.4, 0, "io")
    T_.x.hold(11.1).at(11.4, COURT["T"], "io")
    for i, lt in enumerate(spectators):
        lt.peek(smash, 1.2, 0.6)
        lt.bounce(10.9 + i * 0.06, 0.9)
    st.float_text(10.92, 360, FLOOR - 32, "Ooh!", size=12, weight="600")
    st.say_letter(T_, 11.5, 12.4, "Nice shot!")
    y.bow(11.9, 0.3)
    st.say(11.95, 12.9, "Thank you!", COURT["y"], FLOOR - 24, tail_dx=-14)
    sh.fade(11.8, 12.1, 0)


def weather(st):
    p = st.pal
    T_, a1, n, m, a2, y = st.letters
    under = (a1, n, m, a2, y)
    order = (a1, n, m, a2, T_, y)
    slots = (HUDDLE[0], HUDDLE[1], HUDDLE[3], HUDDLE[4], HUDDLE[2], HUDDLE[5])
    for i, (lt, x) in enumerate(zip(order, slots)):
        lt.hop(13.2 + i * 0.07, x, FLOOR, dur=0.6, h=12)
        lt.peek(14.0, 0, -1)
    st.orb.go(13.0, 13.6, *ORB_SKY, "io")
    st.say_letter(m, 14.2, 15.3, "Could we have some sunshine?")
    st.orb_think(15.35, 16.1, left=True)
    st.orb_pulse(16.1)
    cl = st.sprite(f'<g transform="scale(1.25)">{cloud(p)}</g>', x=CLOUD[0], y=CLOUD[1])
    cl.pop_in(16.15, 0.35)
    wet = st.sprite(rain(p, *RAIN, n=34), layer="back")
    wet.fade(16.35, 16.5, 1).hide(17.3)
    for lt in under:
        lt.shiver(16.5, 17.1)
        lt.peek(16.5, 0, 0.8)
    st.float_text(16.6, 548, FLOOR - 30, "Brr!", size=12, weight="600")

    cx = HUDDLE[2]
    T_.alpha.cut(17.2, 0)
    eyes = "".join(f'<circle cx="{x}" cy="-64" r="3.4" fill="#ffffff" stroke="{p["pupil"]}" stroke-width=".8"/>'
                   f'<circle cx="{x}" cy="-63" r="1.7" fill="{p["pupil"]}"/>' for x in (-8, 8))
    um = st.sprite(umbrella(p, CANOPY_W) + eyes, x=cx, y=FLOOR)
    um.alpha.cut(17.2, 1)
    um.scale.cut(17.2, (0.1, 1)).at(17.4, (1.08, 1), "out").at(17.52, (1, 1), "io")
    um.scale.hold(20.3).at(20.5, (0.1, 1), "in")
    um.alpha.cut(20.5, 0)
    half = CANOPY_W / 2 - 2
    st.defs.append('<clipPath id="dry"><path clip-rule="evenodd" '
                   f'd="M0 0H830V290H0Z M{cx - half} {FLOOR - 48}H{cx + half}V290H{cx - half}Z"/></clipPath>')
    dry = st.sprite(f'<g clip-path="url(#dry)">{rain(p, *RAIN, n=34, seed=0.31)}</g>', layer="back")
    dry.show(17.3).fade(19.8, 19.95, 0)
    for lt in under:
        lt.peek(17.4, 0, -1.1)
    st.float_text(17.5, 455, FLOOR - 28, "Phew!", size=12, weight="600")

    st.orb_type(18.6, 19.5, 20.0, "Oops, sorry! That's rain. Regenerating…", left=True)
    st.orb_pulse(19.6)
    for i, (sx, sy) in enumerate(((630, 44), (690, 38), (662, 64))):
        st.sparkle(19.65 + i * 0.08, sx, sy, 6, color=p["ai2"])
    cl.pop_out(19.8, 0.25)
    sn = st.sprite(sun(p), layer="sky", x=SUN[0], y=SUN[1])
    sn.pop_in(19.95, 0.4)
    sn.fade(24.6, 25.1, 0)

    st.flowers = []
    colors = (p["petal1"], p["petal2"], p["petal3"], p["petal4"])
    for i, (fx, fh) in enumerate(FLOWERS):
        t = 20.1 + i * 0.08
        s = st.sprite(stem(p, fh), layer="back", x=fx, y=FLOOR)
        s.alpha.cut(t, 1)
        s.scale.cut(t, (1, 0.05)).at(t + 0.3, (1, 1), "out")
        b = st.sprite(bloom(colors[i % 4]), layer="back", x=fx, y=FLOOR - fh)
        b.pop_in(t + 0.28, 0.3, 1.3)
        st.flowers.append((s, b, fh))

    T_.alpha.cut(20.5, 1)
    T_.bounce(20.52, 0.8)
    for i, lt in enumerate(under):
        t = 20.7 + i * 0.09
        lt.bounce(t, 1.0)
        lt.wiggle(t + 0.3, n=3, amp=9, step=0.09)
    st.float_text(20.8, 700, FLOOR - 34, "Yay!", size=12, weight="600")


def home(st):
    T_, a1, n, m, a2, y = st.letters
    for i, lt in enumerate((T_, a1, n, m, a2)):
        lt.hop(22.0 + i * 0.15, *lt.home, dur=0.85, h=6)
        lt.peek(21.9 + i * 0.15, 0, 0)
    y.peek(22.0, 1.2, 0.6)
    st.bang(23.1, y.last[0], FLOOR - 34)
    y.peek(23.15, -1.3, 0)
    y.hop(23.35, 420, FLOOR, dur=0.45, h=18, land="chain")
    te = y.hop(23.92, *y.home, dur=0.7, h=6)
    a2.sq.hold(te - 0.05).at(te + 0.05, (0.86, 1.08), "out").at(te + 0.3, (1, 1), "io")
    m.bounce(te + 0.05, 0.5)
    y.peek(te + 0.1, 0, 0)
    y.bow(te + 0.12, 0.3)
    st.say(te + 0.15, te + 1.1, "Sorry!", y.home[0] + 4, y.home[1] + 6, tail_dx=14, below=True)


def goodbye(st):
    p = st.pal
    st.orb.go(24.8, 25.3, 506, 220, "io")
    t0, step = 25.4, 0.13
    toks1 = ["Thanks", " for", " stopping", " by!"]
    toks2 = ["Have", " a", " lovely", " day"]
    line1, x1, t1 = st.stream(t0, step, toks1, 530, 226, 20, p["fg"], "600")
    line2, x2, t2 = st.stream(t1 + 0.05, step, toks2, 530, 252, 15, p["muted"])
    st.dot_target = (x2, 252)
    st.goodbye_lines = line1 + line2
    cursor = st.sprite('<rect x="1" y="-14" width="2.4" height="17" rx="1" fill="url(#ai)"/>', x=530, y=226)
    cursor.show(t0)
    x, t = 530, t0
    for tok in toks1:
        x += measure(tok, 20, True)
        cursor.pos.cut(t, (x, 226))
        t += step
    x = 530
    for tok in toks2:
        x += measure(tok, 15)
        cursor.pos.cut(t + 0.05, (x + 4, 250))
        t += step
    t = t2
    while t < 27.2:
        cursor.alpha.cut(t, 0).cut(t + 0.25, 1)
        t += 0.5
    cursor.hide(27.25)
    st.sparkle(27.4, x1 + 8, 210, 6, color=p["ai2"])
    for s in st.goodbye_lines:
        s.fade(28.2, 28.5, 0)
    for i, lt in enumerate(st.letters):
        lt.bow(26.0 + i * 0.12, 0.2)
    _wave(st, 26.1)
    st.orb_pulse(28.2, 1.2)
    st.orb.pop_out(28.6, 0.3)
    for i, lt in enumerate(st.letters):
        t = 29.2 + i * 0.05
        lt.awake.hold(t).at(t + 0.25, 0, "io")


def curtain(st):
    for s, b, _ in st.flowers:
        s.fade(24.8, 25.2, 0)
        b.fade(24.8, 25.2, 0)


def _wave(st, t0):
    w = st.wave
    _, px, py = w.v
    w.hold(t0)
    for i, a in enumerate((18, -8, 16, -6, 12, 0)):
        w.at(t0 + 0.16 * (i + 1), (a, px, py), "io")


SCENES = [opening_wave, wake, badminton, weather, home, goodbye]
