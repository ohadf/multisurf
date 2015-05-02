# decodes the web response
# usage: python decode.py <file1> <file2>
import sys

f1 = open(sys.argv[1], 'r')
f2 = open(sys.argv[2], 'r')
resp1 = f1.read().decode('base64','strict')
resp2 = f2.read().decode('base64', 'strict')

f3 = open("decode"+sys.argv[1], 'w')
f4 = open("decode"+sys.argv[2], 'w')

f3.write(resp1)
f4.write(resp2)

f1.close()
f2.close()
f3.close()
f4.close()
