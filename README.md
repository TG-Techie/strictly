# python-strictly

A run-time tool to enforce strict typing in python using type hints.

## Usage Example:
```python
from typing import *
from strictly import *

# just decorate your annotated function with 'strictly'
@strictly
def heyey(name: str, greeting: str = 'hey', *, punctuation: Optional[str]='!') -> None:
    """
    desc: this is now strictly typed, whenever it is called strictly will
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
```
hey Dingo!
oh no, bad bad Zoot!
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/jonahym/Documents/thoughts/py_static/strictly.py", line 79, in strict_func
    raise TypingError( # this line is from strictly
strictly.TypingError:
invalid argument type in call of 'heyey', <function heyey at 0x7ff74800baf0>
        argument 'name' must be of type <str>
        found argument of type <int> from value 5
```

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
foo(3.0, 4)
# if returning 'float's is desired functionality the return annotation should
#   be from the typing module, EX: `Union[int, float]`

# this will not work b/c `str`s and 'int's cannot be added together
foo('5', 6)
```
<details>
    <summary>Traceback</summary>
    ```
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/Users/jonahym/Documents/thoughts/py_static/strictly.py", line 95, in strict_func
        ret = func(*args, **kwargs)
      File "<stdin>", line 3, in foo
    TypeError: can only concatenate str (not "int") to str
    ```
</details>

## Using the Typing Module
Currently, strictly has limited support for generic notation from the typing module; supported generics include `Dict[T, S]`, `List[T]`, `Tuple[T]`, `Union[T, S...]`, and `Optional[T]`.

Typing Module functionality may be extended, changed, or replaced in the future.
#### Iterable Generics
Iterable generics are treated as normal variables, only the argument is checked to for proper type, not the contents of teh argument. for example:
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
This functionality was intentional excluded to reduce runtime burden. Check this kind of error conventionally by:
```python
assert all([isinstance(num, int) for num in nums]), "the input must only contain 'int's"
```

## Issues:
if you find a bug/issue in strictly or have a feature toropose please file an issue or pull request respectively.
