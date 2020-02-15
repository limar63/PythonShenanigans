def my_eval(expr, env):
    if is_selfeval(expr):
        return expr
 
    elif is_variable(expr):
        return search_for_var(expr, env)
 
    elif is_command(expr):
        return command(expr)
 
    elif is_quoted(expr):
        return text_of_quote(expr)
 
    elif is_assignment(expr):
        return eval_assingment(expr, env)
 
    elif is_definition(expr):
        return eval_definition(expr, env)
 
    elif is_if(expr):
        return eval_if(expr, env)
 
    elif is_lambda(expr):
        return make_procedure(lambda_parameters(expr), lambda_body(expr), env)
   
    elif is_application(expr):
        return apply(my_eval(operator(expr), env), list_of_values(operands(expr), env))
 
    else:
        raise LispInterException("Exception: unknown type of expression")
 
def apply(procedure, arguments):
    if is_primitive(procedure):
        return apply_primitive_proc(procedure, arguments)
 
    elif is_compound(procedure):
        return eval_sequence(procedure_body(procedure), extend_environment(procedure_parameters(procedure), arguments, procedure_environment(procedure)))
 
    else:
        raise LispInterException("Exception: unknown type of procedure -- APPLY ", procedure)
 
def list_of_values(expressions, env): #Evaluating all the arguments and returning it as a list of values
    return [my_eval(i, env) for i in expressions]
 
def eval_if(expr, env):
    if my_eval(if_predicate(expr), env):
        my_eval(if_consequent(expr), env)
    else:
        my_eval(if_alternative(expr), env)
 
def eval_sequence(expressions, env):
    if check_if_last_exp(expressions):
        return my_eval(first_exp(expressions), env)
    else:
        my_eval(first_exp(expressions), env)
        return (eval_sequence(rest_exp(expressions), env)

def eval_assingment(expression, env): #Variable Assignment (Changing a value to a new one)
    set_variable_value!(assignment_variable(expression), my_eval(assignment_value(expression), env), env)
    return 'Ok!'

def eval_definiton(expression, env): #Variable Definition (Creating a new variable)
    define_variable!(definition_variable(expression), my_eval(definition_value(expression), env), env)
    return 'Ok!'

