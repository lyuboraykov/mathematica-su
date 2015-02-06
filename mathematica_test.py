import unittest
import mathematica

class TestMathematica(unittest.TestCase):
   def test_is_number_pos(self):
      self.assertTrue(mathematica.is_number('4'))

   def test_is_number_neg(self):
      self.assertFalse(mathematica.is_number('a'))

   def test_is_operator_pos(self):
      self.assertTrue(mathematica.is_operator('+'))

   def test_is_operator_neg(self):
      self.assertFalse(mathematica.is_operator('a'))

   def test_is_function_pos(self):
      self.assertTrue(mathematica.is_function('log(1 + 3)'))

   def test_is_function_neg(self):
      self.assertFalse(mathematica.is_function('logg(1 + 3)'))   

   def test_prepare_expression(self):
      expression = '1    + 2 -3 /log    (  12   )'
      prepared_expression = '1 + 2 - 3 / log( 12 )'
      self.assertEquals(mathematica.prepare_expression(expression), prepared_expression)

   def test_prepare_expression_constants(self):
      expression = 'E     + PI'
      prepared_expression = '2.718281828459045 + 3.141592653589793'
      self.assertEquals(mathematica.prepare_expression(expression), prepared_expression)

   def test_get_tokens_from_infix_notation(self):
      prepared_expression = '1 + 2 - 3 / log( 12 )'
      tokens = mathematica.get_tokens_from_infix_notation(prepared_expression)
      self.assertEquals(tokens, ['1', '+', '2', '-', '3', '/', 'log( 12 )'])

   def test_convert_to_postfix_notation(self):
      infix_tokens = ['1', '+', '2', '*', '3']
      postfix_tokens = ['1', '2', '3', '*', '+']
      self.assertEquals(postfix_tokens, mathematica.convert_to_postfix_notation(infix_tokens))

   def test_convert_to_postfix_notation_with_parantheses(self):
      infix_tokens = ['(', '1', '+', '2', ')', '*', '3']
      postfix_tokens = ['1', '2', '+', '3', '*']
      self.assertEquals(postfix_tokens, mathematica.convert_to_postfix_notation(infix_tokens))

   def test_calculate_postfix_notation(self):
      postfix_tokens = ['1', '2', '+', '3', '*']
      self.assertEquals(9.0, mathematica.calculate_postfix_notation(postfix_tokens))

   def test_calculate_expression_simple(self):
      prepared_expression = '1 + ( 3 + 3 ) / 3 * 2'
      self.assertEquals(5.0, mathematica.calculate_expression(prepared_expression))

   def test_calculate_expression_log(self):
      prepared_expression = '1 + log( 2.718281828459045 )'
      self.assertEquals(2.0, mathematica.calculate_expression(prepared_expression))

   def test_calculate_expression_pow(self):
      prepared_expression = '1 + pow( 2, pow( 2, 2 ) )'
      self.assertEquals(17.0, mathematica.calculate_expression(prepared_expression))

   def test_calculate_function_pow(self):
      function_token = 'pow( 2, pow( 2, 2 ) )'
      self.assertEquals(16.0, mathematica.calculate_function(function_token))

   def test_calculate_function_sqrt(self):
      function_token = 'sqrt( 16 )'
      self.assertEquals(4.0, mathematica.calculate_function(function_token))

   def test_calculate_function_sin(self):
      function_token = 'sin( 3.141592653589793 / 2 )'
      self.assertEquals(1.0, mathematica.calculate_function(function_token))

   def test_get_function_arguments(self):
      function_token = 'pow( 2 , pow( 2, 2 ) )'
      self.assertEquals(' 2 , pow( 2, 2 ) ', mathematica.get_function_arguments(function_token, 'pow'))

   def test_split_function_arguments(self):
      arguments = '2 , pow( 2, 2 )'
      self.assertEquals(('2 ', ' pow( 2, 2 )'), mathematica.split_function_arguments(arguments))

if __name__ == '__main__':
   unittest.main()