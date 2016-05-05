# bfi
A brainfuck interpreter
BFI - Brain Fuck Interpreter is a simple, but powerful, Python brainfuck interpreter. With him you can go forward step by step in the source code making it a very embeddable library. See a very simple example:
```python
import bfi
interpreter = bfi.BFI("++[-].")
while not interpreter.EOF:
	interpreter.next()
```

With BFI you can redirect the input and the output to embed in your software:
```python
import bfi
from StringIO import StringIO
output_buffer = StringIO()
input_buffer = StringIO()
# filling the input
input_buffer.write('\x00\x01\x00\x01')
interpreter = bfi.BFI(",>,>,>,++[-].", output=output_buffer, input=input_buffer)
while not interpreter.EOF:
	interpreter.next()
print "output:", output_buffer.getvalue()
```
The BFI allows make cells negative:
```python
import bfi
interpreter = bfi.BFI("[-]-----", allow_negative=True)
while not interpreter.EOF:
	interpreter.next() # run ok
interpreter = bfi.BFI("[-]-----", allow_negative=False)
while not interpreter.EOF:
	interpreter.next() # raises a bfi.NegativeNumberError
```
BFI allows loop the stack:
```python
import bfi
interpreter = bfi.BFI("<", allow_turn_stack=True)
while not interpreter.EOF:
	interpreter.next() # run ok
interpreter = bfi.BFI("[-]-----", allow_turn_stack=False)
while not interpreter.EOF:
	interpreter.next() # raises a bfi.CellOutOfRangeError
```

BFI has manysome other options like stack expanding, pre filling stack etc.
