from pyparsing import *

VALID_OPERATIONS = ('=', '<', '>', '<=', '>=', '!=', 'in')
NAME = Word(alphanums, min=1, max=64)
NUMBER = Word(nums, min=1, max=64)
suppress = lambda c: Suppress(Literal(c))
list_thing = lambda t: Group(suppress('[') + ZeroOrMore(t) + suppress(']'))
list_names = list_thing(NAME)
list_numbers = list_thing(NUMBER)

key = NAME('key')
opr = oneOf(' '.join(VALID_OPERATIONS))('operation')
val = Or([NAME, NUMBER, list_names, list_numbers])('value')
parser = key + opr + val
parse = parser.parseString

def evaluate(context, caveat):
    if caveat.key not in context:
        return False
    return True
