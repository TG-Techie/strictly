from strictly import *

class Scene():
    # any function (including methods) can by strictly typed
    @strictly
    def __init__(self, number: int):
        # b/c this is a method the self argument is not annotated
        # neither is the return type
        self.number = number

# Use any class in annotations
@strictly
def narrate(scene: Scene):
    print(f"on to scene {scene.number}, which is a smashing scene with some"\
        +" lovely acting, in which Arthur discovers a vital clue.")

# let's test with good inputs
the_scene = Scene(24)
narrate(the_scene)
# now let's add some bad inputs
the_scene = Scene('not a number') # 1st TypingError
narrate('nothing') # 2nd TypingError
