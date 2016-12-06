def clamp(value, lowerBound, upperBound):
    if value < lowerBound:
        value = lowerBound
    elif value > upperBound:
        value = upperBound
    return value
