import sys

f = open(sys.argv[1], 'r')

for line in f:
    x = line.encode('base64','strict')
    print x
    y = x.decode('base64','strict')
    print y
