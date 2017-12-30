def a():
    count = 0
    def b():
        nonlocal count
        def c(x):
            nonlocal count
            return count + x
        return c
    return b
new = a()()
print(new(5))
print(new(3))

