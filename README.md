# python-strictly

A run-time tool to enforce strict typing in python using type hints.
<br/>
Write type-safe python code with confidence, focus on the problem you need to solve.

## Usage Example:
All you need to do is decorate your functions with `strictly`.
```python
from strictly import *

@strictly
def my_func(a: int, b: int) -> int:
    return a + b
```

<details>
<summary> Longer Example </summary>

```python
from typing import *
from strictly import *

# just decorate your annotated function with 'strictly'
@strictly
def heyey(name: str, greeting: str='hey', *, punctuation: Union[str, None]='!') -> None:
    """
    print a greeting to say hey.
    this is a strictly typed function, whenever it is called strictly will
    check the inputs against the type hints above;
    """
    if punctuation is None:
        punctuation = ''
    print(greeting, name+punctuation)

# runs fine
heyey('Dingo')
# this will also be fine
heyey('Zoot', 'oh no, bad bad')
# this should error and be caught by strictly
heyey(5)
```
<details>
<summary>Show Traceback</summary>

```
hey Dingo!
oh no, bad bad Zoot!
Traceback (most recent call last):
  File "/Users/jonahym/Documents/thoughts/py_static/negative_tests/simple.py", line 21, in <module>
    heyey(5)
  File "/Users/jonahym/Documents/thoughts/py_static/strictly.py", line 79, in strict_func
    raise TypingError( # this Error is from strictly
strictly.TypingError:
invalid argument type in call of 'heyey', <function heyey at 0x7fd160203c10>
        argument 'name' must be of type <str>
        found argument of type <int> from value 5
```
</details>
</details>

### Tracebacks
When a strictly typed function is passed an argument of the wrong type, strictly will raise a `TypingError` with a formatted message.
For example, this:
```python
my_func(5, 3) # returns 8, no issue
my_func('Not a number', 'Definitely not a number!') # TypingError
```
will have this traceback below:
```
Traceback (most recent call last):
  File "/Users/jonahym/Documents/strictly/strictly.py", line 118, in strict_func
    raise TypingError(*_ # this line is from strictly
strictly.TypingError:
invalid positional argument type in call of 'my_func', <function my_func at 0x7fef9ae751e0>
        positional argument 'a' must be of type <int>
        found positional argument of type <str> from the value 'Not a number'
```

### Installation
strictly is available through pypi, just pip install it using the command line.
```bash
$pip3 install strictly
```

## Incremental Integration
Unannotated arguments will not be checked, this is meant to make the strictly typed transition as easy as possible.
Just decorate any function you want strictly typed and fill in the argument and return annotations later.
```python
from strictly import *

@strictly
def add(unchecked, checked: int) -> int:
    return unchecked+checked

# this will be fine
add(1, 2)

# foo only allows ints to be returned
add(3.0, 4) # TypingError
# if returning 'float's is desired functionality the return annotation should
#   be from the typing module, EX: `Union[int, float]`

# this will not work b/c `str`s and 'int's cannot be added together
add('5', 6) # concatenation error
# this type error was not caught by strictly b/c the 'unchecked' argument was not annotated
```
<details>
<summary>Show TypingError Traceback</summary>

```
Traceback (most recent call last):
  File "/Users/jonahym/Documents/thoughts/py_static/negative_tests/mixed_checking.py", line 11, in <module>
    foo(3.0, 4)
  File "/Users/jonahym/Documents/thoughts/py_static/strictly.py", line 99, in strict_func
    raise TypingError( # this line is from strictly
strictly.TypingError:
incorrect return type from <function foo at 0x7f8c101f2af0>
        expected type <int>
        found return of type <float> from value 7.0
```
</details>

<details>
<summary>Show Concatenation Traceback</summary>

```
Traceback (most recent call last):
  File "/Users/jonahym/Documents/thoughts/py_static/negative_tests/mixed_checking.py", line 16, in <module>
    foo('5', 6)
  File "/Users/jonahym/Documents/thoughts/py_static/strictly.py", line 97, in strict_func
    func( # this line is a pass-through from strictly
  File "/Users/jonahym/Documents/thoughts/py_static/negative_tests/mixed_checking.py", line 5, in foo
    return unchecked+checked
TypeError: can only concatenate str (not "int") to str
```
</details>


## Type Checking Custom Classes
Use strictly with custom classes as you would with a builtin class. Strictly has full support for single class type hints and limited support for Union and Generic notation
(See: "Using the Typing Module" below).
```python
from strictly import *

class Scene():
    # any function (including methods) can by strictly typed
    @strictly
    def __init__(self, number: int):
        # b/c this is a method the self argument is not annotated
        # since this is '__init__' the return type isn't annotated either
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
```
<details>
<summary>Show 1st Traceback</summary>

