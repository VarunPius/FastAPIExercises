# Import
from src.consumer import run_consumer_stream

run_consumer_stream()


'''
This file is a runner for the `consumer` file within the `src` module
We will run into `ModuleNotFoundError: No module named 'src'` error when directly running `consumer.py`

One way to fix that is including the following in the consumer file:
import sys                                               
from os.path import dirname, abspath                     
sys.path.insert(0, dirname(dirname(abspath(__file__))))  

Other is running the files in the module via a runner, and importing all the modules in the runner.

The reason for this is you can't do relative imports from the file you execute since __main__ module is not a part of a package.

Explanation:
Absolute imports - import something available on sys.path

Relative imports - import something relative to the current module, must be a part of a package

If you're running both variants in exactly the same way, one of them should work. 
Here is an example that should help you understand what's going on. 
Let's add another main.py file with the overall directory structure like this:

.
./main.py
./ryan/__init__.py
./ryan/config.py
./ryan/test.py
And let's update test.py to see what's going on:

`
# config.py
debug = True
`

`
# test.py
print(__name__)

try:
    # Trying to find module in the parent package
    from . import config
    print(config.debug)
    del config
except ImportError:
    print('Relative import failed')

try:
    # Trying to find module on sys.path
    import config
    print(config.debug)
except ModuleNotFoundError:
    print('Absolute import failed')
`

`
# main.py
import ryan.test
`

Let's run test.py first:


$ python ryan/test.py
__main__
Relative import failed
True

Here "test" is the __main__ module and doesn't know anything about belonging to a package. 
However import config should work, since the ryan folder will be added to sys.path.

Let's run main.py instead:

$ python main.py
ryan.test
True
Absolute import failed

And here test is inside of the "ryan" package and can perform relative imports. 
import config fails since implicit relative imports are not allowed in Python 3.
'''