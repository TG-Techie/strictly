from typing import *
import typing as _typing
from functools import wraps # a wrapping tool that maintains sanitation.
from types import FunctionType

# the following flags are instance attributes on the 'strictly' function
#   disable : turns off type wrapping

# set what should be exported from the module
__all__ = ['strictly', 'TypingError', 'DeterminationError', 'NoneType']
__version__ = '1.1.2'

NoneType = type(None)

class DeterminationError(TypeError):
    pass

class TypingError(TypeError):
    def __init__(self,
            kind: str, # a description of the value like 'positional argument' or 'return'
            name: Union[str, None], # the name of the arg or kwarg, None if ther is no name
            func: FunctionType, # the function that was called
            arg, # the argument of the correct type
            type_tup: tuple, # the expected types
            ):
        if not len(type_tup):
            type_tup = (object,)

        expected_types = ', '.join([typ.__name__ for typ in type_tup])
        rxed_type_name = type(arg).__name__

        kind = f"{kind} "
        if len(name):
            name = f"'{name}' "
        elif name is None:
            name = ''

        repr_text = repr(arg)
        if len(repr_text) > 20:
            from_detail = f"at {id(arg)}"
        else:
            from_detail = f"from the value {repr_text}"


        _ = f"\ninvalid {kind}type in call of {repr(func.__name__)}, {func}\n"\
           +f"\t{kind}{name}must be of type <{expected_types}>\n"\
           +f"\tfound {kind}of type <{rxed_type_name}> {from_detail}"
        super().__init__(_# this line is from strictly
             )

def _tupleize_type(tp: Union[None, type, tuple, _typing._GenericAlias]) -> Tuple[type]:
    if tp is None: # type convention to use 'None' instead of 'NoneType'
        ret = type(None)
    elif isinstance(tp, type): # any individual type
        ret = (tp,)
    elif isinstance(tp, tuple): # allow for recursive call of _tupleize_type to flatten inputs
        tups = [_tupleize_type(teyep) for teyep in tp]
        ret = ()
        for tup in tups:
            ret += tup
    elif isinstance(tp, _typing._GenericAlias): # account for typing Generics
        if tp.__origin__ == Union:
            tups = [_tupleize_type(teyep) for teyep in tp.__args__]
            ret = ()
            for tup in tups:
                ret += tup
        elif hasattr(tp, '__origin__'):
            return (tp.__origin__,)
        else:
            raise DeterminationError(f"cannot determine what type to check {tp} against")
    else:
        raise DeterminationError(f"cannot determine what type to check {tp} against")
    return ret

def strictly(func: FunctionType) -> FunctionType:
    """
        add run-time type checking to a function from its type hints
    """

    ###
    # this implementation of strictly wraps the input function
    # The long term goal might be to generate python bytecode and insert it
    # at the front of the function and insert return checks infront of the
    # return bytecode
    ###

    global strictly, _tupleize_type, _raise_strictly_error

    if strictly.disable:
        return func

    assert callable(func),('this line is from strictly',\
        f"only callable objects can be decorated as strict, got {func}")[1]
    assert hasattr(func, '__annotations__'),('this line is from strictly',\
        f"an object must be annotateable to be decorated as strict")[1]

    # get base info about all the arguments
    anotes = func.__annotations__
    vars = func.__code__.co_varnames
    # pack information fora ll argumetsn assuming they were all positional
    var_packs = [(index, var, _tupleize_type(anotes.get(var, object))) for index, var in enumerate(vars)]
    # make a dict of vars to tuples of their types
    var_dict = {var:tp for index, var, tp in var_packs}
    if 'return' in anotes:
        check_return = True
        ret_types = _tupleize_type(anotes['return'])
    else:
        check_return = False

    # define a wrapper function to perform the type_checking
    @wraps(func) # add sanitation
    def strictly_typed_func(*args, **kwargs):
        # check the positional arguments
        for pack, arg in zip(var_packs, args):
            index, name, types = pack
            if not isinstance(arg, types):
                _ = (f"positional argument", name, func, arg, types)
                raise TypingError(*_ # this line is from strictly
                )
        # check all keyword arguments
        for kw, arg in kwargs.items():
            types = var_dict[kw]
            #print(kw, arg, types)
            if not isinstance(arg, types):
                _ = ('keyword argument', kw, func, arg, types)
                raise TypingError(*_ # this line is from strictly
                )
        # run the actual function
        ret = \
        func(*args, **kwargs # this line is a pass-through from strictly
        )

        if check_return:
            if not isinstance(ret, ret_types):
                _ = ('return', '', func, ret, ret_types)
                raise TypingError(*_ # this line is from strictly
                )

        # aaaaaand, finally return the value
        return ret

    # return the wrapped function
    return strictly_typed_func

# set the disable flag
strictly.disable = not __debug__

# and here we have could fun!
strictly = strictly(strictly)
#_raise_strictly_error = strictly(_raise_strictly_error)
