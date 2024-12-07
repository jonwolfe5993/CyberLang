from textx import metamodel_from_file

#Load textX metamodel from .tx file
metaModel = metamodel_from_file('cyberpunk_lang.tx')

#Load input file
fileName = input('Enter the file name: ')
try:
    with open(fileName) as f:
        inputCode = f.read()
except FileNotFoundError:
    print('File not found')
    exit()
#Parse the code into a model
model = metaModel.model_from_str(inputCode)

#Varmap to store variable names and their values
varMap = {}

#Function for evaluating expressions
def evalExpression(expr):
    #Get left, right, and operator values
    if expr.__class__.__name__ == 'Comparison':
        left = evalExpression(expr.left)
        right = evalExpression(expr.right)
        relOp = expr.relOp
        #Create comparison string and evaluate
        compString = f'{left} {relOp} {right}'
        return eval(compString)
    try:
        return eval(expr, varMap)        
    except:
        return expr
    
#Function to execute for loops
def executeForLoop(forLoop):
    #Get loop variable, start, and end values
    loopVar = forLoop.var
    start = evalExpression(forLoop.start)
    end = evalExpression(forLoop.end)
    #Execute the loop
    for value in range(start, end + 1):
        #Assign loop variable to the current value
        varMap[loopVar] = value  
        #Execute each statement in the body
        for statement in forLoop.forBody:
            executeStatement(statement) 

#Function to execute while loops
def executeWhileLoop(whileLoop):
    while evalExpression(whileLoop.condition):
        for statement in whileLoop.whileBody:
            executeStatement(statement)

#Function to execute if statements
def executeIfStatement(ifStatement):
    #Evaluate the condition
    if evalExpression(ifStatement.condition):
        for statement in ifStatement.ifBody:
            executeStatement(statement)
        return
    for elseIfBlock in ifStatement.elseIfBlocks:
        if evalExpression(elseIfBlock.condition):
            for statement in elseIfBlock.elseIfBody:
                executeStatement(statement)
            return
    if ifStatement.elseBody:
        executeStatement(ifStatement.elseBody)

#Function to execute statements in program
def executeStatement(statement):
    #Handle variable declaration
    if statement.__class__.__name__ == 'VarDeclaration':
        value = evalExpression(statement.value)
        varMap[statement.name] = value
    #Handle print statement
    elif statement.__class__.__name__ == 'PrintStatement':
        value = evalExpression(statement.expr)
        print(value)
    #Handle for loop
    elif statement.__class__.__name__ == 'ForLoop':
        executeForLoop(statement)
    #Handle if statement
    elif statement.__class__.__name__ == 'IfStatement':
        executeIfStatement(statement)
    #Handle while loop
    elif statement.__class__.__name__ == 'WhileLoop':
        executeWhileLoop(statement)
        
#Execute each statement in the model
for statement in model.statements:
    executeStatement(statement)