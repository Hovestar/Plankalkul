#!/usr/bin/python3
import ParserClasses as pClass

class ParseError(Exception):
    pass

def pullConst(s,value):
    s = s.lstrip()
    if s[:len(value)] != value:
        raise ParseError("Expected '"+value+"'")
    return s[len(value):]
def parseFunction(s):
    """
    Function ::= Decl Statement
    Decl ::= Name varStatement '=>' (var | varStatement)
    """
    name,s = parseName(s)
    inputs, s = parseVarState(s)
    s = pullConst(s,'=>')
    try:
        outputs, s = parseVarState(s)
    except ParseError:
        outputs, s = parseVar(s)
        outputs = pClass.VarStatement([outputs])
    body,s = parseStatement(s)
    return pClass.Function(name,inputs,outputs,body), s
def parseName(s):
    """
    Name ::= ALPHANUMS
    """
    string = s.lstrip()
    i = 0
    while len(string)>i and string[i].isalnum():
        i+=1
    if(i!=0):
        return string[:i],string[i:]
    raise ParseError("Expected at least one letter")
def parseVarState(s):
    """
    varStatement ::= '(' var {',' var} ')'
    """
    s = pullConst(s,'(')
    end = []
    tmp,s = parseVar(s)
    end.append(tmp)
    def helper(exps,s):
        s = s.lstrip()
        if s == "" or s[:1] != ',':
            return exps,s
        s =  s[1:]
        try:
            val,s = parseVar(s)
        except ParseError:
            return exps,s
        return helper(exps+[val],s)
    end,s = helper(end,s)
    s = pullConst(s,')')
    return pClass.VarStatement(end),s
def parseVar(s):
    """
    var ::= ('R'|'V'|'Z') NUMS indexType {indexType} | indexvar
    """
    try:
        return parseIndexVar(s)
    except ParseError:
        pass
    s = s.lstrip()
    if s[:1] not in 'RVZ':
        raise ParseError("Expected a variable name (RVZ)")
    name = s[:1]
    s = s[1:]
    num, s = parseNUM(s)
    name += num
    ind,s = parseIndexType(s)
    def helper(exps,s):
        s = s.lstrip()
        if s == "":
            return exps,s
        try:
            val,s = parseIndexType(s)
        except ParseError:
            return exps,s
        return helper(pClass(exps,val),s)
    tmp = pClass.Var(name,ind)
    return helper(tmp,s)
def parseNUM(s):
    """
    NUMS
    """
    string = s.lstrip()
    i = 0
    while len(string)>i and string[i].isdigit():
        i+=1
    if(i!=0):
        return string[:i],string[i:]
    raise ParseError("Expected at least one digit")
def parseStatement(s):
    """
    Statement ::= (if | Loop | '{' {Statement}'}' | Assignment) NEWLINE
    """
    try:
        end,s = parseIf(s)
        return end,s.lstrip()
    except ParseError:
        pass
    try:
        end,s = parseLoop(s)
        return end,s.lstrip()
    except ParseError:
        pass
    try:
        end,s = parseAssignment(s)
        return end,s.lstrip()
    except ParseError:
        pass
    s = pullConst(s,'{')
    def helper(exp,s):
        s = s.lstrip()
        if s == "":
            return exp,s
        try:
            tmp,s = parseStatement(s)
            return helper(exp+[tmp],s)
        except ParseError:
            return exp,s
    end,s = helper([],s)
    s = pullConst(s,'}')
    return pClass.Statements(end),s
def parseIndexVar(s):
    """
    indexvar ::= LOWERCHAR {LOWERCHAR}
    """
    string = s.lstrip()
    i = 0
    while len(string)>i and string[i].islower():
        i+=1
    if(i>0 and string[:i] not in "ibfc"):
        return pClass.Var(string[:i],pClass.Indexing(None,pClass.PlanType([],'i'))),string[i:]
    raise ParseError("Expected at least one digit")
def parseIf(s):
    """
    if ::= value '->' statement
    """
    val,s = parseValState(s)
    s = pullConst(s,'->')
    state,s = parseStatement(s)
    return pClass.If(val,state),s
def parseIndexType(s):
    """
    indexType ::= '[' [arith] ':' type ']'
    """
    s = pullConst(s,'[')
    try:
        opt,s = parseArith(s)
    except ParseError:
        opt = None
    s = pullConst(s,':')
    indexType,s = parseType(s)
    s = pullConst(s,']')
    return pClass.Indexing(opt,indexType),s
