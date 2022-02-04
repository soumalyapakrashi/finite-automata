# Finite Automata

This program as of its current implementation, performs Moore Reduction. Further informations are as follows:

## Contents

1. [Detailed Scope](https://github.com/soumalyapakrashi/finite-automata#detailed-scope)
2. [Usage Details](https://github.com/soumalyapakrashi/finite-automata#usage-details)
3. [Future Scope](https://github.com/soumalyapakrashi/finite-automata#future-scope)

## Detailed Scope

A Moore machine is the one in which the next state depends on both the current state as well as the current input. Here, we take a state transition table as input of such a machine. That state transition table can be non-optimal, it can have redundant states, it can also have missing values (as is the case with _partially specified machines_). This program converts such machines into a reduced _completely specified machine_ and also standardizes it. Standardization is important because different people can design the same machine in different ways and if they do not follow a set of rules, it can become very difficult to verify and validate different designs. Standardization ensures that it the machine is not having any redundant states, then all the machines will have the same definition.

## Usage Details

This program takes as input a _completely specified machine_ or a _partially specified machine_ which can have redundant states or is not standardized.

The default way to invoke the program is as follows:
```shell
python main.py
```
This will take the transition table as input from the user in the **Terminal** itself.

Input can also be given from a CSV file. For a sample CSV file, see [input.csv](./input.csv). In this case, the program can be invoked as
```shell
python main.py -f input.csv
```

The program can also show detailed steps about how the calculations are done and what assumptions are made. For this, add the *verbose* flag to the program.
```shell
python main.py --file input.csv --verbose
```

The help message can be displayed as follows:
```shell
python main.py --help
```

In all the cases, an output file is produced which contains the final state transition table after reduction and standardization. An example can be found in [output.csv](./output.csv).

## Future Scope

The program as of its current implementation, only supports two input symbols (0 and 1) and two output symbols (0 and 1). This can be extended to have support for multiple input and output symbols.
