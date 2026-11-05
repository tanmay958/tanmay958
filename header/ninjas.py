"""The ninja duel on the rooftops. Polite, but very fast.

 5.9  Two ninjas land on the roofs and bow.
 8.0  Hand signs, shadow clones, a mid-air clash.
 9.4  T's wild shot flies in. The clones vanish, the red ninja catches the
      shuttle between two fingers, nods, and flicks it back.
11.4  Shuriken, deflected. A giant one; red vanishes in smoke and reappears.
16.4  The rain reaches the roofs. "Mind if we join?" Under the umbrella they go.
21.4  Back up. One last friendly clash, a bow, and at the goodbye: smoke.
"""
from layout import ROOFS, ROOF_Y, BLUE_HOME, RED_HOME, CLASH
from ninja import Ninja
from props import rooftops, shuriken, ring
from stage import FLOOR


def setup(st):
    p = st.pal
    st.blue = Ninja(*BLUE_HOME, p["scarf_blue"], face=1)
    st.red = Ninja(*RED_HOME, p["scarf_red"], face=-1)
    st.clones = [Ninja(608, ROOF_Y, p["scarf_blue"], 1), Ninja(660, ROOF_Y, p["scarf_blue"], 1),
                 Ninja(780, ROOF_Y, p["scarf_red"], -1), Ninja(824, ROOF_Y, p["scarf_red"], -1)]
    st.ninjas.extend([st.blue, st.red] + st.clones)
    roofs = st.sprite(rooftops(p, ROOFS, ROOF_Y), layer="sky")
    roofs.fade(5.2, 5.8, 1).fade(28.4, 29.0, 0)


def arrive(st):
    b, r = st.blue, st.red
    for nj, (x, y) in ((b, BLUE_HOME), (r, RED_HOME)):
        st.puff(5.9, x, y - 6, 0.7)
        nj.appear(6.0)
        nj.bounce(6.0, 0.8)
        nj.bow(6.35, 0.15)


def clones(st):
    b, r = st.blue, st.red
    for nj in (b, r):
        nj.pose(8.0, "sign")
        st.sparkle(8.1, nj.x.v + 4 * nj.face, ROOF_Y - 12, 4)
        nj.pose(8.35, "idle")
    for c in st.clones:
        st.puff(8.35, c.x.v, ROOF_Y - 6, 0.6)
        c.appear(8.4)
    pairs = [(b, r, CLASH), (st.clones[0], st.clones[2], (CLASH[0] - 14, CLASH[1] + 16)),
             (st.clones[1], st.clones[3], (CLASH[0] + 14, CLASH[1] - 12))]
    for left, right, (cx, cy) in pairs:
        for nj, side in ((left, -1), (right, 1)):
            home = nj.last
            nj.pose(8.5, "throw")
            nj.fly(8.55, 8.88, cx + 7 * side, cy + 10, "in")
            nj.bounce(8.88, 1.0)
            nj.pose(8.95, "idle")
            nj.hop(9.3, *home, dur=0.38, h=10, lean=0, land=False)
        st.sparkle(8.9, cx, cy - 2, 9)
        rg = st.sprite(ring(st.pal), x=cx, y=cy - 2)
        rg.show(8.9).fade(8.9, 9.2, 0)
        rg.scale.cut(8.9, (0.3, 0.3)).at(9.2, (1.6, 1.6), "out")
    for c in st.clones:
        st.puff(9.5, c.x.v, ROOF_Y - 6, 0.6)
        c.vanish(9.55)


def catch(st):
    r = st.red
    r.peek(9.45, -1, 0.8)
    r.pose(9.8, "catch")
    r.sq.hold(9.9).at(9.98, (1.06, 0.86), "out").at(10.1, (1, 1), "io")
    r.pose(10.12, "throw")
    r.pose(10.4, "idle")
    st.blue.peek(9.6, 1, 0)


