#!/usr/bin/env python
import os
name=input("Name:")
total=int(input("Total:"))
os.mkdir(name)
for i in range(1,total+1):
    os.system("wget http://www.ccctspm.org/bibleonline/hgb/%s/%s%d.htm -O %s/%d.htm"%(name,name,i,name,i))
    os.system("iconv -f gbk -t utf-8 %s/%d.htm -o%s/%d.txt"%(name,i,name,i))

