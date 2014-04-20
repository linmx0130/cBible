#!/usr/bin/env python
n=int(input("Total:"))
for i in range(1,n+1):
    f1=open("%d.txt"%(i),"r")
    f2=open("%d.bil"%(i),"w")
    for t in f1:
        if t[0]!='<' :
            f2.write(t)
    f1.close()
    f2.close()
