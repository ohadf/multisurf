# comparison algorithms

import sys
import re
import httplib

def longest_matching_slice(a, a0, a1, b, b0, b1):
    sa, sb, n = a0, b0, 0
 
    runs = {}
    for i in range(a0, a1):
        new_runs = {}
        for j in range(b0, b1):
            if a[i] == b[j]:
                k = new_runs[j] = runs.get(j-1, 0) + 1
                if k > n:
                    sa, sb, n = i-k+1, j-k+1, k
        runs = new_runs
 
    assert a[sa:sa+n] == b[sb:sb+n]
    return sa, sb, n
 
def matching_slices(a, a0, a1, b, b0, b1):
    sa, sb, n = longest_matching_slice(a, a0, a1, b, b0, b1)
    if n == 0:
        return []
    return (matching_slices(a, a0, sa, b, b0, sb) +
            [(sa, sb, n)] +
            matching_slices(a, sa+n, a1, b, sb+n, b1))

# "-" -> unique to response1, "+" -> unique to response2 
def print_diff(a, b):
    diff_lines = []
    is_diff = False
    ia = ib = 0
    slices = matching_slices(a, 0, len(a), b, 0, len(b))
    slices.append((len(a), len(b), 0))
    for sa, sb, n in slices:
        for line in a[ia:sa]:
            diff_lines.append("-" + line)
            is_diff = True
            print "-" + line
        for line in b[ib:sb]:
            diff_lines.append("+" + line)
            is_diff = True
            print "+" + line
        for line in a[sa:sa+n]:
            diff_lines.append(" " + line)
            #print " " + line
        ia = sa + n
        ib = sb + n
    #if is_diff == True:
    #    for line in diff_lines:
    #        print line
    return [is_diff, diff_lines]

def is_diff(a,b):
    diff = print_diff(a,b)
    return diff[0]

def lines(filename):
    with open(filename) as f:
        return [line.rstrip('\n') for line in f.readlines()]

def count_scripts(l1, l2):
    i1 = 0
    i2 = 0
    pattern = '<script>'
    for line1 in l1:
        n = re.findall(pattern, line1)
        i1 += len(n)
    for line2 in l2:
        n = re.findall(pattern, line2)
        i2 += len(n)
    return [i1,i2]

def get_diff(l1, l2):
    print_diff(l1, l2)

def line_by_line(l1, l2):
    if l1 == l2:
        print "File 1 is equal to file 2."
    else:
        for line in range (0, min(len(l1),len(l2))):
            if l1[line] != l2[line]:
                print "Responses do not match at line %d." % line
                print "conflict: %r \n %r" % (l1[line], l2[line])


# --------------------------------------- for testing purposes only
#url1 = sys.argv[1]
#conn1 = httplib.HTTPConnection(url1)
#conn1.request("GET", "")
#r1 = conn1.getresponse()
#respMsg1 = r1.read()

#url2 = sys.argv[2]
#conn2 = httplib.HTTPConnection(url2)
#conn2.request("GET", "")
#r2 = conn2.getresponse()
#respMsg2 = r2.read()

#resp1 = respMsg1.split("\n")
#resp2 = respMsg2.split("\n")
# --------------------------------------- 

#count_scripts(resp1, resp2)

#print "*****************************************"

#line_by_line(resp1, resp2)

#print "*****************************************"

#get_diff(resp1, resp2)
