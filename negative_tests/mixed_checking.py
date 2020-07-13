from strictly import *

@strictly
def foo(unchecked, checked: int) -> int:
    return unchecked+checked

# this will be fine
foo(1, 2)

# foo only allows ints to be returned
foo(3.0, 4)
# if returning 'float's is desired functionality the return annotation should
#   be from the typing module, EX: `Union[int, float]`

# this will not work b/c `str`s and 'int's cannot be added together
foo('5', 6)
# this type error was not by strictly b/c the argument was not annotated
