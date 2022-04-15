# Y-86-64 Machine Simulator

Y-86-64 is a minimal instruction set architecture designed for "Computer Systems: A Programmer's Perspective" by Randal E. 
Bryant and David O'Hallaron. Toy simulates a system with only main memory and a CPU, interprets Y-86-64 instructions, 
runs them on the system, and displays the state of memory. 

### Syntax changes
I've made some small changes to the syntax of Y86_64 source code concering labels and whitespace. 

1. Operands do not need to be comma seperated, white space will do. The following are all acceptable: 
* `addq %rax, %rbx`
* `addq %rax,%rbx`
* `addq %rax %rbx`

2. Labels do not have to be followed by colons when defined if they are on their own line. 
3. Labels must consist only of alphebetical characters. 

### How to use

Run the python file 'Y86-64.py' in the src folder supplying a Y86_64 source code file as a command line argument.
It will print the final state of the program counter, registers, system status, and flags. The state of main
memory will be written to a text file called 'final_memory_state.txt' in the working directory.