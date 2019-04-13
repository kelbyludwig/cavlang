from pyparsing import *

def to_int(tokens):
    assert(len(tokens) == 1)
    return int(tokens[0])

VALID_OPERATIONS = ('=', '<', '>', '<=', '>=', '!=', 'in')
NAME = Word(alphas + '_.-:', min=1, max=64)
NUMBER = Word(nums, min=1, max=64).addParseAction(to_int)
LBRACE, RBRACE = Literal('['), Literal(']')
LIST_T = lambda t: Group(Suppress(LBRACE) + ZeroOrMore(t) + Suppress(RBRACE))
LIST_NAMES = LIST_T(NAME)
LIST_NUMBERS = LIST_T(NUMBER)

key = NAME('key')
opr = oneOf(' '.join(VALID_OPERATIONS))('operation')
val = (NAME | NUMBER | LIST_NAMES | LIST_NUMBERS)('value')
parser = key + opr + val
parse = parser.parseString

def evaluate(context, caveat):
    if caveat.key not in context:
        return False
    return True
