from functools import reduce
#'(+ 1 2 (+ 2 3))'  -> ['+', 1, 2, ['+', 2, 3]]
#              parsing
             
             
 
#'(car (quote       (+ 42 13)))' -> ['(','car','(','quote','(','+','42','13',')',')',')']
 
class LispInterException(ValueError):pass
 
def tokenize(line):
    word_holder = ''
    tokens = []
    for i in line:
        if i == '(' or i == ')':
            if word_holder == '':
                tokens.append(i)
            else:
                tokens.append(word_holder)
                word_holder = ''
                tokens.append(i)
        elif i == ' ':
             if word_holder != '':
                tokens.append(word_holder)
                word_holder = ''
        else:
            word_holder += i
    if word_holder != '':
        tokens.append(word_holder)
    return tokens
 
 
 
 
 
#tokens: '(','42','(','13',')','666',')'
#stack: '(','42',['13']
 
def parse(array):             #via stack
    stack = []
    for i in array:
        if i != ')':
            if i.isdigit():
                stack.append(int(i))
            else:
                stack.append(i)
        else:
            resulting_list = []
            while stack and stack[-1] != '(':
                resulting_list.append(stack.pop())
            if stack:
                stack.pop()
            else:
                raise LispInterException("Exception: Missing opening skobochka")
            stack.append(resulting_list[::-1])
    return stack.pop()
 
 
def to_str(final_list, count, result): #making result look like lisp code
    print(final_list)
    if count == len(final_list):
        return result[:-1] + ') '
    else:
        if final_list[count] == '\'' or final_list[count] == ',':
            return to_str(final_list, count + 1, result)
        elif type(final_list[count]) == list:
            return to_str(final_list, count + 1, result + to_str(final_list[count], 0, '('))
        elif type(final_list[count]) == int:
            return to_str(final_list, count + 1, result + str(final_list[count]) + ' ')
        else:
            return to_str(final_list, count + 1, result + final_list[count] + ' ')
 
global_d = {}
local_d = {}
 
