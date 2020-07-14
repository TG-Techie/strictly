from typing import *
from strictly import *

Number = Union[int, float]

class Point():

    # a native python feature for sctricter classes
    __slots__ = ('x', 'y')

    # decoate methods to make them strictly typed, including '__init__'
    @strictly
    def __init__(self, x: Number, y: Number):
        # b/c this is a method the self argument is not annotated
        # neither is the return type
        self.x = float(x)
        self.y = float(y)

    @classmethod
    @strictly # decorate functions with strictly before any other decorators
    def from_tuple(cls: type, coords: Union[List[Number], Tuple[Number]]) -> Union['Point']:
        assert len(coords) == 2, f"a Point cannot be made from a list or tuple of length {len(coord)}, must be 2 long"
        return cls(*coords)

# you can use any class in type hints, see the 'point_to_scale' argument
@strictly
def scale_point(point_to_scale: Point, factor: Number) -> None:
    """
    An external function to scale a point around the origin for testing purposes.
    """
    point_to_scale.x *= factor
    point_to_scale.y *= factor

treasure_location = Point(42, 1701)

# lets test it to make sure, we should see four numbers in the ouput
print('before', treasure_location.x, treasure_location.y)
scale_point(treasure_location, 3.14)
scale_point(treasure_location, 3)
print('after', treasure_location.x, treasure_location.y)

# now lets cause an error
scale_point([1, 5], 7) # TypingError
