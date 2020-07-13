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
    desc: print a greeting to say hey.
        this is a strictly typed, whenever it is called strictly will
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
Traceback (most recent call last):
  File "<stdin>", line 20, in <module>
  File "/Users/jonahym/Documents/thoughts/py_static/strictly.py", line 79, in strict_func
    raise TypingError( # this line is from strictly
strictly.TypingError:
invalid argument type in call of 'heyey', <function heyey at 0x7ff74800baf0>
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
foo(3.0, 4)
# if returning 'float's is desired functionality the return annotation should
#   be from the typing module, EX: `Union[int, float]`

# this will not work b/c `str`s and 'int's cannot be added together
foo('5', 6)
# this type error was not by strictly b/c the argument was not annotated
```
<details>
<summary>Traceback</summary>

```
Traceback (most recent call last):
  File "<stdin>", line 16, in <module>
  File "/Users/jonahym/Documents/thoughts/py_static/strictly.py", line 95, in strict_func
    ret = func(*args, **kwargs)
  File "<stdin>", line 1, in foo
TypeError: can only concatenate str (not "int") to str
```
</details>

## Distribution / Production
Proceedurally type checking every input at runtime slows down performance, inorder to combat this strictly can be disbaled completely.
```python
strictly.disable = True
```
When strictly is disabled any previously altered functions will not be checked.
Additionally, any functions decorated after strictly is disabled will not altered and won't be checked even if strictly is enabled later.
<details>
<summary>Longer Example</summary>

```python
from strictly import *

@strictly
def foo(x:int) -> int:
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
Currently, strictly has limited support for generic notation from the typing module; supported generics include `Dict[T, S]`, `List[T]`, `Tuple[T]`, `Union[T, S...]`, and `Optional[T]`.

 Typing Module functionality may be extended, changed, or replaced in the future.

#### Iterable Generics
Iterable generics are treated as normal variables, only the argument is checked to for proper type, not the contents of the argument. for example:
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
  File "<stdin>", line 10, in <module>
  File "/Users/jonahym/Documents/thoughts/py_static/strictly.py", line 95, in strict_func
    ret = func(*args, **kwargs)
  File "<stdin>", line 3, in find_max
TypeError: '>' not supported between instances of 'str' and 'int'
```
</details>
<br/>
This functionality was intentional excluded to reduce runtime burden. Check this kind of error conventionally:

```python
assert all([isinstance(num, int) for num in nums]), "the input must only contain 'int's"
```

## Issues and Features:
- In either case please feature feel free message me on discord: `TG-Techie#5402`.
- Bugs: If you find a bug/issue in strictly please file an issue on github with an example and explanation of the issue.
- Features: If you have proposed please fork this repositor and make a pull request.

### License
Strictly is distributed freely under the MIT License.

#### possible Future Features (no promises):
 - A `strictly.require_hints` flag to ensure every argument has a type hint
 - An opt-in option feature to programatically check the content of generics.
