#code IN PYTHON to apply left factoring in a given grammar


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
left_factored_trfn={}
for i in TrFn.keys():
    alpha,extra=set(),set()
    l=TrFn[i]
    for j1 in l:
        for j2 in l:
            if j1!=j2:
                for ctr in range(min(len(j1),len(j2)),0,-1):
                    if j1[:ctr]==j2[:ctr]:
                        alpha.add(j1[:ctr])
                        if len(j1)>1:
                            extra.add(j1[ctr:])
                        else:
                            extra.add('#')
                        if len(j2)>1:
                            extra.add(j2[ctr:])
                        else:
                            extra.add('#')
                        break
    alphaN=set()
    for i1 in alpha:
        for i2 in l:
            if i1 not in i2:
                alphaN.add(i2)
                extra.add('#')
    if len(alpha)==0:
        left_factored_trfn[i]=l
        continue
    else:
        alpha=list(alpha)
        alpha.extend(list(alphaN))
        new_syb=i+chr(39)
        for a in range(len(alpha)):
            alpha[a]+=new_syb
        left_factored_trfn[i]=alpha
        left_factored_trfn[new_syb]=list(extra)
print("Transition Function after removal of left factoring is :- ",left_factored_trfn)