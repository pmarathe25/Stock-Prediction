def parseFile(filename):
    symbols = []
    with open(filename) as f:
        for line in f:
            symbols.append(line.split('|')[1])
    return symbols
