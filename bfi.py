# Author: Willie Lawrence - cptx032 arroba gmail dot com
import sys

class NegativeNumberError(Exception):
	pass

class CellOutOfRangeError(Exception):
	pass

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

		# max element size. None if has not limit
		self.element_size = kws.get('element_size', None)

		# switcher dictionary, a map of commands
		# and python functions
		self.__dictionary = {
			'+' : self.inc,
			'-' : self.dec,
			'>' : self.move_right,
			'<' : self.move_left,
			'.' : self.print_elem,
			',' : self.read_char,
			'[' : self.start_while_loop,
			']' : self.end_while_loop
		}

	@property
	def EOF(self):
		'''
		returns 'True' when the interpreter comes to end of file
		'''
		return (self.code_cursor > (len(self.__code) - 1)) or (self.code_cursor < 0)

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
		if (self.element_size is not None) and ( self.stack[self.stack_cursor] > self.element_size ):
			raise CellOutOfRangeError('the cell %d has exceeded the cell range: %d' % ( self.stack_cursor, self.stack[self.stack_cursor] ))

	def dec(self):
		'''
		decreases the current elem of stack
		'''
		self.stack[self.stack_cursor] -= 1
		if (not self.allow_negative) and (self.stack[self.stack_cursor] < 0):
			raise NegativeNumberError('Negative number in %dth position: %d' % ( self.stack_cursor, self.stack[self.stack_cursor] ))

	def move_right(self):
		'''
		move to next element of stack.
		the stack expanding has precedence to
		stack turning. so if both are allowed
		the stack will be expanded and not turned
		'''
		self.stack_cursor += 1
		if self.stack_cursor >= len(self.stack):
			if self.allow_stack_expanding:
				self.stack.append( 0 )
			elif self.allow_turn_stack:
				self.stack_cursor = 0
			else:
				raise CellOutOfRangeError('right move out of stack')

	def move_left(self):
		'''
		move back in stack frame
		'''
		self.stack_cursor -= 1
		if self.stack_cursor < 0:
			if self.allow_turn_stack:
				self.stack_cursor = len(self.stack)-1
			else:
				raise CellOutOfRangeError('left move out of stack')

	def unknown_command(self):
		'''
		called when a unknown char is called
		'''
		pass

	def next(self):
		'''
		goes forward one step in the source
		'''
		if self.EOF:
			return False
		command = self.__code[self.code_cursor]
		self.__dictionary.get(command, self.unknown_command)()
		self.code_cursor += 1
		return True

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

	def read_char(self):
		'''
		reads a value from input buffer and stores it in stack
		'''
		self.stack[self.stack_cursor] = ord( str(self.input.read(1)) )

	def start_while_loop(self):
		'''
		Goes to next command after while's end
		if actual cell is zero
		'''
		# when the actual cell is zero jump to end of loop
		if self.stack[self.stack_cursor] == 0:
			inner_loop_counter = 0
			# plus one because 'self.code_cursor' points to
			# while's start it self
			for i in range(self.code_cursor + 1, len(self.code)):
				if self.code[i] == '[':
					inner_loop_counter += 1
				elif self.code[i] == ']':
					if inner_loop_counter > 0:
						inner_loop_counter -= 1
					else:
						# the next command after while's end
						self.code_cursor = i
						return

	def end_while_loop(self):
		'''
		Always back to loop's start
		'''
		outer_loop_counter = 0
		for i in range(self.code_cursor):
			index = self.code_cursor - 1 - i
			command = self.code[index]
			if command == ']':
				outer_loop_counter += 1
			elif command == '[':
				if outer_loop_counter > 0:
					outer_loop_counter -= 1
				else:
					# minus one here, because the code cursor will be
					# incremented after this function execution
					self.code_cursor = index - 1
					return

if __name__ == '__main__':
	bfi = BFI('+++++++++++++++.[-].')
	while not bfi.EOF:
		bfi.next()
	print "\n", bfi.stack