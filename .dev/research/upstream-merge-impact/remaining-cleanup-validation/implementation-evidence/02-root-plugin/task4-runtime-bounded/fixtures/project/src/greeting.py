def greet(name):
    if not name:
        raise ValueError("name required")
    return f"Hello, {name}!"
