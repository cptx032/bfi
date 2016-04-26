# Author: Willie Lawrence - cptx032 arroba gmail dot com
import sys

class BFI:
	'''
	'''
	def __init__(self, code, **kws):
		# semi-private string with the code it self
		# read only property: 'code'
		self.__code = code

		# the input buffer for ',' command
		self.input = kws.get('input', sys.stdin)

		# the output buffer for '.' command
		self.output = kws.get('output', sys.stdout)

		# the stack for data storing
		self.stack = [0] * kws.get('stack_size', 1)

		# 0-start index to code indicating where save and read
		# the data
		self.stack_cursor = 0

		# 0-start index to code indicating the next command
		self.code_cursor = 0

		# flag to indicates if a value inside stack can be
		# negative or not
		self.allow_negative = kws.get('allow_negative', False)

		# flag to indicates if '<' at start will make
		# the cursor to last char, and if '>' in the last
		# char will make the cursor to first char
		self.allow_turn_stack = kws.get('allow_turn_stack', False)

		# flag to indicates if '>' can create a new element in stack
		# if 'False' use 'stack_size' to pre set the stack size
		self.allow_stack_expanding = kws.get('allow_stack_expanding', True)

		# max element size
		self.element_size = kws.get('', 255)

		# switcher dictionary, a map of commands
		# and python functions
		self.__dictionary = {
			'+' : self.inc,
			'-' : self.dec,
			'>' : self.move_right,
			'<' : self.move_left,
			'.' : self.print_elem
		}

	@property
	def code(self):
		'''
		read-only code string
		'''
		return self.__code

	def inc(self):
		'''
		increments the current elem of stack
		'''
		self.stack[self.stack_cursor] += 1

	def dec(self):
		'''
		decreases the current elem of stack
		'''
		self.stack[self.stack_cursor] -= 1

	def move_right(self):
		'''
		move to next element of stack
		'''
		# fixme > verify stack elem creation
		# and loop
		raise NotImplementedError

	def move_left(self):
		'''
		move back in stack frame
		'''
		raise NotImplementedError

	def next(self):
		'''
		goes forward one step in the source
		'''
		raise NotImplementedError

	def back(self):
		'''
		back one step in the source
		'''
		raise NotImplementedError

	def clear_stack(self, delete=True):
		'''
		clears the stack. If 'delete' param is
		'True' the stack will change your size
		Else the stack will stay with the same size
		but all items will be zero. Use delete only
		when 'allow_stack_expanding' is 'True'
		'''
		if delete:
			self.stack = [0]
		else:
			self.stack = [0] * len(self.stack)

	def print_elem(self):
		'''
		print the current elem of stack in output buffer
		'''
		self.output.write( chr(self.stack[self.stack_cursor]) )

if __name__ == '__main__':
	bfi = BFI('+++.')