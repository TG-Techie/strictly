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
