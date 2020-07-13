from typing import *
from strictly import *

# just decorate your annotated function with 'strictly'
@strictly
def heyey(name: str, greeting: str = 'hey', *, punctuation: Optional[str]='!'):
    """
    desc: this is now strictly typed, whenever it is called strictly will
        check the inputs against the type hints above.
    """
    if punctuation is None:
        punctuation = ''
    print(greeting, name+punctuation)

# run it
heyey('Dingo') # runs fine
heyey('Zoot', 'oh no, bad bad') # also fine
try:
    heyey(5) # this should error
except TypingError as mistake:
    print('strictly caught the TypeError listed below')
    raise mistake
