#!/usr/bin/python3
import sys
import Parser
import ParserClasses

def main(argv):
    if(len(argv) != 3):
        print()
        return
    fname = argv[1]
    inputs = argv[2]
    with open(fname,'r') as f:
        body = f.read()
    func,s = Parser.parseFunction(body)
    ins = eval(inputs)
    mem = ParserClasses.Memory()
    _, outs = func(mem, *ins)
    for i in outs:
        print(i)

if __name__ == "__main__":
    main(sys.argv)
