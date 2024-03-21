
"""Works only for expression grammar which is ambigious 
"""


def reduce(array):
    for i in range(len(array),0,-1):
        p=''.join(array[i:])
        for t in TrFn:
            if p==t[1]:
                del array[i:]
                array.append(t[0])
                print(array)
    return array
def can_reduce(array):
    for i in range(len(array),0,-1):
        p=''.join(array[i:])
        for t in TrFn:
            if p==t[1]:
                return True
    return False    
stack=[]
stack.append('$')
variables=list(input("Enter the non terminals space separated :- "))
terminals=list(input("Enter the terminals space separated :- "))
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
print(TrFn)
ipstr=input("Enter the input to be parsed :- ")
ipstr+='$'
ipstack=list(ipstr.strip())[::-1]
while len(ipstack)>0:
    if ipstack[-1]=='$' and stack[-2]=='$':
        print("ACCEPTED ")
        break
    x=ipstack.pop()
    stack.append(x)
    print(stack)
    while can_reduce(stack):
        stack=reduce(stack)
    
    
