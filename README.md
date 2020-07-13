# python-strictly

A run-time tool to enforce strict typing in python using type hints.

## Usage Example:
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
<summary>Traceback</summary>

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

## Incremental Integration
You do not need to annotate every argument, this is meant to make the
transition to using strictly as easy as possible. Just decorate any function
you want strictly typed and fill in the annotations later.
```python
from strictly import *

@strictly
def foo(unchecked, checked: int) -> int:
    return unchecked+checked

# this will be fine
foo(1, 2)

# foo only allows ints to be returned
foo(3.0, 4) # TypingError
# if returning 'float's is desired functionality the return annotation should
#   be from the typing module, EX: `Union[int, float]`

# this will not work b/c `str`s and 'int's cannot be added together
foo('5', 6) # concatenation error
# this type error was not caught by strictly b/c the 'unchecked' argument was not annotated
```
<details>
<summary>TypingError Traceback</summary>

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
<summary>Concatenation Traceback</summary>

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

## Distribution / Production
Procedurally type checking every input at runtime slows down performance,
inorder to combat this strictly can be disbaled completely.
```python
strictly.disable = True
```
When strictly is disabled any previously altered functions will not be checked when called.
Additionally, any functions decorated after strictly is disabled will not altered and won't be checked even if strictly is enabled later.
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

#since strictly is disabled both of these
foo(None) # this has a small performance hit b/c it was altered
bar(None)
```
</details>


## Using the Typing Module
Currently, strictly has limited support for generic notation from the typing module;
supported generics include `Dict[T, S]`, `List[T]`, `Tuple[T]`, `Union[T, S...]`,
and `Optional[T]`.

 Strictly speaking, typing module functionality __may__ be extended or altered in the future.

#### Iterable Generics
Iterable generics are treated as normal variables, only the argument is
checked to for proper type, not the contents of the argument.
for example:
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
<summary>Traceback</summary>

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
This functionality was intentional excluded to reduce runtime burden. Check this kind of error conventionally:

```python
assert all([isinstance(num, int) for num in nums]), "the input must only contain 'int's"
```

## Issues and Features:
- For both Issues and proposed features please feel free to __message me on discord__: `TG-Techie#5402`.
- __Bugs__: If you find a bug/issue in strictly please file an issue on github with an example and explanation.
- __Features__: If you have a proposed feature please fork this repositor and make a pull request with the code or without code make an issue to discuss the possible feature.

### License
Strictly is distributed freely under the MIT License.

#### Possible Future Features (no promises):
 - A `strictly.require_hints` flag to ensure every argument has a type hint (defauting False).
 - An opt-in option feature to programatically check the content of generics.
