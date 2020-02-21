#1 1 2 3 5 8 13 21 34
#1 2 3 4 5 6
 
def fib_slow(number):
    if number in [1, 2]:
        return 1
    else:
        return fib_slow(number - 2) + fib_slow(number - 1)
   
cache = {1:1, 2:1}
 
def fib_with_cache(number):
    if number in cache:
        return cache[number]
    else:
        cache[number] = fib_with_cache(number - 2) + fib_with_cache(number - 1)
        return cache[number]
       
 
def fib_with_cache_inside(number, cache = {1:1, 2:1}):   # Algol own-variables, stactic
    if number in cache:
        return cache[number]
    else:
        cache[number] = fib_with_cache_inside(number - 2) + fib_with_cache_inside(number - 1)
        return cache[number]
       
class FibDict(dict):
   
    def __init__(self):
        self[1] = 1
        self[2] = 1
   
    def __missing__(self, x):
        self[x] = self[x - 2] + self[x - 1]
        return self[x]
       
fibo = FibDict()
 
 
 
 
# memoization, memoize - функция декоратор
 
def memoize(function): #function - функция от 1 аргумента в данном случае
    cache = {}
    def memoized_fucntion(x):
        if x in cache:
            return cache[x]
        else:
            cache[x] = function(x)
            return cache[x]
    return memoized_fucntion
   
def tracing(function):
    def traced_function(x):
        print(function.__name__ + '(' + str(x) + ')')
        result = function(x)
        print('result ', result)
        return result
    return traced_function
 
def tracing_any(function):
    def traced_function(*args):
        print(function.__name__, ''.join(str(i) for i in args)) #лист компрехеншн + джоин для дз, чтоб избавиться от запятых лишних
        result = function(*args)
        print('result', result)
        return result
    return traced_function
   
@tracing_any
@memoize #применение декоратора, синт. сахар вместо строки 62
def fib_slow(number):
    if number in [1, 2]:
        return 1
    else:
        return fib_slow(number - 2) + fib_slow(number - 1)
   
#fib_slow=memoize(fib_slow)
print(fib_slow(35))
 
#ДЗ - комментарий в трейсэни, применить Traceany к my_eval и к my_apply (нужно трассировать лишь то, что относится к интерпретатору) (заставить работать (define (foo) (lambda (x) (+ 1 x))) )