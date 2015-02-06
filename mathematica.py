#!/usr/bin/env python

import re
import sys
import queue
import math
from collections import deque

class Operator:
   def __init__(self, sign, precedence):
      self.sign = sign
      self.precedence = precedence

FUNCTIONS = ['log', 'pow', 'sin', 'cos', 'tg', 'cotg', 'sqrt']
OPERATORS = [Operator('+', 10), Operator('-', 10), Operator('*', 20), Operator('/', 20)]
CONSTANTS = {
   'E': math.e,
   'PI': math.pi
}

def calculate_expression(expression):
   '''Calculates infix notation'''
   infix_tokens = get_tokens_from_infix_notation(expression)
   postfix_notation_tokens = convert_to_postfix_notation(infix_tokens)
   return calculate_postfix_notation(postfix_notation_tokens)

def prepare_expression(expression):
   '''
   Converts the expression into a format used by the other functions.
   All tokens are separated by a single whitespace.
   expression - a string with the infix notation of the expression
   '''
   prepared_expression = expression
   for operator in OPERATORS:
      prepared_expression = prepared_expression.replace(operator.sign, ' ' + operator.sign + ' ')
   for key in CONSTANTS.keys():
      prepared_expression = prepared_expression.replace(key, str(CONSTANTS[key]))
   prepared_expression = prepared_expression.replace('(', ' ( ')
   prepared_expression = prepared_expression.replace(')', ' ) ')
   prepared_expression = re.sub(' +', ' ', prepared_expression)
   prepared_expression = prepared_expression.strip()
   for function in FUNCTIONS:
      prepared_expression = prepared_expression.replace(function + ' ', function)
   return prepared_expression

def get_tokens_from_infix_notation(infix_notation):
   '''Returns an array of tokens separated from the prepared notation'''
   tokens = []
   token_beginning_index = 0
   is_a_function = False
   function_parantheses_count = 0
   for i, character in enumerate(infix_notation):
      if 'a' <= character <= 'z' and not is_a_function:
         is_a_function = True
         token_beginning_index = i
      elif character == '(' and is_a_function:
         function_parantheses_count += 1
      elif character == ')' and is_a_function:
         function_parantheses_count -= 1
         if function_parantheses_count == 0:
            is_a_function = False
            tokens.append(infix_notation[token_beginning_index:i + 1])
      elif character == ' ' and not is_a_function:
         tokens.append(infix_notation[token_beginning_index:i])
         token_beginning_index = i + 1
      elif i == len(infix_notation) - 1:
         tokens.append(infix_notation[token_beginning_index:i + 1])
   return tokens

def convert_to_postfix_notation(infix_tokens):
   '''Returns the postfix notation of the tokens'''
   outputQueue = deque()
   operatorStack = []
   postfix_notation = ''
   for token in infix_tokens:
      if is_number(token) or is_function(token):
         outputQueue.append(token)
      if is_operator(token):
         while len(operatorStack) > 0 and is_operator(operatorStack[-1]):
            current_operator_precedence = get_operator_precedence_by_sign(token)
            top_operator_precedence = get_operator_precedence_by_sign(operatorStack[-1])
            if current_operator_precedence <= top_operator_precedence:
               outputQueue.append(operatorStack.pop())
            else:
               break
         operatorStack.append(token)
      if token == '(':
         operatorStack.append(token)
      if token == ')':
         while len(operatorStack) > 0 and operatorStack[-1] != '(':
            outputQueue.append(operatorStack.pop())
         operatorStack.pop()
      if len(operatorStack) > 0 and is_function(operatorStack[-1]):
         outputQueue.append(operatorStack.pop())
   while len(operatorStack) > 0:
      outputQueue.append(operatorStack.pop())
   return list(outputQueue)

def is_number(token):
   try:
      float(token)
      return True
   except ValueError:
      return False

def is_function(token):
   for function in FUNCTIONS:
      if function in token:
         return True
   return False

def is_operator(token):
   return token in [operator.sign for operator in OPERATORS]

def get_operator_precedence_by_sign(sign):
   for operator in OPERATORS:
      if operator.sign == sign:
         return operator.precedence
   return 0

def calculate_postfix_notation(postfix_notation_tokens):
   numbers = []
   for token in postfix_notation_tokens:
      if is_number(token):
         numbers.append(float(token))
      if is_operator(token):
         num1 = numbers.pop()
         num2 = numbers.pop()
         if token == '+':
            numbers.append(num1 + num2)
         elif token == '-':
            numbers.append(num1 - num2)
         elif token == '*':
            numbers.append(num1 * num2)
         elif token == '/':
            numbers.append(num1 / num2)
      if is_function(token):
         numbers.append(calculate_function(token))
   return numbers.pop()

def replace_last(string, old, new):
   '''Replaces the last occurence of text in a string'''
   return string[::-1].replace(old, new, 1)[::-1]

def get_token_without_function(token, function):
   token = token.replace(function + '(', '', 1)
   token = replace_last(token, ')', '')
   return token

def split_function_arguments(function_arguments_string):
   '''
   Returns the splitted arguments of a function.
   Works only with two arguments.
   '''
   open_parantheses_count = 0
   for i, character in enumerate(function_arguments_string):
      if character == ',' and open_parantheses_count == 0:
         arg1 = function_arguments_string[:i]
         arg2 = function_arguments_string[i + 1:]
         return arg1, arg2
      if character == '(':
         open_parantheses_count += 1
      if character == ')':
         open_parantheses_count -= 1
   return '',''

def calculate_function(token):
   if token[:3] == 'log':
      token = get_token_without_function(token, 'log')
      return math.log(calculate_expression(token))
   if token[:3] == 'pow':
      token = get_token_without_function(token, 'pow')
      arg1, arg2 = split_function_arguments(token)
      base = calculate_expression(arg1.strip())
      power = calculate_expression(arg2.strip())
      return math.pow(base, power)
   if token[:3] == 'sin':
      token = get_token_without_function(token, 'sin')
      return math.sin(calculate_expression(token))
   if token[:3] == 'cos':
      token = get_token_without_function(token, 'cos')
      return math.cos(calculate_expression(token))
   if token[:2] == 'tg':
      token = get_token_without_function(token, 'tg')
      return math.tan(calculate_expression(token))
   if token[:4] == 'cotg':
      token = get_token_without_function(token, 'cotg')
      return 1 / math.tan(calculate_expression(token))
   if token[:4] == 'sqrt':
      token = get_token_without_function(token, 'sqrt')
      return math.pow(calculate_expression(token), 0.5)

if __name__ == '__main__':
   while True:
      expression = input("Enter expression: ")
      if expression == "exit":
         break
      modified_expression = prepare_expression(expression)
      print(calculate_expression(modified_expression))