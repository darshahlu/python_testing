from example.example_library.is_balanced import is_balanced


def test_is_balanced():
    assert is_balanced('') == True
    assert is_balanced('hello') == True
    assert is_balanced('(yes)') == True
    assert is_balanced('[(nope])') == False
    assert is_balanced('{}[]([wee!])') == True
    assert is_balanced('{') == False
    assert is_balanced(')') == False