def shurikens(st):
    p = st.pal
    b, r = st.blue, st.red
    star1 = st.sprite(shuriken(p), x=BLUE_HOME[0] + 9, y=ROOF_Y - 15)
    b.pose(11.35, "throw").pose(11.6, "idle")
    star1.show(11.4).go(11.4, 11.75, RED_HOME[0] - 6, ROOF_Y - 14, "lin")
    r.pose(11.68, "throw").pose(11.9, "idle")
    st.sparkle(11.75, RED_HOME[0] - 7, ROOF_Y - 14, 5)
    star1.go(11.76, 12.05, RED_HOME[0] - 18, ROOF_Y + 30, "in").fade(11.9, 12.05, 0)

    star2 = st.sprite(shuriken(p), x=RED_HOME[0] - 9, y=ROOF_Y - 15)
    r.pose(11.95, "throw").pose(12.2, "idle")
    star2.show(12.0).go(12.0, 12.33, BLUE_HOME[0] + 7, ROOF_Y - 14, "lin")
    b.pose(12.28, "throw").pose(12.45, "idle")
    st.sparkle(12.33, BLUE_HOME[0] + 8, ROOF_Y - 14, 5)
    star2.go(12.34, 12.6, BLUE_HOME[0] + 20, ROOF_Y + 30, "in").fade(12.45, 12.6, 0)

    giant = st.sprite(shuriken(p, 11), x=BLUE_HOME[0] + 12, y=ROOF_Y - 16)
    b.pose(12.5, "throw").pose(12.75, "idle")
    giant.show(12.55).go(12.55, 12.95, RED_HOME[0], ROOF_Y - 14, "lin")
    st.puff(12.86, RED_HOME[0], ROOF_Y - 8, 0.8)
    r.vanish(12.9)
    r.x.cut(13.0, 725)
    giant.arc(12.96, 13.42, BLUE_HOME[0] + 8, ROOF_Y - 16, h=22)
    giant.hide(13.42)
    b.pose(13.4, "catch").pose(13.7, "idle")
    b.bounce(13.42, 0.7)
    st.puff(13.3, 725, ROOF_Y - 8, 0.7)
    r.appear(13.35)
    st.say(13.5, 14.35, "Close one!", 725, ROOF_Y - 31, tail_dx=-6)
    b.bow(13.8, 0.1)


def shelter(st):
    b, r = st.blue, st.red
    for nj in (b, r):
        nj.peek(16.4, 0, -1)
        nj.shiver(16.5, 16.9, 1.0)
    b.hop(16.95, 760, FLOOR, dur=0.55, h=10)
    r.hop(17.05, 785, FLOOR, dur=0.5, h=10)
    b.turn(17.55, -1)
    r.turn(17.55, -1)
    b.peek(17.55, 0, 0)
    r.peek(17.55, 0, 0)
    st.say(17.6, 18.5, "Mind if we join?", 760, FLOOR - 31, tail_dx=-10)
    b.hop(18.4, 708, FLOOR, dur=0.35, h=6)
    r.hop(18.5, 719, FLOOR, dur=0.35, h=6)
    b.peek(18.8, 0, -1)
    r.peek(18.8, 0, -1)


def farewell(st):
    b, r = st.blue, st.red
    b.turn(20.7, 1)
    b.peek(20.7, 0, 0)
    r.peek(20.7, 0, 0)
    b.bow(20.75, 0.1)
    r.bow(20.8, 0.1)
    b.hop(21.5, *BLUE_HOME, dur=0.55, h=20)
    r.hop(21.6, *RED_HOME, dur=0.55, h=20)
    for nj, side in ((b, -1), (r, 1)):
        home = nj.last
        nj.pose(22.35, "throw")
        nj.fly(22.4, 22.7, CLASH[0] + 7 * side, CLASH[1] + 10, "in")
        nj.bounce(22.7, 1.0)
        nj.pose(22.75, "idle")
        nj.hop(23.05, *home, dur=0.4, h=10, lean=0, land=False)
    st.sparkle(22.72, CLASH[0], CLASH[1] - 2, 12)
    rg = st.sprite(ring(st.pal, 14), x=CLASH[0], y=CLASH[1] - 2)
    rg.show(22.72).fade(22.72, 23.1, 0)
    rg.scale.cut(22.72, (0.3, 0.3)).at(23.1, (1.8, 1.8), "out")
    b.bow(23.55, 0.15)
    r.bow(23.6, 0.15)
    b.bow(26.3, 0.15)
    r.bow(26.35, 0.15)
    for nj, (x, y) in ((b, BLUE_HOME), (r, RED_HOME)):
        st.puff(27.55, x, y - 6, 0.8)
        nj.vanish(27.6)


SCENES = [setup, arrive, clones, catch, shurikens, shelter, farewell]
