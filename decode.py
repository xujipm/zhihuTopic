# coding: utf-8
# author: xujipm

import json

file = open('zhihu-thread-5.txt', 'r')
data = json.loads(file.read())
print(len(data))

file = open('zhihu-thread.txt', 'r')
data = json.loads(file.read())
print(len(data))

file = open('zhihu-thread-6.txt', 'r')
data = json.loads(file.read())
print(len(data))
print(data['20041935'])