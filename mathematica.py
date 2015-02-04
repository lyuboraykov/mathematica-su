import re
import sys

FUNCTIONS = ['log', 'pow', 'sin', 'cos', 'tg', 'cotg', 'sqrt']
OPERATORS = ['+', '-', '*', '/']

def prepare_expression(expression):
   '''
   expression - a string with the infix notation of the expression
   It converts it to a format used by the other functions.
   All tokens are separated by a single whitespace.
   '''
   for operator in OPERATORS:
      prepared_expression = prepared_expression.replace(operator,' ' + operator + ' ')
      
   prepared_expression = prepared_expression.replace("(", " ( ")
   prepared_expression = prepared_expression.replace(")", " ) ")
   prepared_expression = prepared_expression.replace(")", " ) ")
   prepared_expression = re.sub(" +", " ", expression)
   for function in FUNCTIONS:
      prepared_expression = prepared_expression.replace(function + ' ', function)
   return prepared_expression


class Operator:
   def __init__(self, precedence, sign):
      this.precedence = precedence
      this.sign = sign

def convert_to_postfix_notation(infixTokens):
   pass

def is_number(token):
   pass

def is_function(token):
   pass

def is_operator(token):
   pass

def calculate_postfix_notation(postfix_notation):
   pass

def calculate_function(token):
   pass

if __name__ == '__main__':
   while True:
      expression = raw_input("Enter expression: ")
      if expression == "exit":
         break
      modified_expression = prepare_expression(expression)
      print modified_expression