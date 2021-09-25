import mooremachine

def getData():
    table = {
        'A': [ ['E', 0], ['D', 1] ],
        'B': [ ['F', 0], ['D', 0] ],
        'C': [ ['E', 0], ['B', 1] ],
        'D': [ ['F', 0], ['B', 0] ],
        'E': [ ['C', 0], ['F', 1] ],
        'F': [ ['B', 0], ['C', 0] ]
    }

    print(mooremachine.mooreReductionComplete(table))


if __name__ == "__main__":
    getData()
