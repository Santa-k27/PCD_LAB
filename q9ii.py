
variables=list(input("Enter the non terminals space separated :- ").split())
operators=list(input("Enter the terminals space separated :- ").split())
start=input("Enter the start symbol :- ")
TrFn=[]
print("Enter the transition function as following format (LHS -> RHS ) ")
print("Enter END to end the transition function ")
while True:
    ip=input()
    if ip.lower()=='end':
        break
    ip=list(ip.split('->'))
    TrFn.append(ip)

#to find leading and trailing 
leading,trailing={},{}
for i in variables:
    leading[i]=set()
    trailing[i]=set()
#LEADING 
for i in range(len(TrFn)):
    s=TrFn[i][1]
    if (len(s)>1 and s[0] in variables and s[1] in operators):
        leading[TrFn[i][0]].add(s[1])
    if (s[0] in operators):
        leading[TrFn[i][0]].add(s[0])
    if (s[0] in variables):
        for k in leading[s[0]]:
            leading[TrFn[i][0]].add(k)
#TRAILING 
for i in range(len(TrFn)):
    s=TrFn[i][1]
    if (len(s)>1 and s[-1] in variables and s[-2] in operators):
        trailing[TrFn[i][0]].add(s[-2])
    if (s[-1] in operators):
        trailing[TrFn[i][0]].add(s[-1])
    if (s[-1] in variables):
        for k in trailing[s[-1]]:
            trailing[TrFn[i][0]].add(k)
print(leading)
print(trailing)
table=[]
for i in range(len(TrFn)):
    s=TrFn[i][1]
    for j in range(len(s)):
        try:
            if (len(s)>=3 and (s[j] in operators and s[j+2] in operators) and (s[j+1] in variables)):
                table.append([s[j],s[j+2],'≐'])
        except IndexError:
            continue       
    for j in range(len(s)):
        try:
            if (len(s)>=2 and (s[j] in operators and s[j+1] in operators)):
                table.append([s[j],s[j+1],'≐'])
        except IndexError:
            continue
    for j in range(len(s)):
        try:
            if (len(s)>=2 and s[j] in operators and s[j+1] in variables):
                for k in leading[s[j+1]]:
                    table.append([s[j],k,'⋖'])
        except IndexError:
            continue
    for j in range(len(s)):
        try:
            if (len(s)>=2 and s[j] in variables and s[j+1] in operators):
                for k in trailing[s[j]]:
                    table.append([k,s[j+1],'⋗'])
        except IndexError:
            continue
for i in leading[start]:
    table.append(['$',i,'⋖'])
for i in trailing[start]:
    table.append([i,'$','⋗'])   
for i in table:
    print(i[0],"   ",i[1],"    ",i[2])
operators.append('$')
TrFn1=[]
for i in TrFn:
    i0=start
    i1=''
    for j in i[1]:
        if j in variables:
            i1+=start
        else:
            i1+=j
    TrFn1.append([i0,i1])
print(TrFn)
print(TrFn1)
            
            
def top_operator(st):
    ctr1=-1
    while True:
        if st[ctr1] in operators:
            return st[ctr1],ctr1
        ctr1-=1
def get_oper(oper1,oper2):
    # found=any(x[0] == oper1 and x[1] == oper2 for x in table)
    # if found:
    #     for i in table:
    #         if i[0]==oper1 and i[1]==oper2:
    #             return i[2]
    # else:
    #     return 'X'
    third_element = next((t[2] for t in table if t[0] == oper1 and t[1] == oper2), 'X')
    return third_element
def get_close(x):
    c=-1
    while True:
        if x[c]=='⋖':
            return len(x)+c
        c-=1
def red(x):
    for i in TrFn1:
        if i[1]==x:
            return i[0]
def delete_after_index(my_deque, index):
    for i in range(len(my_deque)-index):
        my_deque.pop()

ipstr=input("Enter the input to be parsed :- ")
from collections import deque
stack=deque()
stack.append('$')
ipstr=ipstr+'$'
ctr2=0
while True:
    o1,ind1=top_operator(stack)
    o2,ind2=ipstr[ctr2],ctr2
    if None in stack:
        print("ERROR !!! the given string doesnot belong to the grammar ")
        break
    if o1=='$' and o2=='$':
        print("Given String IS ACCEPTED !!!! ")
        break
    else:
        action=get_oper(o1,o2)
        if action=='X':
            print("ERROR !!! the given string doesnot belong to the grammar ")
            break
        else:
            if action=='⋖':
                stack.insert(len(stack)-abs(ind1)+1,'⋖')
                stack.append(ipstr[ind2])
                print(stack)
                ctr2+=1
            elif action=='≐':
                stack.append(ipstr[ind2])
                print(stack)
                ctr2+=1
            elif action=='⋗':
                x1=get_close(stack)
                del stack[x1]
                ele=list(stack)[x1:]
                t=''.join(ele)
                delete_after_index(stack,x1)
                stack.append(red(t))
                print(stack)


# ⋗ 
# ⋖ 
# ≐