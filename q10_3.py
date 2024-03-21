#code in python to find FIRST AND FOLLOW OF NON TERMINALS

variables=list(input("Enter the non terminals space separated :- ").split())
terminals=list(input("Enter the terminals space separated :- ").split())
start=input("Enter the start symbol :- ")
TrFn={}
print("Enter the transition function as following format (LHS -> RHS ) ")
print("Enter END to end the transition function ")
while True:
    ip=input()
    if ip.lower()=='end':
        break
    ip=list(ip.split('->'))
    if ip[0] not in TrFn.keys():
        TrFn[ip[0]]=[ip[1]]
    else:
        TrFn[ip[0]].append(ip[1])
print("Transition Function is : ",TrFn)
first={}
for i in TrFn.keys():
    first[i]=set()
for i in terminals:
    first[i]=set(i)
for i in TrFn.keys():
    l=TrFn[i]
    for elem in l:
        for j in range(len(elem)):
            if elem[j] in terminals:
                first[i].add(elem[j])
                break
            else:
                first[i]=first[i].union(first[elem[j]])
                if '#' not in first[elem[j]]:
                    break
                
print("FIRST OF ALL NON-TERMINALS AND TERMINALS : ",first)
follow={}
for i in variables:
    follow[i]=set()
def first_string(st):
    res=set()
    for j in range(len(st)):
        if st[j] in terminals:
            res.add(st[j])
            print(res,st)
            return res
        else:
            res=res.union(first[st[j]])
            if '#' not in first[st[j]]:
                break
    print(st,res)
    return res
            
            
follow[start].add('$')
for i in TrFn.keys():
    l=TrFn[i]
    for elem in l:
        for j in range(len(elem)):
            if elem[j] in variables:
                if j!=(len(elem)-1):
                    x=first_string(elem[j+1:])
                    print(x)
                    follow[elem[j]].update(x)
                    if '#' in x:
                        follow[elem[j]].update(i)
                else:
                    follow[elem[j]].update(i)
for i in follow.keys():
    for j in follow.keys():
            if i in follow[j]:
                for k in follow[i]:
                    follow[j].add(k)
                follow[j].remove(i)
for i in follow.keys():
    if '#' in follow[i]:
        follow[i].remove('#')
print("FOLLOW OF ALL THE NON TERMINALS :- ",follow)               

        
            
            