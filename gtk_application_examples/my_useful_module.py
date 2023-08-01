x = "global x"

def outer():
    x = "x in outer"
    print("outer x = ", x)

    def inner():
        nonlocal x
        x = x + " modified"
        print("inner x = ", x)

    inner()

outer()
