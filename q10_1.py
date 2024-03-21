#code IN PYTHON to remove left recursion in a given grammar

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
modifed_trfn={}
for i in TrFn.keys():
    alpha,beta=[],[]
    l=TrFn[i]
    for j in l:
        if j[0]==i:
            alpha.append(j[1:])
        else:
            beta.append(j)
    if len(alpha)==0:
        modifed_trfn[i]=l
        continue
    else:
        new_syb=i+chr(39)
        for b in range(len(beta)):
            beta[b]=beta[b]+new_syb
        modifed_trfn[i]=beta
        for a in range(len(alpha)):
            alpha[a]+=new_syb
        alpha.append('#')
        modifed_trfn[new_syb]=alpha
print("Transition Function after removal of left recursion is :- ",modifed_trfn)