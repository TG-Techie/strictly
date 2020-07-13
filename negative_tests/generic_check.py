from typing import *
from strictly import *

@strictly
def find_max(nums : List[int]) -> int:
    return max(nums)
# will work, strictly check that the input is a list
find_max([7, 2, 5, 9, 3])
# however, it will not check the the objects in the list
find_max([7, 2, 5, 9, '9000'])
