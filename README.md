## cavlang

cavlang is a small library for parsing and evaluating [Macaroon-style caveats](https://ai.google/research/pubs/pub41892).

Some example caveats you can express in cavlang:

`username = alice`

`object_id = 17`

`current_time <= 1555187389`

`operation in [read write]`

## example usage

```python
import time
from caveats import evaluate

# create a caveat requiring a username to be alice
username_caveat = 'username = alice'
# create a caveat requiring a token is used before a certain time
expiry_caveat = 'time < %d' % (int(time.time()) + 10)
# create a caveat requiring a read or write action
action_caveat = 'action in [read write]'

# a sample context generated as a result of some action
context = {
    'time': int(time.time()),
    'username': 'alice',
    'action': 'read',
}

# evaluate each caveat in the context. all should be true!
assert(evaluate(context, username_caveat))
assert(evaluate(context, expiry_caveat))
assert(evaluate(context, action_caveat))
print('done!')
```
