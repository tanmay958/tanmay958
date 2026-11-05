"""The orb's spark minions. Helpful, mostly.

 6.4  Two bring the net and hammer it in; one hits its own foot. "Ow!"
 6.6  Three carry in a crate with the shuttle, then sit down with popcorn.
12.0  One copies a ninja hand sign, poofs itself and coughs.
16.5  In the rain three fly up and push the cloud. It does not budge.
      One falls, bounces off the umbrella: "Oof!". The other two hold leaves.
20.5  One waters a flower. It grows far too tall.
24.8  They line up under the goodbye. The last one runs in late with the full stop.
"""
from actor import Minion
from layout import COURT, WATCHERS, LEAF_SPOTS, CLOUD, HUDDLE
from props import crate, net, hammer, popcorn, leaf, watering_can
from stage import FLOOR
from story import FLOWERS, TALL

START_X = 852


def setup(st):
    st.mins = [Minion(START_X + i * 14, FLOOR) for i in range(5)]
    st.minions.extend(st.mins)


def net_crew(st):
    p = st.pal
    m3, m4 = st.mins[3], st.mins[4]
    spots = (COURT["net"] - 13, COURT["net"] + 13)
    for mn, x in zip((m3, m4), spots):
        mn.appear(6.3)
        mn.walk(6.35, 6.9, x, step=0.11)
    nt = st.sprite(net(p), layer="back", x=COURT["net"], y=FLOOR)
    nt.pop_in(6.95, 0.3)
    nt.pop_out(12.9)
    for i, (mn, x) in enumerate(zip((m3, m4), spots)):
        hm = st.sprite(hammer(p), x=x + (5 if i else -5), y=FLOOR - 6)
        hm.alpha.cut(7.0, 1)
        t = 7.0 + i * 0.08
        for _ in range(3):
            hm.rot.hold(t).at(t + 0.08, -50 if i else 50, "out").at(t + 0.16, 0, "in")
            t += 0.17
        hm.pop_out(7.75)
        mn.pose(7.0, "push").pose(7.7, "down")
    st.float_text(7.55, spots[1], FLOOR - 24, "Ow!", size=11, color=st.pal["red"], weight="700")
    m4.hop(7.55, spots[1], FLOOR, dur=0.25, h=6)
    m4.shiver(7.85, 8.2, 1.0)
    m3.peek(7.6, 1.2, 0)
    for mn, x in zip((m3, m4), LEAF_SPOTS):
        mn.walk(8.3, 8.9, x, step=0.12)
        mn.peek(9.0, -1.2, 0)


def crate_crew(st):
    p = st.pal
    m0, m1, m2 = st.mins[:3]
    drop = (466, 480, 494)
    box = st.sprite(crate(p), x=START_X + 14, y=FLOOR - 16)
    box.alpha.cut(6.55, 1)
    for mn, x in zip((m0, m1, m2), drop):
        mn.appear(6.55)
        mn.pose(6.55, "up")
        mn.walk(6.6, 7.55, x, step=0.12)
    box.go(6.6, 7.55, drop[1], FLOOR - 16, "lin")
    box.go(7.58, 7.68, drop[1], FLOOR, "in")
    st.puff(7.68, drop[1], FLOOR, 0.7)
    box.pop_out(7.8)
    for mn, x in zip((m0, m1, m2), WATCHERS):
        mn.pose(7.6, "down")
        mn.walk(7.9, 8.6, x, step=0.12)
        mn.peek(8.7, 1.2, 0)
    tub = st.sprite(popcorn(p), x=WATCHERS[1] + 7, y=FLOOR - 3)
    tub.pop_in(8.7, 0.25)
    tub.pop_out(16.3)
    for i, t in enumerate((9.6, 10.9, 11.6)):
        st.mins[i % 3].bounce(t, 0.6)


def copycat(st):
    m2 = st.mins[2]
    m2.peek(11.5, 1.2, -1)
    m2.pose(12.0, "up")
    st.sparkle(12.1, m2.x.v, FLOOR - 22, 4)
    st.puff(12.3, m2.x.v, FLOOR - 6, 0.9)
    m2.pose(12.35, "down")
    m2.shiver(12.5, 12.85, 1.2)
    st.float_text(12.5, m2.x.v + 6, FLOOR - 26, "*cough*", size=10)
    m2.close_eyes(12.4, 12.85)