def my_eval(expr, global_d, local_d):
    if type(expr) == int: #displaying int number
        return expr
 
    elif expr == '#t' or expr == '#f': #displaying true/false
        return expr
   
    elif expr == 'global': #displaying global dict
        return global_d
 
    elif expr == 'clear global': #Clearing global dict
        global_d.clear()
        return 'global dictionary is cleared'
 
    elif expr == 'exit': #exit key
        exit('Exiting terminal')
 
    elif type(expr) == str: #Calling variable
        if expr in local_d:
            return local_d[expr]
        elif expr in global_d:
            return global_d[expr]
        else:
            raise LispInterException("Exception: Variable is not defined")
   
    elif type(expr) == list and expr[0] == '+':  #plus
        #print('plusuu')
        return reduce(lambda x,y: x + my_eval(y, global_d, local_d), expr[1:], 0)
       
    elif type(expr) == list and expr[0] == '-': #minus
        #print('minusuu')
        if len(expr) == 2: #Lisp returns -x if it's (- x)
            return my_eval(expr[1], global_d, local_d) * -1
        else:
            return reduce(lambda x,y: x - my_eval(y, global_d, local_d), expr[1:], 0)
       
    elif type(expr) == list and expr[0] == '*': #multiply
        #print('umnojau')
        return reduce(lambda x,y: x * my_eval(y, global_d, local_d), expr[1:], 1)
       
    elif type(expr) == list and expr[0] == '/': #divide
        #print('delu')
        if len(expr) == 1:
            return 'Error: You can\'t call eval for the empty division symbol'
        else:
            return reduce(lambda x,y: x / my_eval(y, global_d, local_d), expr[1:])
 
    elif type(expr) == list and expr[0] == 'null': #null
        #print('null func')
        if my_eval(expr[1], global_d, local_d):
            return '#f'
        else:
            return '#t'
 
    elif type(expr) == list and expr[0] == '=': #equal
        #print('equal func')
        if my_eval(expr[1], global_d, local_d) == my_eval(expr[2], global_d, local_d):
            return '#t'
        else:
            return '#f'
 
    elif type(expr) == list and expr[0] == '/=': #not equal
        #print('not equal func')
        if my_eval(expr[1], global_d, local_d) != my_eval(expr[2], global_d, local_d):
            return '#t'
        else:
            return '#f'
 
    elif type(expr) == list and expr[0] == '>': #more than
        #print('more than func')
        if my_eval(expr[1], global_d, local_d) > my_eval(expr[2], global_d, local_d):
            return '#t'
        else:
            return '#f'
 
    elif type(expr) == list and expr[0] == '<': #less than
        #print('less than func')
        if my_eval(expr[1], global_d, local_d) < my_eval(expr[2], global_d, local_d):
            return '#t'
        else:
            return '#f'
 
    elif type(expr) == list and expr[0] == '>=': #more or equal than
        #print('more or equal than func')
        if my_eval(expr[1], global_d, local_d) >= my_eval(expr[2], global_d, local_d):
            return '#t'
        else:
            return '#f'
 
    elif type(expr) == list and expr[0] == 'if': #if function
        #print('if func')
        if my_eval(expr[1], global_d, local_d) == '#t':
            return my_eval(expr[2], global_d, local_d)
        else:
            return my_eval(expr[3], global_d, local_d)
    
    elif type(expr) == list and expr[0][0] == 'if' : #lambda if function
        #print('lambda if func')
        if my_eval(expr[0][1], global_d, local_d) == '#t':
            return my_eval([expr[0][2], expr[1]], global_d, local_d)
        else:
            return my_eval([expr[0][3], expr[1]], global_d, local_d)
 
    elif type(expr) == list and expr[0] == '<=': #less or equal than
        #print('less or equal func')
        if my_eval(expr[1], global_d, local_d) <= my_eval(expr[2], global_d, local_d):
            return '#t'
        else:
            return '#f'
 
    elif type(expr) == list and expr[0] == 'cons':  #car + cdr (cons 1 2) -> '(1.2) | (cons 1 '(b c d)) -> '(1 b c d)
        #print('cons func')
        a = my_eval(expr[1], global_d, local_d)
        b = my_eval(expr[2], global_d, local_d)
        if type(b) != list:
            raise LispInterException("Exception: this intepreter can't handle pairs")
        else:
            return [a] + b
 
    elif type(expr) == list and expr[0] == 'list': #Creating lists
        #print('list func')
        return [my_eval(i, global_d, local_d) for i in expr[1:]]
 
    elif type(expr) == list and expr[0] == 'car': #head of list
        #print('car func')
        return my_eval(expr[1], global_d, local_d)[0]
 
    elif type(expr) == list and expr[0] == 'cdr': #list without head
        #print('cdr func')
        return my_eval(expr[1], global_d, local_d)[1:]
 
    elif type(expr) == list and expr[0] == 'quote': #quoting expression into list
        #print('quote  func')
        return expr[1]
 
    elif type(expr) == list and expr[0] == 'let': #local namespace parallel (let ((var1 value1) (var2 value2)) body)
        #print('let func')
        local_d_new = local_d.copy() #переносим все предыдущие значения в новый дикт, так как надо изолировать дикт в параметрах подаваемый на данный шаг рекурсии и подаваемый на следующий шаг рекурсии
        for i in expr[1]: #Заполнение словаря новыми переменными из текущей итерации рекурсии
            local_d_new[i[0]] = my_eval(i[1], global_d, local_d)
        return my_eval(expr[2], global_d, local_d_new)
   
    elif type(expr) == list and expr[0] == 'let*': #local namespace one after another (let* ((var1 value1) (var2 value2)) body)
        for i in expr[1]: #Создание новой копии словаря после каждого добавления переменной, чтобы в последующих шагах, если использовалась перезаданная переменная из прошлого шага, было использовано новое значение
            local_d = local_d.copy()
            local_d[i[0]] = my_eval(i[1], global_d, local_d)
        return my_eval(expr[2], global_d, local_d)
   
    elif type(expr) == list and expr[0][0] == 'lambda': #making lambda expression ((lambda (params) (body)) params-value)
        #print('lambda func')
        local_d = local_d.copy()
        actuals = [my_eval(i, global_d, local_d) for i in expr[1:]]
        for i,j in enumerate(expr[0][1]):
            local_d[j] = actuals[i]
        return (my_eval(expr[0][2], global_d, local_d))
 
    elif type(expr) == list and expr[0] == 'define':
        #print('define func')
        if type(expr[1]) == str: #для присваивания атому
            global_d[expr[1]] = my_eval(expr[2], global_d, local_d)
            return 'defined variable ' + expr[1]
        else: #Для присваивания функции
            if not all(isinstance(n, str) for n in expr[1]):
                raise LispInterException('Exception: define - not an identifier, identifier with default, or keyword for procedure argument')
            else:
                global_d[expr[1][0]] = [['lambda', expr[1][1:], expr[2]]]
                return 'defined function ' + str(expr[1][0])
 
    else:
        if expr[0] in local_d:
            print('searching in local')
            return my_eval(global_d[expr[0]] + expr[1:], global_d, local_d)
        elif expr[0] in global_d:
            print('searching in global')
            return my_eval(global_d[expr[0]] + expr[1:], global_d, local_d)
        else:
            raise LispInterException('Exception: you gave some bullshit to the eval')
 
 
#Прогнать парсинг с отладочной печатью
#Написать функцию самостоятельно перегона из стринга в инт, из инта в стринг
#Доделать всю арифметику, а также car cdr quote cons if
 
# REPL = Read Eval Print Loop
 
def repl():
    global_d = {}
    while True:
        expr = input("MICRO-LISP: ")
        try:
            result = (my_eval(parse(tokenize(expr)), global_d, {}))
            if type(result) == int:
                print(my_eval(parse(tokenize(expr)), global_d, {}))
            else:
                print(to_str(my_eval(parse(tokenize(expr)), global_d, {}), 0, '(')[:-1])
        except LispInterException as e:
            print (e)
       
repl()
 
#Добавить в необходимые места ексепшены (например, не хватает открывающейся скобки)
#Сделать Define
#Реализовать специальную конструкцию If, чтобы експрешион ((if (= 1 1) (lambda (x) (+ 1 x)) (lambda (y) (+ 2 x))) 42)   выполнялся (прописать myeval...)
#Реализовать интерпретатор без рекурсии