from example.example_library.is_balanced import is_balanced


def test_is_balanced():
    assert is_balanced('') is True
    assert is_balanced('hello') is True
    assert is_balanced('(yes)') is True
    assert is_balanced('[(nope])') is False
    assert is_balanced('{}[]([wee!])') is True
    assert is_balanced('{') is False
    assert is_balanced(')') is False
