# data analysis for our crawls

import sys
from os import listdir
import comparisons
from bs4 import BeautifulSoup

def get_num_scripts(l1, l2):
    soup1 = BeautifulSoup(l1)
    s1 = soup1.find_all('script')
    soup2 = BeautifulSoup(l2)
    s2 = soup2.find_all('script')
    return len(s1) == len(s2)

def get_content_scripts(l1, l2):
    soup1 = BeautifulSoup(l1)
    s1 = soup1.find_all('script')
    soup2 = BeautifulSoup(l2)
    s2 = soup2.find_all('script')
    return (s1) == (s2)

def get_num_urls(l1, l2):
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
    return len(set(l1_links)) == len(set(l2_links))

def get_content_urls(l1, l2):
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
    return set(l1_links) == set(l2_links)

def get_text(l1, l2):
    soup1 = BeautifulSoup(l1)
    # kill all script and style elements
    for script in soup1(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text1 = soup1.get_text()

    # break into lines and remove leading and trailing space on each
    lines1 = (line.strip() for line in text1.splitlines())
    # break multi-headlines into a line each
    chunks1 = (phrase.strip() for line in lines1 for phrase in line.split("  "))
    # drop blank lines
    text1 = '\n'.join(chunk for chunk in chunks1 if chunk)

    #print(text1.encode('utf-8'))

    soup2 = BeautifulSoup(l2)
    # kill all script and style elements
    for script in soup2(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text2 = soup2.get_text()

    # break into lines and remove leading and trailing space on each
    lines2 = (line.strip() for line in text2.splitlines())
    # break multi-headlines into a line each
    chunks2 = (phrase.strip() for line in lines2 for phrase in line.split("  "))
    # drop blank lines
    text2 = '\n'.join(chunk for chunk in chunks2 if chunk)

    #print(text2.encode('utf-8'))
    return text1 == text2

directory = sys.argv[1]
files = [ f for f in listdir(directory)]

#<url, [5_0, 5_2, 5_14]> for each node

kr_map = {}
ru_map = {}
cz_map = {}
cn_map = {}
for file_name in files:
    file_name_contents = file_name.split("_")
    if file_name_contents[0] == 'netapp6.cs.kookmin.ac.kr':
        if file_name_contents[1] == '5' and file_name_contents[2] == '0':
            if file_name_contents[4] in kr_map:
                kr_map[file_name_contents[4]][0] = file_name
            else:
                kr_map[file_name_contents[4]] = [file_name, "", ""]
        if file_name_contents[1] == '5' and file_name_contents[2] == '2':
            if not file_name_contents[4] in kr_map:
                kr_map[file_name_contents[4]] = ["", file_name, ""]
            else:
                kr_map[file_name_contents[4]][1] = file_name
        if file_name_contents[1] == '5' and file_name_contents[2] == '14':
            if not file_name_contents[4] in kr_map:
                kr_map[file_name_contents[4]] = ["", "", file_name]
            else:
                kr_map[file_name_contents[4]][2] = file_name
    elif file_name_contents[0] == 'plab1.cs.msu.ru':
        if file_name_contents[1] == '5' and file_name_contents[2] == '0':
            if file_name_contents[4] in ru_map:
                ru_map[file_name_contents[4]][0] = file_name
            else:
                ru_map[file_name_contents[4]] = [file_name, "", ""]
        if file_name_contents[1] == '5' and file_name_contents[2] == '2':
            if not file_name_contents[4] in ru_map:
                ru_map[file_name_contents[4]] = ["", file_name, ""]
            else:
                ru_map[file_name_contents[4]][1] = file_name
        if file_name_contents[1] == '5' and file_name_contents[2] == '14':
            if not file_name_contents[4] in ru_map:
                ru_map[file_name_contents[4]] = ["", "", file_name]
            else:
                ru_map[file_name_contents[4]][2] = file_name
    elif file_name_contents[0] == 'planetlab-1.scie.uestc.edu.cn':
        if file_name_contents[1] == '5' and file_name_contents[2] == '0':
            if file_name_contents[4] in cn_map:
                cn_map[file_name_contents[4]][0] = file_name
            else:
                cn_map[file_name_contents[4]] = [file_name, "", ""]
        if file_name_contents[1] == '5' and file_name_contents[2] == '2':
            if not file_name_contents[4] in cn_map:
                cn_map[file_name_contents[4]] = ["", file_name, ""]
            else:
                cn_map[file_name_contents[4]][1] = file_name
        if file_name_contents[1] == '5' and file_name_contents[2] == '14':
            if not file_name_contents[4] in cn_map:
                cn_map[file_name_contents[4]] = ["", "", file_name]
            else:
                cn_map[file_name_contents[4]][2] = file_name
    elif file_name_contents[0] == 'planetlab3.cesnet.cz':
        if file_name_contents[1] == '5' and file_name_contents[2] == '0':
            if file_name_contents[4] in cz_map:
                cz_map[file_name_contents[4]][0] = file_name
            else:
                cz_map[file_name_contents[4]] = [file_name, "", ""]
        if file_name_contents[1] == '5' and file_name_contents[2] == '2':
            if not file_name_contents[4] in cz_map:
                cz_map[file_name_contents[4]] = ["", file_name, ""]
            else:
                cz_map[file_name_contents[4]][1] = file_name
        if file_name_contents[1] == '5' and file_name_contents[2] == '14':
            if not file_name_contents[4] in cz_map:
                cz_map[file_name_contents[4]] = ["", "", file_name]
            else:
                cz_map[file_name_contents[4]][2] = file_name


temporal_body_pairs = [] # (kr, ru), (cz, cn)
spatial_body_pairs = [] # (kr, ru), (cz, cn)
temporal_body_triplets = [] # (client = ru, peers = cz, cn)
spatial_body_triplets = [] # (client = ru, peers = cz, cn)

for url in kr_map:
    temporal_body_pairs.append((kr_map[url][0], kr_map[url][2]))
    
for url in ru_map:
    temporal_body_pairs.append((ru_map[url][0], ru_map[url][2]))
    temporal_body_triplets.append((ru_map[url][0], ru_map[url][1], ru_map[url][2]))
    if url in kr_map:
        spatial_body_pairs.append((kr_map[url][1], ru_map[url][1]))
    if url in cz_map and url in cn_map:
        spatial_body_triplets.append((ru_map[url][1], cz_map[url][1], cn_map[url][1]))

for url in cz_map:
    temporal_body_pairs.append((cz_map[url][0], cz_map[url][2]))

for url in cn_map:
    temporal_body_pairs.append((cn_map[url][0], cn_map[url][2]))
    if url in cz_map:
        spatial_body_pairs.append((cz_map[url][1], cn_map[url][1]))

total_pairs = 0.0
safe_pairs1 = 0.0 # number of lines
safe_pairs2 = 0.0 # is there a diff
safe_pairs4 = 0.0 # same set of links
safe_pairs5 = 0.0 # same number of links

same_num_scripts = 0.0
same_content_scripts = 0.0
same_num_urls = 0.0
same_content_urls = 0.0
same_text = 0.0
total_diffs = 0.0

#f_diff_res = open('diff_lines_europe_asia.txt', 'w')
for pair in spatial_body_pairs:
    if (not (pair[0] == "")) and (not (pair[1] == "")):
        f1 = open(directory+"/"+pair[0], 'r')
        f2 = open(directory+"/"+pair[1], 'r')
        resp1 = f1.read().decode('base64','strict')
        resp2 = f2.read().decode('base64', 'strict')

        resp1_split = resp1.split("\n")
        resp2_split = resp2.split("\n")

        #res1 = comparisons.num_lines(resp1_split, resp2_split)
        [res2, res3] = comparisons.get_diff(resp1_split, resp2_split)
        #[res4, res5] = comparisons.compare_links(resp1,resp2)

        if res2:
            r1 = get_num_scripts(resp1, resp2)
            r2 = get_content_scripts(resp1, resp2)
            r3 = get_num_urls(resp1, resp2)
            r4 = get_content_urls(resp1, resp2)
            r5 = get_text(resp1, resp2)

            if r1 == True:
                same_num_scripts += 1.0
            if r2 == True:
                same_content_scripts += 1.0
            if r3 == True:
                same_num_urls += 1.0
            if r4 == True:
                same_content_urls += 1.0
            if r5 == True:
                same_text += 1.0
            total_diffs += 1.0

        #if res1:
        #    safe_pairs1 += 1.0
        #if res2:
        #    safe_pairs2 += 1.0
        #if res4:
        #    safe_pairs4 += 1.0
        #if res5:
        #    safe_pairs5 += 1.0
        #total_pairs += 1.0
    
total_triplets = 0.0
safe_pairs6 = 0.0 # line by line with two peers
for triplet in spatial_body_triplets:
    if (not (triplet[0] == "")) and (not (triplet[1] == "")) and (not (triplet[2] == "")):
        f1 = open(directory+"/"+triplet[0], 'r')
        f2 = open(directory+"/"+triplet[1], 'r')
        f3 = open(directory+"/"+triplet[2], 'r')

        resp1 = f1.read().decode('base64','strict')
        resp2 = f2.read().decode('base64', 'strict')
        resp3 = f3.read().decode('base64', 'strict')

        resp1_split = resp1.split("\n")
        resp2_split = resp2.split("\n")
        resp3_split = resp3.split("\n")

        res6 = comparisons.compare_with_two_peers(resp1_split, resp2_split, resp3_split)

        if res6:
            safe_pairs6 += 1.0
        total_triplets += 1.0

f_res = open('statistical_results_europe_asia_diff_analysis.txt', 'w')
f_res.write("****SPATIAL ANALYSIS****\n")
f_res.write("The files with diffs have the following characteristics:\n")
f_res.write("Total diffs: "+str(total_diffs)+"\n")
f_res.write("The fraction of pairs with a diff and the same number of scripts is: "+str(same_num_scripts/total_diffs)+"\n")
f_res.write("The fraction of pairs with a diff and the same content of scripts is: "+str(same_content_scripts/total_diffs)+"\n")
f_res.write("The fraction of pairs with a diff and the same number of urls is: "+str(same_num_urls/total_diffs)+"\n")
f_res.write("The fraction of pairs with a diff and the same content of urls is: "+str(same_content_urls/total_diffs)+"\n")
f_res.write("The fraction of pairs with a diff and the same text is: "+str(same_text/total_diffs)+"\n")
#f_res.write("There were "+str(total_pairs)+"total number of pairs.\n")
#f_res.write("The fraction of safe pairs according to the number of lines analysis is: "+str(safe_pairs1/total_pairs)+"\n")
#f_res.write("The fraction of safe pairs according to the diff analysis is: "+str(safe_pairs2/total_pairs)+"\n")
#f_res.write("The fraction of safe pairs according to the number of tags/urls analysis is: "+str(safe_pairs5/total_pairs)+"\n")
#f_res.write("The fraction of safe pairs according to the set of tags/urls analysis is: "+str(safe_pairs4/total_pairs)+"\n")
#f_res.write("The fraction of safe triplets according to the multiple peers analysis is: "+str(safe_pairs6/total_triplets)+"\n")

total_pairs = 0.0
safe_pairs1 = 0.0 # number of lines
safe_pairs2 = 0.0 # is there a diff
safe_pairs4 = 0.0 # same set of links
safe_pairs5 = 0.0 # same number of links

same_num_scripts = 0.0
same_content_scripts = 0.0
same_num_urls = 0.0
same_content_urls = 0.0
same_text = 0.0
total_diffs = 0.0

for pair in temporal_body_pairs:
    if (not (pair[0] == "")) and (not (pair[1] == "")):
        f1 = open(directory+"/"+pair[0], 'r')
        f2 = open(directory+"/"+pair[1], 'r')
        resp1 = f1.read().decode('base64','strict')
        resp2 = f2.read().decode('base64', 'strict')

        resp1_split = resp1.split("\n")
        resp2_split = resp2.split("\n")

        #res1 = comparisons.num_lines(resp1_split, resp2_split)
        [res2, res3] = comparisons.get_diff(resp1_split, resp2_split)
        #[res4, res5] = comparisons.compare_links(resp1,resp2)

        if res2:
            r1 = get_num_scripts(resp1, resp2)
            r2 = get_content_scripts(resp1, resp2)
            r3 = get_num_urls(resp1, resp2)
            r4 = get_content_urls(resp1, resp2)
            r5 = get_text(resp1, resp2)

            if r1 == True:
                same_num_scripts += 1.0
            if r2 == True:
                same_content_scripts += 1.0
            if r3 == True:
                same_num_urls += 1.0
            if r4 == True:
                same_content_urls += 1.0
            if r5 == True:
                same_text += 1.0
            total_diffs += 1.0

        #if res1:
        #    safe_pairs1 += 1.0
        #if res2:
        #    safe_pairs2 += 1.0
        #if res4:
        #    safe_pairs4 += 1.0
        #if res5:
        #    safe_pairs5 += 1.0
        #total_pairs += 1.0
    
total_triplets = 0.0
safe_pairs6 = 0.0 # line by line with two peers
for triplet in temporal_body_triplets:
    if (not (triplet[0] == "")) and (not (triplet[1] == "")) and (not (triplet[2] == "")):
        f1 = open(directory+"/"+triplet[0], 'r')
        f2 = open(directory+"/"+triplet[1], 'r')
        f3 = open(directory+"/"+triplet[2], 'r')

        resp1 = f1.read().decode('base64','strict')
        resp2 = f2.read().decode('base64', 'strict')
        resp3 = f3.read().decode('base64', 'strict')

        resp1_split = resp1.split("\n")
        resp2_split = resp2.split("\n")
        resp3_split = resp3.split("\n")

        res6 = comparisons.compare_with_two_peers(resp1_split, resp2_split, resp3_split)

        if res6:
            safe_pairs6 += 1.0
        total_triplets += 1.0

f_res.write("****TEMPORAL ANALYSIS****\n")
f_res.write("The files with diffs have the following characteristics:\n")
f_res.write("Total diffs: "+str(total_diffs)+"\n")
f_res.write("The fraction of pairs with a diff and the same number of scripts is: "+str(same_num_scripts/total_diffs)+"\n")
f_res.write("The fraction of pairs with a diff and the same content of scripts is: "+str(same_content_scripts/total_diffs)+"\n")
f_res.write("The fraction of pairs with a diff and the same number of urls is: "+str(same_num_urls/total_diffs)+"\n")
f_res.write("The fraction of pairs with a diff and the same content of urls is: "+str(same_content_urls/total_diffs)+"\n")
f_res.write("The fraction of pairs with a diff and the same text is: "+str(same_text/total_diffs)+"\n")
#f_res.write("There were "+str(total_pairs)+"total number of pairs.\n")
#f_res.write("The fraction of safe pairs according to the number of lines analysis is: "+str(safe_pairs1/total_pairs)+"\n")
#f_res.write("The fraction of safe pairs according to the diff analysis is: "+str(safe_pairs2/total_pairs)+"\n")
#f_res.write("The fraction of safe pairs according to the number of tags/urls analysis is: "+str(safe_pairs5/total_pairs)+"\n")
#f_res.write("The fraction of safe pairs according to the set of tags/urls analysis is: "+str(safe_pairs4/total_pairs)+"\n")
#f_res.write("The fraction of safe triplets according to the multiple peers analysis is: "+str(safe_pairs6/total_triplets)+"\n")
f_res.close()
