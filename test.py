
l1=['b','c','d','b','c','a','a']
l2=[]

[l2.append(i)for i in l1 if not  i in l2]
print(l2)