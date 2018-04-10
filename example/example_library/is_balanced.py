
def is_balanced(s):
    parens = {
        ')': '(',
        ']': '[',
        '}': '{',
    }
    opens = parens.values()
    closes = parens.keys()
    found_opens = list()
    for c in s:
        if c in opens:
            found_opens.append(c)
        elif c in closes:
            try:
                last_open = found_opens.pop()
            except IndexError:
                return False
            if parens[c] != last_open:
                return False
    return not len(found_opens)


if __name__ == "__main__":
    print(is_balanced(''))
    print(is_balanced('hello'))
    print(is_balanced('(yes)'))
    print(is_balanced('[(no])'))
    print(is_balanced('{}[]([wee])'))

