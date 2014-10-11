# comparison algorithms

import sys
import re
import httplib
from bs4 import BeautifulSoup
import codecs

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
    soup1 = BeautifulSoup(l1)
    s1 = soup1.find_all('script')
    soup2 = BeautifulSoup(l2)
    s2 = soup2.find_all('script')
    return [len(s1), len(s2)]

def get_diff(l1, l2):
    print_diff(l1, l2)

def line_by_line(l1, l2):
    soup1 = BeautifulSoup(l1)
    soup2 = BeautifulSoup(l2)
    prettyHTML1 = soup1.prettify()
    prettyHTML2 = soup2.prettify()
    f = open('/tmp/prettyHTML1.txt', 'w')
    f.write(prettyHTML1.encode('ascii', 'ignore'))
    f.close()
    f2 = open('/tmp/prettyHTML2.txt', 'w')
    f2.write(prettyHTML2.encode('ascii', 'ignore'))
    f2.close()
    
    f3 = open('prettyHTML1.txt', 'r')
    data1 = f3.read()
    f4 = open('prettyHTML2.txt', 'r')
    data2 = f4.read()
    for line in range (0, min(len(data1), len(data2))):
        if data1[line] != data2[line]:
            return False
    return True

def compare_links(l1,l2):
    l1_links = []
    soup1 = BeautifulSoup(l1)
    for link in soup1.find_all('a'):
        l1_links.append(link.get('href'))
    for link2 in soup1.find_all('img'):
        l1_links.append(link2.get('src'))

    l2_links = []
    soup2 = BeautifulSoup(l2)
    for link3 in soup2.find_all('a'):
        l2_links.append(link3.get('href'))
    for link4 in soup2.find_all('img'):
        l2_links.append(link4.get('src'))
    return [set(l1_links), set(l2_links)]

def compare_with_two_peers(l1,l2,l3):
    c1 = line_by_line(l1,l2)
    c2 = line_by_line(l1,l3)
    c3 = line_by_line(l2,l3)
    if (c1 and c2 and c3):
        return True
    elif (not c1) and c3:
        return False
    elif (not c2) and c3:
        return False
    elif (not c1) and (not c2) and (not c3):
        return True
    else:
        return False
    #if l1 == l2 == l3:
    #    return 0
    #else:
    #    for i in range(0, (len(parse_lines1)-1)):
    #        if (not parse_lines1[i] == parse_lines2[i]) and (parse_lines2[i] == parse_lines3[i]):
    #            return 1
    #        elif (not parse_lines1[i] == parse_lines3[i]) and (parse_lines2[i] == parse_lines3[i]):
    #            return 2
    #        elif (not parse_lines1[i] == parse_lines2[i]) and (not parse_lines1[i] == parse_lines3[i]) and (not parse_lines2[i] == parse_lines3[i]):
    #            return 3

def multiple_comparisons(l1,l2):
    [s1,s2] = count_scripts(l1,l2)
    x = line_by_line(l1,l2)
    [c1,c2] = compare_links(l1,l2)
    if ((s1 == s2) and (x) and (c1 == c2)):
        return True
    else:
        return False


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

#url3 = sys.argv[3]
#conn3 = httplib.HTTPConnection(url3)
#conn3.request("GET", "")
#r3 = conn3.getresponse()
#respMsg3 = r3.read()

#resp1 = respMsg1.split("\n")
#resp2 = respMsg2.split("\n")
# --------------------------------------- 

#count_scripts(respMsg1, respMsg2)

#print "*****************************************"

#f1 = open('client.txt','r')
#f2 = open('peer.txt', 'r')

#line_by_line(f1.read(), f2.read())

#print "*****************************************"

#get_diff(resp1, resp2)

#print "******************************************"

#compare_links(respMsg1,respMsg2)

#compare_with_two_peers(respMsg1,respMsg2,respMsg3)

#multiple_comparisons(respMsg1,respMsg2)
