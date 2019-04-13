import pytest
from caveats import parse, evaluate

TEST_CONTEXT = {'a': 1, 'b': 2, 'foo': 'bar'}

@pytest.mark.parametrize('caveat,expected', [
        ('k = v', ['k', '=', 'v']),
        ('k != v', ['k', '!=', 'v']),
        ('k < v', ['k', '<', 'v']),
        ('k > v', ['k', '>', 'v']),
        ('k <= v', ['k', '<=', 'v']),
        ('k >= v', ['k', '>=', 'v']),
        ('foo != bar', ['foo', '!=', 'bar']),
        ('k in [a]', ['k', 'in', ['a']]),
        ('k in []', ['k', 'in', []]),
        ('curtime <= 123', ['curtime', '<=', 123]),
        ('abc in [1 2 3]', ['abc', 'in', [1, 2, 3]]),
        ('urn:foo:bar.baz_baz = a:b-c', ['urn:foo:bar.baz_baz', '=', 'a:b-c']),
    ])
def test_parser(caveat, expected):
    result = parse(caveat)
    assert(len(expected) == 3)
    assert(result[0] == expected[0])
    assert(result[1] == expected[1])
    assert(result[2] == expected[2])

@pytest.mark.parametrize('s,context,expected', [
        ('foo = bar', TEST_CONTEXT, True),
        ('dne = dne', TEST_CONTEXT, False),
    ])
def test_evaluate(s, context, expected):
    assert(evaluate(context, s) == expected)
