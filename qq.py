def f1():
    y = 5

    def f2():
        nonlocal y
        y += 1
        return y
    return f2


g = f1()
print(g())
print(g())
print(g())
print(g())
print(g())
print(g())
print(g())
