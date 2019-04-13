from pyparsing import (
    Word, Literal, Group, Suppress, 
    ZeroOrMore, oneOf, alphas, nums,
)

# defined operations and their respective python functions
DISPATCH = {
    '=':  lambda l, r: l == r,
    '<':  lambda l, r: l < r,
    '>':  lambda l, r: l > r,
    '<=': lambda l, r: l <= r,
    '>=': lambda l, r: l >= r,
    '!=': lambda l, r: l != r,
    'in': lambda l, r: l in r,
}
VALID_OPERATIONS = DISPATCH.keys()

# names are string values with characters [a-zA-Z_.-:]
NAME = Word(alphas + '_.-:', min=1, max=64)

# numbers are integer values
NUMBER = Word(nums, min=1, max=64).addParseAction(lambda ts: int(ts[0]))

# braces define the beginning and end of a list
LBRACE, RBRACE = Literal('['), Literal(']')

# a list can contain names or numbers.
LIST_T = lambda t: Group(Suppress(LBRACE) + ZeroOrMore(t) + Suppress(RBRACE))
LIST_NAMES = LIST_T(NAME)
LIST_NUMBERS = LIST_T(NUMBER)

# the parser handles strings of the form "key operation value" where:
# * key is a name
# * operation is a defined operation
# * value is a name, number, or list of either.
KEY = NAME
OPR = oneOf(' '.join(VALID_OPERATIONS))
VAL = NAME | NUMBER | LIST_NAMES | LIST_NUMBERS
PARSER = KEY + OPR + VAL

def parse(s):
    '''parse parses a string and returns the result as a list of:
    [key, operation, value]
    '''
    return PARSER.parseString(s).asList()

def evaluate(context, s):
    '''given keys and values (a context), parse the string s and determine if
    the caveat is true or not.
    '''
    cav_key, cav_opr, cav_val = parse(s)
    ctx_val = context.get(cav_key)
    opr_func = DISPATCH.get(cav_opr, lambda l, r: False)
    return opr_func(ctx_val, cav_val)
