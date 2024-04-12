#BOOLEAN AND RELOP

precedence={"==":1,"<=":1,">=":1,"==":1,"<":1,">":1,"!=":1 , "not":4, "and":2 ,"or":1}
operators=list(precedence.keys())
print(operators)

class Node:
  def __init__(self,value=None,left=None,right=None,codeid=None, code_label=None, code=None,next=None):
    self.value=value
    self.left=left
    self.right=right
    self.codeid=codeid
    self.code_label=code_label
    self.code=code
    self.next=next

class Stack:
  def __init__(self):
    self.top=None

  def push(self,new_node):
    if(not self.top):
      self.top=new_node

    else:
      new_node.next=self.top
      self.top=new_node

  def pop(self):
    if(not self.top):
      print("Stack is empty!")

    else:
      popped=self.top
      self.top=self.top.next
      return popped

class Tree:
  def inorder(self,p):
    if(not p):
      return

    self.inorder(p.left)
    if(p.value in operators):
      print(p.value, end="\t")
      print(p.code)
    else:
      print(p.value)

    self.inorder(p.right)


  def postorder(self,p):
    if(not p):
      return
    self.postorder(p.left)
    self.postorder(p.right)
    if(p.value in operators):
      print(p.value, end="\t")
      print(p.code)
      print("\n")
    else:
      print(p.value)
      print("\n")

input="( ( x < y ) and ( y >= z ) or ( x == z ) or ( not ( w ) ) )"
expr=input.split()
print(expr)


#infix to postfix
stack=[]
postfix=[]

for i in range(len(expr)):
  if(expr[i]=='('):
    stack.append('(')

  elif(expr[i] not in operators and expr[i]!=')'):
    postfix.append(expr[i])

  elif(expr[i] in operators and stack[-1]=='('):
    stack.append(expr[i])

  elif(expr[i] in operators and stack[-1] in operators):
    if(precedence[expr[i]] > precedence[stack[-1]]):
      stack.append(expr[i])

    else:
      while(len(stack) and stack[-1]!='(' and stack[-1]!=')' and precedence[expr[i]]<=precedence[stack[-1]]):
        postfix.append(stack.pop())

      stack.append(expr[i])

  elif(expr[i]==')'):
    if(len(stack)!=0):
      while(True):
        elt=stack.pop()

        if(elt=='('):
          break
        postfix.append(elt)


print(postfix)


#tree construction
tree_stack=Stack()
syntax_tree=Tree()


code_id=-1

precedence={"==":1,"<=":1,">=":1,"==":1,"<":1,">":1,"!=":1 , "not":4, "and":2 ,"or":1}

binary_operators=["==","<=",">=","<",">","!=","and","or"]
unary_operators=["not"]


for c in postfix:
  if(c in binary_operators):
    print(c)
    new_node=Node()
    new_node.value=c
    op2=tree_stack.pop()
    op1=tree_stack.pop()
    new_node.codeid=code_id+1
    new_node.code_label="T"+str(new_node.codeid)
    new_node.code=new_node.code_label+" = " + op1.code_label + " " +  c + " " + op2.code_label

    new_node.left=op1
    new_node.right=op2
    tree_stack.push(new_node)
    code_id=code_id+1

  elif(c in unary_operators):
    new_node=Node()
    new_node.value=c
    op=tree_stack.pop()
    new_node.codeid=code_id+1
    new_node.code_label="T"+str(new_node.codeid)
    new_node.code=new_node.code_label+" = " + c + " " + op.code_label
    new_node.left=op
    new_node.right=None
    tree_stack.push(new_node)
    code_id=code_id+1

  else:
    new_node=Node()
    new_node.value=c
    new_node.codeid=-1
    new_node.code_label=c
    new_node.code=""
    tree_stack.push(new_node)

root=tree_stack.pop()

print("\n\n\n")

print("POSTORDER TRAVERSAL OF THE SYNTAX TREE \n")
syntax_tree.postorder(root)
