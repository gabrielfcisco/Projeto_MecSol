import numpy as np
import matplotlib.pyplot as plt

n_nos = int(input("Enter the number of nodes: "))
nodes = []
for i in range(n_nos):
    x = int(input("Enter the x coordinate of node " + str(i+1) + ": "))
    y = int(input("Enter the y coordinate of node " + str(i+1) + ": "))
    fx = int(input("Enter the x force on node " + str(i+1) + ": "))
    fy = int(input("Enter the y force on node " + str(i+1) + ": "))
    rx = int(input("Enter the x restraint on node " + str(i+1) + ": "))
    ry = int(input("Enter the y restraint on node " + str(i+1) + ": "))
    nodes.append(dict(x = x, y = y, fx = fx, fy = fy, rx = rx, ry = ry))

n_ele = int(input("Enter the number of elements: "))
elements = []
for i in range(n_ele):
    n1 = int(input("Enter the first node of element " + str(i+1) + ": "))
    n2 = int(input("Enter the second node of element " + str(i+1) + ": "))
    elements.append(dict(n1 = n1, n2 = n2))


print(nodes)
print(elements)

plt.figure(1,figsize=(12,4))
plt.ylim(-1,5)

# Plotagem dos apoios e das forças
for no in range(n_nos):
    x, y, fx, fy, rx, ry = nodes[no].values()

    if rx == 1:
        plt.scatter(x,y,400,marker =5,zorder = -2,color ='gray')
    if ry == 1:
        plt.scatter(x,y,400,marker =6,zorder = -2,color ='gray')

    if fx >0:
        plt.arrow(x-1.5,y,1,0,width =0.05,color='k')
        plt.text(x-1.5,y,'{}kN'.format(fx/1000),va='bottom')
    if fx <0:
       plt.arrow(x+1.5,y,-1,0,width =0.05,color='k')
       plt.text(x+.5,y,'{}kN'.format(fx/1000),va='bottom')
    if fy >0:
        plt.arrow(x,y-1.5,0,1,width =0.05,color='k')
        plt.text(x,y,'{}kN'.format(fy/1000),va='bottom',rotation=90)
    if fy <0:
       plt.arrow(x,y+1.5,0,-1,width =0.05,color='k')
       plt.text(x,y+.5,'{}kN'.format(fy/1000),ha='right',rotation=90)


# Plotagem das barras
for barra in range(n_ele):
    # Vamos passar os nós para as variáveis N1 e N2
    N1 = elements[barra]['n1']
    N2 = elements[barra]['n2']
    # Agora vamos acessar as coordendas de cada um dos nós
    x1 = nodes[N1-1]['x']
    y1 = nodes[N1-1]['y']
    x2 = nodes[N2-1]['x']
    y2 = nodes[N2-1]['y']
    x = [x1,x2]
    y = [y1,y2]
    
    plt.plot(x,y,'black')
    plt.scatter(x,y, s=80,marker ='o',color ='black')
    plt.show()
    #plt.grid(True)



