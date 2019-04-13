import pytest
from caveats import parse, evaluate
from pyparsing import ParseException

TEST_CONTEXT = {"user_id": 1, "expires": 100, "username": "alice", "op": "READ"}


@pytest.mark.parametrize(
    "caveat,expected",
    [
        ("k = v", ["k", "=", "v"]),
        ("k != v", ["k", "!=", "v"]),
        ("k < v", ["k", "<", "v"]),
        ("k > v", ["k", ">", "v"]),
        ("k <= v", ["k", "<=", "v"]),
        ("k >= v", ["k", ">=", "v"]),
        ("foo != bar", ["foo", "!=", "bar"]),
        ("k in [a]", ["k", "in", ["a"]]),
        ("k in []", ["k", "in", []]),
        ("curtime <= 123", ["curtime", "<=", 123]),
        ("abc in [1 2 3]", ["abc", "in", [1, 2, 3]]),
        ("urn:foo:bar.baz_baz = a:b-c", ["urn:foo:bar.baz_baz", "=", "a:b-c"]),
    ],
)
def test_parser(caveat, expected):
    result = parse(caveat)
    assert len(expected) == 3
    assert result[0] == expected[0]
    assert result[1] == expected[1]
    assert result[2] == expected[2]


@pytest.mark.parametrize(
    "caveat",
    [
        "bad",
        "foo == bar",
        "123 = not a valid key",
        "foo = [1, not_a_number]",
        "foo = [string, 123]",
        "foo = [[heheh]]",
        "foo = 1.0",
        "A" * 100 + " = foo",
        "    = bar",
        "foo = ",
    ],
)
def test_invalid_strings(caveat):
    with pytest.raises(ParseException):
        print(parse(caveat))


@pytest.mark.parametrize(
    "s,context,expected",
    [
        ("user_id = 1", TEST_CONTEXT, True),
        ("missing_context_key = dne", TEST_CONTEXT, False),
        ("expires <= 100", TEST_CONTEXT, True),
        ("username != bob", TEST_CONTEXT, True),
        ("op in [READ WRITE]", TEST_CONTEXT, True),
        ("op in [WRITE]", TEST_CONTEXT, False),
    ],
)
def test_evaluate(s, context, expected):
    assert evaluate(context, s) == expected
