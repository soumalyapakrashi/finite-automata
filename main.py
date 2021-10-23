import argparse
import csv
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

    final_table = mooremachine.reduceAutomata(table)
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

    return table


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help = "Get data from file specified")
    args = parser.parse_args()

    # If input file has been mentioned
    if(args.file):
        table = {}

        # Read the data from the input CSV file
        with open(args.file, newline = '') as csvfile:
            filereader = csv.reader(csvfile)
            isFirstRow: bool = True

            for row in filereader:
                # The first row is supposed to have the header. So we ignore that.
                if isFirstRow == False:
                    table[row[0]] = [ [ row[1], row[2] ], [ row[3], row[4] ] ]
                isFirstRow = False
        
        final_table = mooremachine.reduceAutomata(table)

        # Write data into the output CSV file
        with open("output.csv", "w", newline = '') as csvfile:
            filewriter = csv.writer(csvfile)
            filewriter.writerow([ "PS", "NS0", "OS0", "NS1", "OS1" ])

            for key in final_table:
                output_list = [ key, final_table[key][0][0], final_table[key][0][1], final_table[key][1][0], final_table[key][1][1] ]
                filewriter.writerow(output_list)




    # If no file is mentioned as argument, accept data from terminal
    else:
        table = getData()
        final_table = mooremachine.reduceAutomata(table)
        print("")
        mooremachine.printStateTransitionTable(final_table)


if __name__ == "__main__":
    # main()
    debugProgram()
