#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import requests
import os
from lxml import html, etree
import sys
import socket

rows, columns = os.popen('stty size', 'r').read().split()

offset = int(int(columns)/2) # half width
prog = sys.argv[0]

dict_primary = ['en','de']
dict_second = ['fr','sv','bs','cs','da','el','bg','eo','es','fi','hr','hu','is','it','la','nl','no','pl','pt','ro','ru','sk','sq','sr','tr']
dict_avail = dict_primary + dict_second

# Parse arguments
if len(sys.argv) <= 2:
    print('Please provide at least two arguments:')
    print(prog+' <dict><dict> <search>\n')
    print('Possible dictionaries <dict> are')
    print('Primary: '+" ".join(dict_primary))
    print('Secondary: '+" ".join(dict_second))
    print('Examples')
    print('>>> '+prog+' '+dict_primary[0]+dict_second[0]+'  <search> (search in two directions)')
    print('>>> '+prog+' '+dict_primary[1]+'-'+dict_second[0]+' <search> (sarch from '+dict_primary[1]+' to '+dict_second[0]+')')
    print('>>> '+prog+' '+dict_second[0]+'-'+dict_primary[0]+' <search>')
    print('>>> '+prog+' '+dict_primary[0]+dict_primary[1]+'  <search>')
    print('for a comprehensive list see http://dict.cc/')
    exit()
if len(sys.argv) > 2:
    dictionary = sys.argv[1].lower()
    dict_from = dictionary[0:2]
    if len(dictionary) == 4:
        dict_to = dictionary[2:4]
    elif len(dictionary) == 5:
        if not dictionary[2] == '-':
            print('invalid')
            exit()
        dict_to = dictionary[3:5]

    else:
        print('invalid')
        exit()
    if dict_from == dict_to:
        print('Provide two different dictionaries')
        print('You provided '+dict_from+' and '+dict_to+'.')
        exit()
    for dict_tag in [dict_from, dict_to]:
        if not dict_tag in dict_avail:
            print('Please select an available dictionary')
            print('You provided '+dict_tag)
            print('Available are')
            print(" ".join(dict_avail))
            exit()
    if not (dict_from in dict_primary or dict_to in dict_primary):
        print('Please select at least one primary dictionary from the list below')
        print(" ".join(dict_primary))
        exit()
search = " ".join(sys.argv[2:])

# set up session
s = requests.Session()
s.headers.update({'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'})
get = {'s':search}
url = "http://"+dictionary+".dict.cc/"

# get result
response = s.get(url, params=get)
tree = html.fromstring(response.content)

# get languages
content = tree.xpath('//h1[@class="searchh1"]/text()')
lang_from = content[0][1:-1] # sanitise
lang_to = content[1][1:-1]

# parse results
content = tree.xpath('//td[@class="td7nl"]')
i = 1
if (len(content)):
    print(" "+lang_from+" "*(offset + 2 - len(lang_from)) + lang_to)
    print(offset*2*"-")
for item in content:
    i += 1
    if i%2:
        res_to = " ".join(item.xpath('child::a//text()'))
        if item.xpath('child::dfn//text()'):
            res_to += " {"+", ".join(item.xpath('child::dfn//text()'))+"}"
        j = 0
        while j < len(res_from) or j < len(res_to):
            kk = offset - len(res_from[j:j+offset])
            delim = "_" if kk else " "
            # print results
            print(" "+res_from[j:j+offset] +" "+delim*kk+" "+res_to[j:j+offset])
            j += offset
            pass
    else :
        res_from = " ".join(item.xpath('child::a//text()'))
        if item.xpath('child::dfn//text()'):
            res_from += " {"+", ".join(item.xpath('child::dfn//text()'))+"}"

# parse suggestions
if not (len(content)) :
    content = tree.xpath('//td[@class="td3nl"]')
    # print results
    print('No results for '+search+' in dictionary '+dictionary)
    if len(dictionary) >= 5:
        print('Try search in both directions with \n>>> '+prog+' '+dict_from+dict_to+' '+search)
    if (len(content)):
        print('Suggestions')
        print(" "+lang_from+" "*(offset + 2 - len(lang_from)) + lang_to)
        print(offset*2*"-")
        i = 1
        a = "";
        for item in content:
            i += 1
            if i%2:
                res_to = " ".join(item.xpath('child::node()//text()'))
                j = 0
                while j < len(res_from):
                    kk = offset - len(res_from[j:j+offset])
                    delim = " "
                    print(" "+res_from[j:j+offset] +" "+delim*kk+" "+res_to[j:j+offset])
                    j += offset
                    pass
            else :
                res_from = " ".join(item.xpath('child::node()//text()'))
