"""Puts the stage and every cast's scenes together for one palette."""
import minions
import ninjas
import story
from stage import Stage


def build(pal):
    st = Stage(pal)
    for scene in story.SCENES + ninjas.SCENES + minions.SCENES + [story.curtain]:
        scene(st)
    return st.render()
