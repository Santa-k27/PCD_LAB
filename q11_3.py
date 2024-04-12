from collections import deque
states=['0', '1', '2', '3', '4', '5', '6', '7', '8']
var=['E','T','F']
term=['+','*','i','$']
action= {
    '0': {'i': 'S 4', '+': 'ER', '*': 'ER', '$': 'ER'},
    '1': {'i': 'ER', '+': 'S 5', '*': 'ER', '$': 'AC'},
    '2': {'i': 'ER', '+': 'R E->T', '*': 'S 6', '$': 'R E->T'},
    '3': {'i': 'ER', '+': 'R T->F', '*': 'R T->F', '$': 'R T->F'},
    '4': {'i': 'ER', '+': 'R F->i', '*': 'R F->i', '$': 'R F->i'},
    '5': {'i': 'S 4', '+': 'ER', '*': 'ER', '$': 'ER'},
    '6': {'i': 'S 4', '+': 'ER', '*': 'ER', '$': 'ER'},
    '7': {'i': 'ER', '+': 'R E->E+T', '*': 'S 6', '$': 'R E->E+T'},
    '8': {'i': 'ER', '+': 'R T->T*F', '*': 'R T->T*F', '$': 'R T->T*F'}
}

goto= {
    '0': {'E': '1', 'T': '2', 'F': '3'},
    '1': {'E': 'ER', 'T': 'ER', 'F': 'ER'},
    '2': {'E': 'ER', 'T': '6', 'F': 'ER'},
    '3': {'E': 'ER', 'T': 'ER', 'F': 'ER'},
    '4': {'E': 'ER', 'T': 'ER', 'F': 'ER'},
    '5': {'E': 'ER', 'T': '7', 'F': '3'},
    '6': {'E': 'ER', 'T': 'ER', 'F': '8'},
    '7': {'E': 'ER', 'T': 'ER', 'F': 'ER'},
    '8': {'E': 'ER', 'T': 'ER', 'F': 'ER'}
}

# Helper Functions
def top_state(st):
    ctr1 = -1
    while True:
        if st[ctr1] in states:
            return st[ctr1]
        ctr1 -= 1

def top_var(st):
    ctr1 = -1
    while True:
        if st[ctr1] in var:
            return st[ctr1]
        ctr1 -= 1

def get_action(x1, x2):
    return action[x1][x2]

def find_state(sta):
    nt_top = top_var(sta)
    state_top = top_state(sta)
    return goto[state_top][nt_top]

def remove_prod(st, expr):
    s = ''.join(st)
    i = len(s) - 1
    while i > 0:
        sub = s[i:len(s) - 1]
        c_sub = ''.join(c for c in sub if not c.isdigit())
        if c_sub == expr:
            for _ in range(len(s) - i):
                st.pop()
            return
        i -= 1
    return
temp_count = 0

def newtemp():
    global temp_count
    temp_count += 1
    return f"t{temp_count}"
      
ipstr=input("Enter the input to be parsed :- ")
stack=deque()
stack.append('0')
ipstr=ipstr+'$'
ctr2=0
place={}
for i in var:
    place[i]=0
add_3=[]
while True:
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
            if t=='F->i':
                place['F']='i'
            elif t=='T->F':
                place['T']=place['F']
            elif t=='E->T':
                place['E']=place['T']
            elif t=='E->E+T':
                t=newtemp()
                add_3.append(t+" = "+place['E']+' + '+place['T'])
                place['E']=t
            elif t=='T->T*F':
                t=newtemp()
                add_3.append(t+" = "+place['T']+' * '+place['F'])
                place['T']=t 
def generate_quadruples_triples(add_3):
    quadruples = []
    triples = []

    for expression in add_3:
        parts = expression.split('=')
        result = parts[0]
        operands = parts[1].split()

        triple = (operands[0],operands[1],operands[2])
        triples.append(triple)
        op = operands[1]
        arg1 = operands[0]
        arg2 = operands[2]
        quadruple = (op, arg1, arg2, result)
        quadruples.append(quadruple)

    return quadruples, triples
if add_3:
    print("3 address code : -------------------------")
    for i in add_3:
        print(i)           
    quadruples, triples = generate_quadruples_triples(add_3)
    print("Quadruples:")
    for q in quadruples:
        print(q)

    print("\nTriples:")
    for t in triples:
        print(t)