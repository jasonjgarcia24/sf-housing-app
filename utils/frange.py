import decimal


def frange(x, y, step):
    x    = str(x)    if not isinstance(x, str)    else x
    y    = str(y)    if not isinstance(y, str)    else y
    step = str(step) if not isinstance(step, str) else step
    
    x = decimal.Decimal(x)
    y = decimal.Decimal(y)
    
    while x < y:
        yield float(x)
        x += decimal.Decimal(step)