from typing import *
from strictly import *

strictly.disable = False

@strictly
def foo(a:int,  aa, b : int,  c : int = 5, *, d : Optional[str]) -> int :
    # `/,`s work after arguments but is excluded in this test for 3.6/3.7 compatibilty
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
    foo('f', 1, 2, d='4')
    raise TestError("strictly did not catch a pos only type mis-match")
except TypingError:
    print('pos only type mis-match properly caught')

try:
    foo(0, 7, 'g', 2, d='0')
    raise TestError("strictly did not catch a normal arg type mis-match")
except TypingError:
    print('normal arg type mis-match properly caught')

try:
    foo(0, 1, 'x', d='0')
    raise TestError("strictly did not catch a default arg type mis-match")
except TypingError:
    print('default arg type mis-match properly caught')

try:
    foo(0, 1, 2, d=0)
    raise TestError("strictly did not catch a kwarg only type mis-match")
except TypingError:
    print('kwarg type mis-match properly caught')

try:
    foo(0, 5.0, 2, d='0')
    raise TestError("strictly did not catch a return type error")
except TypingError:
    print('return type mis-match properly caught')

print('tests passed')