def parseAssignment(s):
    """
    Assignment ::= valState '=>' var
    """
    valState,s = parseValState(s)
    s = pullConst(s,'=>')
    var, s = parseVar(s)
    return pClass.Assignment(var,valState),s
def parseLoop(s):
    """
    Loop ::= loopname Statement
    loopname ::= 'W' | 'W1' '(' arith ')' '=>' var
    """
    try:
        s = pullConst(s,"W1")
        s = pullConst(s,"(")
        var1,s = parseArith(s)
        s = pullConst(s,")")
        s = pullConst(s,"=>")
        var2,s = parseVar(s)
        loopType = pClass.ForLoop(var1,var2)
    except ParseError:
        s = pullConst(s,"W")
        loopType = pClass.WhileLoop()
    state,s = parseStatement(s)
    return pClass.LoopState(loopType,state),s
def parseValue(s):
    """
    value ::= NUM | var | '#t'| '#f' | '(' valstate ')'
    """
    try:
        val,s = parseNUM(s)
        return pClass.Num(int(val)),s
    except ParseError:
        pass
    try:
        return parseVar(s)
    except ParseError:
        pass
    try:
        s=pullConst(s,"#t")
        return pClass.Bool(True)
    except ParseError:
        pass
    try:
        s=pullConst(s,"#f")
        return pClass.Bool(False)
    except ParseError:
        pass
    s = pullConst(s,'(')
    state,s = parseValState(s)
    s = pullConst(s,')')
    return state,s
def parseType(s):
    """
    type ::= {indexvar '*'} ('i'|'b'|'f'|'c'|'X'[NUM])
    """
    def helper(exp,s):
        s = s.lstrip()
        if s == "":
            return exp,s
        try:
            tmp, s = parseIndexVar(s)
            exp.append(tmp)
            s = pullConst(s,"*")
        except ParseError:
            return exp,s
        return helper(exp,s)
    dims,s = helper([],s)
    for typ in 'ibfc':
        try:
            s = pullConst(s,typ)
            return pClass.PlanType(dims,typ),s
        except ParseError:
            pass
    s = pullConst(s,'X')
    try:
        num,s = parseNUM(s)
        typ = 'X' + num
    except ParseError:
        typ = 'X'
    return pClass.PlanType(dims,typ),s
def parseValState(s):
    """
    valstate ::= (arith [('<'|'>'|'=') arith] | '!' valState)
    """
    try:
        tmps = s
        tmps = pullConst(tmps,'!')
        state,tmps = parseValState(tmps)
        return pClass.Not(state),tmps
    except ParseError:
        pass
    arith,s = parseArith(s)
    try:
        tmps = s
        op = None
        for tmpop in "<>=":
            try:
                tmps = pullConst(tmps,tmpop)
                op = tmpop
                break
            except ParseError:
                pass
        if(op == None):
            raise ParseError("Expected Comparison Op")
        arith2,tmps = parseArith(tmps)
        return pClass.Compare(op,arith,arith2),tmps
    except ParseError:
        pass
    return arith,s
def parseArith(s):
    """
    arith ::= arithp
    arithp ::= aritht {('+'|'-') aritht}
    """
    def helper(exp,s):
        tmps = s
        op = None
        try:
            tmps = pullConst(tmps,'+')
            op = pClass.Plus()
        except ParseError:
            try:
                tmps = pullConst(tmps,'-')
                op = pClass.Minus()
            except ParseError:
                return exp,s
        try:
            val, tmps = parseArithT(tmps)
            return helper(pClass.Arith(op,exp,val),tmps)
        except ParseError:
            return exp,s
    exp1,s = parseArithT(s)
    tmp = helper(exp1,s)
    return tmp
def parseArithT(s):
    """
    aritht ::= value {('*'|'/') value}
    """
    def helper(exp,s):
        op = None
        try:
            s = pullConst(s,'*')
            op = pClass.Times()
        except ParseError:
            try:
                s = pullConst(s,'/')
                op = pClass.Div()
            except ParseError:
                return exp,s
        try:
            val, s = parseValue(s)
            return helper(pClass.Arith(op,exp,val),s)
        except ParseError:
            pass
    exp1,s = parseValue(s)
    return helper(exp1,s)

if __name__ == "__main__":
    import sys
    fname = sys.argv[1]
    with open(fname,'r') as f:
        body = f.read()
    func,s = parseFunction(body)
    print(func)
    mem, val = func(pClass.Memory(),15)
    print(mem)
    print(val)
