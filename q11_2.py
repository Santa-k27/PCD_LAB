from collections import deque
n=int(input("Enter the number of states of the SLR parser : "))
states=[str(i) for i in range(n)]
print(states)
op=list(input("Enter the terminals in this grammar : ").split())
var=list(input("Enter the Non-terminals in this grammar : ").split())
print("For the entries of parser table , enter s i for shift and r transistion for reduce ")
print("enter ER for error and AC for accept !")
action={}
for i in states:
    t={}
    for j in op:
        x=input(f"Enter the parser table entry P[{i}][{j}] according to the above rules :- ")
        t[j]=x
    action[i]=t
goto={}
for i in states:
    t={}
    for j in var:
        x=input(f"Enter the parser table entry P[{i}][{j}] according to the above rules :- ")
        if x!='ER':
            t[j]=x
        else:
            t[j]=x
    goto[i]=t

def top_state(st):
    ctr1=-1
    while True:
        if st[ctr1] in states:
            return st[ctr1]
        ctr1-=1   
def top_var(st):
    ctr1=-1
    while True:
        if st[ctr1] in var:
            return st[ctr1]
        ctr1-=1
def get_action(x1,x2):
    print(x1,',',x2)
    return action[x1][x2]
def find_state(sta):
    nt_top=top_var(sta)
    state_top=top_state(sta)
    return goto[state_top][nt_top]
def remove_prod(st,expr):
    s=''.join(st)
    i=len(s)-1
    while i>0:
        sub=s[i:len(s)-1]
        c_sub=''.join(c for c in sub if not c.isdigit())
        if c_sub==expr:
            for _ in range(len(s)-i):
                st.pop()
            return
        i-=1
    return
print(action)
ipstr=input("Enter the input to be parsed :- ")

stack=deque()
stack.append('0')
ipstr=ipstr+'$'
ctr2=0

while True:
    print(stack)
    s1=top_state(stack)
    s2=ipstr[ctr2]
    act=get_action(s1,s2)
    if act=='ER':
        print("ERROR !!! the given string doesnot belong to the grammar ")
        break
    if act=='AC':
        print("Given String IS ACCEPTED !!!! ")
        break
    else:
        if act[0]=='S':
            a,s=act.split()
            stack.append(s2)
            stack.append(s)
            ctr2+=1
        elif act[0]=='R':
            a,t=act.split()
            t_lhs,t_rhs=t.split('->')
            remove_prod(stack,t_rhs)
            stack.append(t_lhs)
            s_new=find_state(stack)
            stack.append(s_new)
            
            
            