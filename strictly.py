from typing import *
import typing as _typing
import types as _types

class TypingError(TypeError):
    pass

def _tupleize_type(tp):
    #print('\n_tupleize_type')
    if tp is None:
        ret = type(None)
    if isinstance(tp, _typing._GenericAlias):
        print(tp, tp._name)
        if tp._name == None:
            tups = [_tupleize_type(teyep) for teyep in tp.__args__]
            ret = ()
            for tup in tups:
                ret += tup
        elif tp._name == 'Dict':
            return (dict,)
        elif tp._name == 'List':
            return (list,)
        elif tp._name == 'Tuple':
            return (tuple,)
        else:
            raise TypingError(f"unsupported generic alias {tp} not yet supported, try using a 'Union' or the base type (EX: 'dict' instead of Dict[Foo, Bar])")
    elif isinstance(tp, type):
        ret = (tp,)
    elif isinstance(tp, tuple):
        tups = [_tupleize_type(teyep) for teyep in tp]
        ret = ()
        for tup in tups:
            ret += tup
    else:
        ret = (type(tp),)
        #ret = (object,)
    print(tp, ret, '\n')
    return ret

disable = False

def strictly(func):
    global disable
    if disable:
        return func

    assert callable(func), f"only callable objects can be decorated as strict"
    assert hasattr(func, '__annotations__'), f"an object must be annotateable to be decorated as strict"

    # get base info about all the arguments
    anotes = func.__annotations__
    vars = func.__code__.co_varnames
    # pack information fora ll argumetsn assuming they were all positional
    var_packs = [(index, var, _tupleize_type(anotes.get(var, object))) for index, var in enumerate(vars)]
    # make a dict of vars to tuples of their types
    var_dict = {var:tp for index, var, tp in var_packs}
    ret_types = _tupleize_type(anotes.get('return', object))

    # define a wrapper function to perform the type_checking
    def strict_func(*args, **kwargs):
        # check the positional arguments
        for pack, arg in zip(var_packs, args):
            index, name, types = pack
            if not isinstance(arg, types):
                raise TypeError( # this line is from strictly
                     f"\ninvalid argument type in call of {repr(func.__name__)}, {func}\n"\
                    +f"\targument '{name}' must be of type <{', '.join([repr(typ.__name__) for typ in types])}>\n"\
                    +f"\tfound argument of type <{type(arg).__name__}> from value {repr(arg)}"
                    )
        # check all keyword arguments
        for kw, arg in kwargs.items():
            types = var_dict[kw]
            #print(kw, arg, types)
            if not isinstance(arg, types):
                raise TypeError( # this line is from strictly
                     f"\ninvalid keyword argument type in call of {repr(func.__name__)}, {func}\n"\
                    +f"\tkwarg '{kw}' must be of type <{', '.join([repr(typ.__name__) for typ in types])}>\n"\
                    +f"\tfound kwarg of type <{type(arg).__name__}> from value {repr(arg)}"
                    )
        # run the actual  function
        ret = func(*args, **kwargs)
        # check the type of the return value
        if not isinstance(ret, ret_types):
            raise TypeError( # this line is from strictly
                 f"\nincorrect return type from {func}\n"\
                +f"\texpected type <{', '.join([repr(typ.__name__) for typ in ret_types])}>\n"\
                +f"\tfound return of type <{type(ret).__name__}> from value {repr(ret)}"
                )
        # ahhh, finally return
        return ret

    # make the name denote a difference
    strict_func.__name__ = 'strict_'+func.__name__

    # return the wrapped function
    return strict_func

# tests
if __name__ == '__main__':

    @strictly
    def foo(a:int,  aa, /, b : int,  c : int = 5, *, d : Optional[str]) -> int :
        if d is None:
            d = 0
        else:
            d = int(d)
        return a+aa+b+c+d

    # these should work
    foo(0, 1, 2, 3, d="4")
    foo(0, 1, 2, c=3, d="4")
    foo(0, 1, b=2, c=3, d="4")
    foo(0, 1, c=3, b=2, d="4")

    # test intentional type errors
    class TestError(Exception): pass
    # test pos only arg fail
    try:
        foo('f', 1, 2, d=4)
        raise TestError("strictly did not catch a pos only type mis-match")
    except TypeError:
        print('pos only type mis-match properly caught')

    try:
        foo(0, 'g', 2, d=0)
        raise TestError("strictly did not catch a normal arg type mis-match")
    except TypeError:
        print('normal arg type mis-match properly caught')

    try:
        foo(0, 1, 'x', d=0)
        raise TestError("strictly did not catch a default arg type mis-match")
    except TypeError:
        print('default arg type mis-match properly caught')

    try:
        foo(0, 1, 2, d=0)
        raise TestError("strictly did not catch a kwarg only type mis-match")
    except TypeError:
        print('kwarg type mis-match properly caught')

    print('tests passed')

#foo('5', 1, c=3, b=2, d="4")
