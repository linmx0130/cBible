#/usr/bin/env python
n=int(input())
for i in range(1,n+1):
    f1=open("%d.bil"%(i),"r")
    f2=open("%d.txt"%(i),"w")
    mark=False
    for t in f1:
        if mark:
            mark=False
            f2.write(t)
        if len(t)>2:
            if (t[1]==':')or(t[2]==':') :
                f2.write(t)
                mark=True
    f1.close()
    f2.close()
