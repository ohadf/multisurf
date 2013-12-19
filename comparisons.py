# comparison algorithms

import sys
import re

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
    ia = ib = 0
    slices = matching_slices(a, 0, len(a), b, 0, len(b))
    slices.append((len(a), len(b), 0))
    for sa, sb, n in slices:
        for line in a[ia:sa]:
            print "-" + line
        for line in b[ib:sb]:
            print "+" + line
        for line in a[sa:sa+n]:
            print " " + line
        ia = sa + n
        ib = sb + n

def lines(filename):
    with open(filename) as f:
        return [line.rstrip('\n') for line in f.readlines()]

def count_scripts(filename1, filename2):
    f1 = open(filename1, 'r')
    f2 = open(filename2, 'r')
    i1 = 0
    i2 = 0
    for line1 in f1:
        if '<script>' in line1:
            i1 += 1
    for line2 in f2:
        if '<script>' in line2:
            i2 += 1
    print "There are "+str(i1)+" script tags in file 1."
    print "There are "+str(i2)+" script tags in file 2."
    f1.close()
    f2.close()

def get_diff(filename1, filename2):
    print_diff(lines(filename1), lines(filename2))

def line_by_line(filename1, filename2):
    f1 = open(filename1, 'r')
    f2 = open(filename2, 'r')
    l1 = []
    l2 = []
    for line1 in f1:
        l1.append(line1)
    for line2 in f2:
        l2.append(line2)
    if l1 == l2:
        print "File 1 is equal to file 2."
    else:
        for line in range (0, min(len(l1),len(l2))):
            if l1[line] != l2[line]:
                print "Responses do not match at line %d." % line
                print "conflict: %r \n %r" % (l1[line], l2[line])
    f1.close()
    f2.close()
    
# TODO
def compare_dom_tree(filename1, filename2):
    f1 = open(filename1, 'r')
    f2 = open(filename2, 'r')
    f1.close()
    f2.close()
