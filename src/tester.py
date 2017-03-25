#!/usr/bin/python3
import Parser
import ParserClasses
import traceback

def loadFile(name):
    with open(name+'.plan','r') as f:
        body = f.read()
    with open(name+'.res','r') as f:
        tests = f.readlines()
    insOuts = map(lambda x: x.split('=>'),tests)
    try:
        code,rem = Parser.parseFunction(body)
    except Parser.ParseError as e:
        print("Issue: Code did not parse. This is the error:\n {}".format(e))
        return
    if(rem.strip() != ""):
        print("Issue: Code not eaten this left:\n {}".format(rem.strip()))
    for valIn,valOut in insOuts:
        try:
            mem,testVal = code(ParserClasses.Memory(),*eval(valIn))
        except ParserClasses.ExecutionError as e:
            print("Issue: Code failed in execution with error: \n{}".format(e))
            continue
        print(mem)
        valOut = eval(valOut)
        if(testVal!=valOut):
            print("Issue: {} != {}".format(testVal,valOut))
        else:
            print("Good: {} == {}".format(testVal,valOut))

if __name__== "__main__":
    directory = "../Tests/"
    files = ['03']
    for fname in files:
        loadFile(directory+fname)
