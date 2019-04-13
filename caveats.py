from pyparsing import *

def to_int(tokens):
    assert(len(tokens) == 1)
    return int(tokens[0])

operation_dispatch = {
    '=':  lambda l, r: l == r,
    '<':  lambda l, r: l < r,
    '>':  lambda l, r: l > r,
    '<=': lambda l, r: l <= r,
    '>=': lambda l, r: l >= r,
    '!=': lambda l, r: l != r,
    'in': lambda l, r: l in r,
}

VALID_OPERATIONS = operation_dispatch.keys()
NAME = Word(alphas + '_.-:', min=1, max=64)
NUMBER = Word(nums, min=1, max=64).addParseAction(to_int)
LBRACE, RBRACE = Literal('['), Literal(']')
LIST_T = lambda t: Group(Suppress(LBRACE) + ZeroOrMore(t) + Suppress(RBRACE))
LIST_NAMES = LIST_T(NAME)
LIST_NUMBERS = LIST_T(NUMBER)

KEY = NAME
OPR = oneOf(' '.join(VALID_OPERATIONS))
VAL = NAME | NUMBER | LIST_NAMES | LIST_NUMBERS
parser = KEY + OPR + VAL
parse = lambda s: parser.parseString(s).asList()

def evaluate(context, s):
    caveat = parse(s)
    cav_key, cav_opr, cav_val = caveat
    ctx_val = context.get(cav_key)
    opr_func = operation_dispatch.get(cav_opr, lambda l, r: False)
    return opr_func(ctx_val, cav_val)
