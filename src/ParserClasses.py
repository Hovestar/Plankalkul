import copy

class ExecutionError(Exception):
    pass
class Memory:
    def __init__(self):
        self.vals = {}
    def __getitem__(self,key):
        val = self.vals[key.name]
        inds = key.indexes
        # Indexing(None,PlanType([],i))
        if len(inds)==1 and inds[0].loc == None:
            return val
        raise NotImplelentedError("This")


    def __setitem__(self,key,value):
        self.vals[key.name] = value

class Function:
    def __init__(self,name,inputs,outputs,body):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.body = body
    def __str__(self):
        return "Function("+','.join(map(str,[self.name,self.inputs,self.outputs,self.body]))+")"
    def __call__(self,mem, *args):
        mem = copy.copy(mem)
        for elem,val in zip(self.inputs.varList,args):
            mem[elem] = val
        mem, val = self.body(mem)
        return mem,list(map(mem.__getitem__,self.outputs.varList))

class VarStatement:
    def __init__(self,varList):
        # This is a bunch of variables in a row
        self.varList = varList
    def __str__(self):
        return 'VarStatement('+','.join(map(str,self.varList))+')'
    def __call__(self,mem):
        raise ExecutionError("Variable Called")

class Var:
    def __init__(self,name,indexes):
        self.name = name
        self.indexes = indexes
    def __str__(self):
        return 'Var('+str(self.name)+','+','.join(map(str,self.indexes))+')'
    def __call__(self,mem):
        return mem,mem[self]
    def __hash__(self):
        return self.name.__hash__()
    def __cmp__(self,other):
        return self.name.__cmp__(other.name)

class Statements:
    def __init__(self,stateList):
            self.stateList = stateList
    def __str__(self):
        return "Statements("+','.join(map(str,self.stateList))+")"
    def __call__(self,mem):
        for state in self.stateList:
            mem, val = state(mem)
        return mem, val

class If:
    def __init__(self,val,statement):
        self.val = val
        self.statement = statement
    def __str__(self):
        return "If("+str(self.val)+','+str(self.statement)+")"
    def __call__(self,mem):
        mem,val = self.val(mem)
        if val:
            mem, _ = self.statement(mem)
        return mem,val

class Indexing:
    def __init__(self,loc,indexType):
         self.loc = loc
         self.indexType = indexType
    def __str__(self):
        return "Indexing("+','.join(map(str,[self.loc,self.indexType]))+")"
    def __call__(self,mem):
        raise ExecutionError("Index Called")

class PlanType:
    def __init__(self,dims,name):
        self.dims = dims
        self.name = name
    def __str__(self):
        return "PlanType("+str(self.dims)+','+str(self.name)+")"
    def __call__(self,mem):
        raise ExecutionError("Type Called")

class Assignment:
    def __init__(self,var,valState):
        self.var = var
        self.valState = valState
    def __str__(self):
        return "Assignment("+','.join(map(str,[self.var,self.valState]))+")"
    def __call__(self,mem):
        mem,val = self.valState(mem)
        mem[self.var] = val
        return mem,val

class WhileLoop:
    def __init__(self):
        pass
    def __str__(self):
        return "WhileLoop"
    def __call__(self, mem, statements):
        mem, val = statements(mem)
        while(val):
            mem, val = statements(mem)
        return mem,val

class ForLoop:
    def __init__(self,mainVar,indVar):
        self.mainVar = mainVar
        self.indVar = indVar
    def __str__(self):
        return "ForLoop("+','.join(map(str,[self.mainVar,self.indVar]))+")"
    def __call__(self,mem,statement):
        arr = mem[self.mainVar]
        if isinstance(arr,int):
            arr = range(arr)
        for i in arr:
            mem[self.indVar] = i
            mem,val = statement(mem)
        return mem, val

class LoopState:
    def __init__(self,loopType,state):
        self.loopType = loopType
        self.statement = state
    def __str__(self):
        return "LoopState("+','.join(map(str,[self.loopType,self.statement]))+")"
    def __call__(self,mem):
        return self.loopType(mem,self.statement)

class Num:
    def __init__(self,val):
        self.val = int(val)
    def __str__(self):
        return "Num("+str(self.val)+")"
    def __call__(self, mem):
        return mem, self.val

class Bool:
    def __init__(self,val):
        self.val = bool(val)
    def __str__(self):
        return "Bool("+str(self.val)+")"
    def __call__(self, mem):
        return mem, self.val

class Not:
    def __init__(self,state):
        self.state = state
    def __str__(self):
        return "Not("+str(self.state)+")"
    def __call__(self,mem):
        mem,val = self.state(mem)
        return mem, not val

class Compare:
    def __init__(self,op,arith1,arith2):
        self.op = op
        self.arith1 = arith1
        self.arith2 = arith2
    def __str__(self):
        return "Compare("+','.join(map(str,[self.op,self.arith1,self.arith2]))+")"
    def __call__(mem,self):
        mem, val1 = self.arith1(mem)
        mem, val2 = self.arith2(mem)
        if op == '<':
            return mem, val1 < val2
        if op == '>':
            return mem, val1 > val2
        if op == '=':
            return mem, val1 == val2

class Arith:
    def __init__(self,op,exp1,exp2):
        self.op = op
        self.exp1 = exp1
        self.exp2 = exp2
    def __str__(self):
        return "Arith("+','.join(map(str,[self.op,self.exp1,self.exp2]))+")"
    def __call__(self, mem):
        mem,val1 = self.exp1(mem)
        mem,val2 = self.exp2(mem)
        return mem, self.op(val1,val2)

class Minus:
    def __init__(self):
        pass
    def __str__(self):
        return "Minus"
    def __call__(self,val1,val2):
        return val1-val2

class Plus:
    def __init__(self):
        pass
    def __str__(self):
        return "Plus"
    def __call__(self,val1,val2):
        return val1+val2

class Div:
    def __init__(self):
        pass
    def __str__(self):
        return "Div"
    def __call__(self,val1,val2):
        return val1/val2

class Times:
    def __init__(self):
        pass
    def __str__(self):
        return "Times"
    def __call__(self,val1,val2):
        return val1*val2
