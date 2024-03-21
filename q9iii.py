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
import networkx as nx
import matplotlib.pyplot as plt
operators.append('$')
g =nx.DiGraph()
for i in operators:
    g.add_node('f'+str(i))
    g.add_node('g'+str(i))
for i in table:
    if i[2]=='⋗':
        g.add_edge('f'+str(i[0]),'g'+str(i[1]))
    elif i[2]=='⋖':
        g.add_edge('g'+str(i[1]),'f'+str(i[0]))

nx.draw(g, with_labels=True, node_size=1000, node_color='skyblue', font_size=10, font_color='black', edge_color='red', arrowsize=20)
plt.show()
roots = [v for v, d in g.in_degree()]
leaves = [v for v, d in g.out_degree()]
func={}
for root in roots:
    path=[]
    for leaf in leaves:
        paths = nx.all_simple_paths(g, root, leaf)
        p=list(paths)
        path.extend(p)
    if path:
        x=len(max(path,key=len))
        func[root]=x-1
    else:
        func[root]=0
func = dict(sorted(func.items(), key=lambda x: x[0]))
func_tab=[]
for i,v in func.items():
    print(i[0],"     ",i[1],"     ",v)