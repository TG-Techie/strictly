from typing import *
import typing as _typing
from functools import wraps # a wrapping tool that maintains sanitation.

# the following flags are instancse attributes on the strictly function
#   disable             : turns off type checking and wrapping

# set what should be exported from the module
__all__ = ['strictly', 'TypingError', 'DeterminationError', 'NoneType']

NoneType = type(None)

class TypingError(TypeError):
    pass

class DeterminationError(TypeError):
    pass

def _tupleize_type(tp):
    if tp is None:
        ret = type(None)
    if isinstance(tp, _typing._GenericAlias):
        if tp.__origin__ == Union:
            tups = [_tupleize_type(teyep) for teyep in tp.__args__]
            ret = ()
            for tup in tups:
                ret += tup
        elif hasattr(tp, '__origin__'):
            return (tp.__origin__,)
        else:
            raise DeterminationError(f"cannot determin what type to check {tp} against")
    elif isinstance(tp, type):
        ret = (tp,)
    elif isinstance(tp, tuple):
        tups = [_tupleize_type(teyep) for teyep in tp]
        ret = ()
        for tup in tups:
            ret += tup
    else:
        ret = (type(tp),)
    return ret

def strictly(func):
    global strictly

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
    def strict_func(*args, **kwargs):
        # if strictly is disable at runtime do not check types
        if strictly.disable:
            return func(*args, **kwargs) # this line is a pass-through from strictly

        # check the positional arguments
        for pack, arg in zip(var_packs, args):
            index, name, types = pack
            if not isinstance(arg, types):
                raise TypingError( # this Error is from strictly
                     f"\ninvalid argument type in call of {repr(func.__name__)}, {func}\n"\
                    +f"\targument '{name}' must be of type <{', '.join([typ.__name__ for typ in types])}>\n"\
                    +f"\tfound argument of type <{type(arg).__name__}> from value {repr(arg)}"
                    )
        # check all keyword arguments
        for kw, arg in kwargs.items():
            types = var_dict[kw]
            #print(kw, arg, types)
            if not isinstance(arg, types):
                raise TypingError( # this Error is from strictly
                     f"\ninvalid keyword argument type in call of {repr(func.__name__)}, {func}\n"\
                    +f"\tkwarg '{kw}' must be of type <{', '.join([typ.__name__ for typ in types])}>\n"\
                    +f"\tfound kwarg of type <{type(arg).__name__}> from value {repr(arg)}"
                    )
        # run the actual function
        # move the call onto another line to make excepts clearer
        ret = \
        func( # this line is a pass-through from strictly
            *args, **kwargs
        )
        # check the type of the return value
        if check_return:
            if not isinstance(ret, ret_types):
                raise TypingError( # this Error is from strictly
                     f"\nincorrect return type from {func}\n"\
                    +f"\texpected type <{', '.join([typ.__name__ for typ in ret_types])}>\n"\
                    +f"\tfound return of type <{type(ret).__name__}> from value {repr(ret)}"
                    )
        # ahhh, finally return
        return ret

    # return the wrapped function
    return strict_func

# set the disable flag
strictly.disable = not __debug__
