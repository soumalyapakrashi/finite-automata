import mooremachine

# This function is used for debugging purposes. This bypasses the lengthy process of giving input in the terminal
def debugProgram():
    table = {
        'A': [ ['E', 0], ['D', 1] ],
        'B': [ ['F', 0], ['D', 0] ],
        'C': [ ['E', 0], ['B', 1] ],
        'D': [ ['F', 0], ['B', 0] ],
        'E': [ ['C', 0], ['F', 1] ],
        'F': [ ['B', 0], ['C', 0] ]
    }

    final_table = mooremachine.mooreReductionComplete(table)
    print("")
    mooremachine.printStateTransitionTable(final_table)


# Prints a short description of the input expected and gives an example
def printInfoMessage():
    print("NOTE:")
    print("Currently, the implementation supports only a completely specified Moore Machine. The machine can have one 'present state' and 2 'input symbols' - 0 and 1. For each 'input symbol', each 'present state' will have a corresponding 'next state' and an 'output symbol' which again, has to be either 0 or 1. An example of the state trasition table of such a machine is shown as follows for reference:")
    print("")

    print("PS |   Input Symbols")
    print("   |    0    |    1")
    print("   | NS | OS | NS | OS")
    print("----------------------")
    print(" A |  E |  0 |  D |  1")
    print(" B |  F |  0 |  D |  0")
    print(" C |  E |  0 |  B |  1")
    print(" D |  F |  0 |  B |  0")
    print(" E |  C |  0 |  F |  1")
    print(" F |  B |  0 |  C |  0")

    print("")
    print("PS: Present State")
    print("NS: Next State")
    print("OS: Output Symbol")


# Gets the state transition table as input from user and prints the standardized version of the reduced
# state transition table
def getData():
    table = {}

    printInfoMessage()

    print("\nInput State Transition Table:")
    nos_states = 0
    try:
        nos_states = int(input("Total Number of States = "))
    except:
        print("Invalid value of the total number of states")

    for state_counter in range(nos_states):
        try:
            cs = input(f"Current State (State Number: {state_counter + 1}) = ")
            print("\nFor Input Symbol: 0")
            ns0 = input("Next State = ")
            os0 = int(input("Output Symbol = "))
            print("\nFor Input Symbol: 1")
            ns1 = input("Next State = ")
            os1 = int(input("Output Symbol = "))
            table[cs] = [ [ ns0, os0], [ ns1, os1 ] ]
        except:
            print("\nInvalid Input")
            break

        print("")

    final_table = mooremachine.mooreReductionComplete(table)
    print("")
    mooremachine.printStateTransitionTable(final_table)


if __name__ == "__main__":
    getData()
