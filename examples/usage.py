from strictly import *

# lets make a strict function
@strictly
def some_strictly_typed_func(
    x, # an unannotated function will not be strictly typed
    y : int, # this will now onyl be able to take and int
    z : Union[float, int], # you can use unions from the typing module to allow more than one type
    q : int = 9, # it even works on default and keyword only arguments
) -> Union[(float, int)]:
    return x + y + z + q

# then call it

# these will work
some_strictly_typed_func(1, 2, 3, 4)
some_strictly_typed_func(1, 2, 7.0, q=4)

# this will fail
some_strictly_typed_func(1, '2', 3, 4) # comment this line out to test the one below

# but will pass the arg b/c we didn't annotate
# but it will fail because you cannot add 'str's to 'int's
some_strictly_typed_func('1', 2, 3, 4)