```
on to scene 24, which is a smashing scene with some lovely acting, in which Arthur discovers a vital clue.
Traceback (most recent call last):
  File "/Users/jonahym/Documents/thoughts/py_static/examples/simple_custom_classes.py", line 21, in <module>
    the_scene = Scene('not a number') # TypingError
  File "/Users/jonahym/Documents/thoughts/py_static/strictly.py", line 78, in strict_func
    raise TypingError( # this Error is from strictly
strictly.TypingError:
invalid argument type in call of '__init__', <function Scene.__init__ at 0x7fc2b801c9d0>
        argument 'number' must be of type <int>
        found argument of type <str> from value 'not a number'
```
</details>

<details>
<summary>Show 2nd Traceback</summary>

```
on to scene 24, which is a smashing scene with some lovely acting, in which Arthur discovers a vital clue.
Traceback (most recent call last):
  File "/Users/jonahym/Documents/thoughts/py_static/examples/simple_custom_classes.py", line 22, in <module>
    narrate('nothing') # 2nd TypingError
  File "/Users/jonahym/Documents/thoughts/py_static/strictly.py", line 78, in strict_func
    raise TypingError( # this Error is from strictly
strictly.TypingError:
invalid argument type in call of 'narrate', <function narrate at 0x7f8b1827e3a0>
        argument 'scene' must be of type <Scene>
        found argument of type <str> from value 'nothing'
```
</details>

## Using the Typing Module
Currently, strictly has limited support for generic notation from the typing module;
supported generics include `Dict[T, S]`, `List[T]`, `Tuple[T]`,`Union[T, S...]`,and `Optional[T]` for non-generic inputs.

Work on making strictly completely compatible with the typing module is on going (See: "Possible Future Features" below).

#### Iterable Generics
Iterable generics are treated as normal variables, only the argument itself is checked for the proper type, not the contents .
For example:
```python
from typing import *
from strictly import *

@strictly
def find_max(nums : List[int]) -> int:
    return max(nums)
# will work, strictly check that the input is a list
find_max([7, 2, 5, 9, 3])
# however, it will not check the the objects in the list
find_max([7, 2, 5, 9, '9000'])
```
<details>
<summary>Show Traceback</summary>

```
Traceback (most recent call last):
  File "/Users/jonahym/Documents/thoughts/py_static/negative_tests/generic_check.py", line 10, in <module>
    find_max([7, 2, 5, 9, '9000'])
  File "/Users/jonahym/Documents/thoughts/py_static/strictly.py", line 97, in strict_func
    func( # this line is a pass-through from strictly
  File "/Users/jonahym/Documents/thoughts/py_static/negative_tests/generic_check.py", line 6, in find_max
    return max(nums)
TypeError: '>' not supported between instances of 'str' and 'int'
```
</details>
<br/>
This functionality was intentionally excluded to reduce run-time burden. Check this kind of error conventionally:

```python
assert all([isinstance(num, int) for num in nums]), "the input must only contain 'int's"
```

## Distribution / Production
Procedurally type checking every input at run-time slows down performance,
inorder to combat this strictly can be disbaled completely.
```python
strictly.disable = True
```
When strictly is disabled functions will not be altered, meaning even if strictly
is turned back on any functions made while strictly was disbaled will not be checked.
<details>
<summary>Longer Example</summary>

```python
from strictly import *

@strictly
def foo(x: int) -> int:
    return x

strictly.disable = True # from here on all functions are unaltered

@strictly
def bar(y: str) -> str:
    return y

foo(None) # this will be checked
bar(None) # this won't be checked
```
</details>

## Issues and Features:
- For both Issues and proposed features please feel free to message me on discord: `TG-Techie#5402`.
- __Bugs__: If you find a bug/issue in strictly please file an issue on github with an example and explanation.
- __Features__: If you have a proposed feature please fork the [strictly repo](https://github.com/TG-Techie/strictly) and make a pull request with the code or without code make an issue to discuss the possible feature.

### License
Strictly is distributed freely under the MIT License.

#### Possible Future Features (no promises):
 - support for `ForwardRef` Hint from the typing module.
 - Add a `strictly.disable_checks` flag so that every function gets altered but won't be checked at run-time.
 - A `strictly.require_hints` flag to ensure every argument has a type hint (defaulting False).
 - An opt-in option feature to programmatically check the content of generics.