def rain_gags(st):
    p = st.pal
    m0, m1, m2, m3, m4 = st.mins
    left = CLOUD[0] - 70
    for i, (mn, dy) in enumerate(((m0, -8), (m1, 6), (m2, 20))):
        t = 16.45 + i * 0.07
        mn.peek(t, 0, -1)
        mn.pose(t, "push")
        mn.fly(t + 0.05, t + 0.55, left + i * 3, CLOUD[1] + dy + 18)
        mn.tilt(t + 0.6, t + 0.75, 22, "out")
        mn.shiver(t + 0.8, 17.6, 0.8, 0.06)
        mn.close_eyes(t + 0.8, 17.6)
    st.float_text(17.2, left - 4, CLOUD[1] + 4, "hnnngh", size=10)
    canopy = (HUDDLE[2] - 20, FLOOR - 86)
    m1.tilt(17.7, 17.9, 200, "in")
    m1.fly(17.7, 17.95, *canopy, "in")
    m1.tilt(17.95, 18.35, 360, "out")
    m1.rot.cut(18.36, (0, 0, m1.pivot))
    m1.x.hold(17.95).at(18.35, 470, "lin")
    m1.y.hold(17.95).at(18.12, (0, FLOOR - 120), "out").at(18.35, (0, FLOOR), "in")
    m1.bounce(18.36, 1.2)
    st.float_text(18.4, 452, FLOOR - 24, "Oof!", size=11, weight="700")
    m1.pose(18.4, "down")
    m1.walk(18.6, 18.85, 486, step=0.12)
    for mn, x, t in ((m0, 500, 17.75), (m2, 514, 17.85)):
        mn.tilt(t, t + 0.15, 0)
        mn.pose(t, "down")
        mn.fly(t + 0.05, t + 0.5, x, FLOOR, "in")
        mn.peek(t + 0.6, 0, -1)
    for mn, x in zip((m3, m4), LEAF_SPOTS):
        lf = st.sprite(leaf(p), x=x, y=FLOOR - 24)
        lf.pop_in(16.45, 0.25)
        lf.fade(19.95, 20.2, 0)
        mn.pose(16.45, "up").pose(20.1, "down")
        mn.peek(16.6, 0, -1)


def watering(st):
    p = st.pal
    m3, m4 = st.mins[3], st.mins[4]
    fx, fh = FLOWERS[TALL]
    m3.walk(20.45, 20.7, fx - 14, step=0.12)
    m3.peek(20.7, 1.2, -0.5)
    can = st.sprite(watering_can(p), x=fx - 14, y=FLOOR - 9)
    can.pop_in(20.72, 0.22)
    can.rot.hold(20.8).at(20.95, 28, "io").hold(21.3).at(21.4, 0, "io")
    can.pop_out(21.55)
    stem, head, _ = st.flowers[TALL]
    k = 2.7
    stem.scale.hold(21.05).at(21.35, (1, k), "snap")
    head.go(21.05, 21.35, fx, FLOOR - fh * k, "snap")
    st.bang(21.4, fx - 14, FLOOR - 30)
    m3.peek(21.4, 0.6, -1.3)
    m4.peek(21.4, -0.8, -1.3)
    m4.bounce(21.5, 0.8)
    m4.bounce(21.85, 0.8)


def line_up(st):
    p = st.pal
    m0, m1, m2, m3, m4 = st.mins
    tx, ty = st.dot_target
    spots = (548, 582, 616, 690)
    for i, (mn, x) in enumerate(zip((m1, m0, m2, m3), spots)):
        mn.walk(24.8 + i * 0.05, 25.3 + i * 0.05, x, step=0.12)
        mn.pose(25.35, "up")
        mn.peek(25.4, 0, -1)
    m4.walk(24.8, 25.1, START_X, step=0.12)
    dot = st.sprite(f'<circle r="1.9" fill="{p["muted"]}"/>', x=START_X, y=FLOOR - 22)
    dot.alpha.cut(26.4, 1)
    m4.pose(26.4, "up")
    m4.walk(26.4, 27.0, tx, step=0.1)
    dot.go(26.4, 27.0, tx, FLOOR - 22, "lin")
    for mn in (m0, m1, m2, m3):
        mn.peek(26.5, 1.2, 0)
    m4.hop(27.1, tx, FLOOR, dur=0.3, h=8)
    dot.arc(27.1, 27.35, tx + 1, ty - 1, h=6)
    st.sparkle(27.36, tx + 2, ty - 6, 5)
    m4.pose(27.4, "down")
    m4.bow(27.7, 0.15)
    dot.fade(28.2, 28.5, 0)
    for i, mn in enumerate(st.mins):
        mn.pose(28.2, "down")
        x = mn.last[0]
        st.puff(28.4 + i * 0.05, x, FLOOR - 6, 0.5)
        mn.vanish(28.45 + i * 0.05)


SCENES = [setup, net_crew, crate_crew, copycat, rain_gags, watering, line_up]
