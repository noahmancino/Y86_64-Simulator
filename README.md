# Toy: A Y-86-64 Machine Simulator

Y-86-64 is a minimal instruction set architecture designed for "Computer Systems: A Programmer's Perspective" by Randal E. 
Bryant and David O'Hallaron. Toy simulates a system with only main memory and a CPU, interprets Y-86-64 instructions, 
runs them on the system, and displays the state of memory. 

### Syntax changes
I've made some small changes to the syntax of Y86_64 source code concering labels and whitespace. 

1. Operands do not need to be comma seperated, white space will do. The following are all acceptable: 
* `addq %rax, %rbx`
* `addq %rax,%rbx`
* `addq %rax %rbx`
2. Colons are treated the same as newlines.

3. Labels do not have to be followed by colons when defined.
4. Labels must consist soley of alphebetical characters. 