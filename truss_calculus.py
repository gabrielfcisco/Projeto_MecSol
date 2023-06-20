import numpy as np
import matplotlib
from matplotlib import pyplot as plt


def calculadora_trelica(nodes_coords, links, supports, forces):
    E= int(2e11)
    A = float(0.01)

    nodes = []

    for no in range(len(nodes_coords)):
        nodes.append(dict(x=nodes_coords[no][0], y=nodes_coords[no][1],
                          rx=supports[no][0], ry=supports[no][1],
                          fx=forces[no][0], fy=forces[no][1]))
    
    elements = []

    for barra in range(len(links)):
        elements.append(dict(n1=links[barra][0], n2=links[barra][1], A=A, E=E))
    
    n_nos = len(nodes_coords)
    n_ele = len(links)
    # n_nos = int(input("Enter the number of nodes: "))
    # nodes = []
    # for i in range(n_nos):
    #     x = float(input("Enter the x coordinate of node " + str(i+1) + ": "))
    #     y = float(input("Enter the y coordinate of node " + str(i+1) + ": "))
    #     rx = float(input("Enter the x restraint on node " + str(i+1) + ": "))
    #     ry = float(input("Enter the y restraint on node " + str(i+1) + ": "))
    #     fx = float(input("Enter the x force on node " + str(i+1) + ": "))
    #     fy = float(input("Enter the y force on node " + str(i+1) + ": "))
    #     nodes.append(dict(x = x, y = y, fx = fx, fy = fy, rx = rx, ry = ry))

    # n_ele = int(input("Enter the number of elements: "))
    # elements = []
    # for i in range(n_ele):
    #     n1 = int(input("Enter the first node of element " + str(i+1) + ": "))
    #     n2 = int(input("Enter the second node of element " + str(i+1) + ": "))
    #     elements.append(dict(n1 = n1, n2 = n2, A = A, E = E))


    print(nodes)
    print(elements)

    plt.figure(1,figsize=(12,4.5))

    # Plotagem dos apoios e das forças
    for no in range(n_nos):
        x, y, fx, fy, rx, ry = nodes[no].values()

        # Desenhando rotulas
        plt.scatter(x, y, s=50, color='black', marker="o")
        
        # 6 é restrição vertical e 5 na horizontal
        if rx == 1:
            plt.scatter(x,y,s=200,marker =5,color ='blue')
        if ry == 1:
            plt.scatter(x,y,s=200,marker =6,color ='blue')

        if fx >0:
            plt.arrow(x-1.5,y,1,0,width =0.05,color='r')
            plt.text(x-1.5,y,'{:.2f}kN'.format(fx/1000),va='bottom')
        if fx <0:
            plt.arrow(x+1.5,y,-1,0,width =0.05,color='r')
            plt.text(x+.5,y,'{:.2f}kN'.format(fx/1000),va='bottom')
        if fy >0:
            plt.arrow(x,y-1.5,0,1,width =0.05,color='r')
            plt.text(x,y,'{:.2f}kN'.format(fy/1000),va='bottom',rotation=90)
        if fy <0:
            plt.arrow(x,y+1.5,0,-1,width =0.05,color='r')
            plt.text(x,y+.5,'{:.2f}kN'.format(fy/1000),ha='right',rotation=90)


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
        x = np.array([x1,x2])
        y = np.array([y1,y2])
        
        plt.plot(x,y,'black')

    # plt.show()
        #plt.grid(True)

    # Determinação das propriedades das barras

    for barra in range(n_ele):
        # Nós que compõem as barras
        N1 = elements[barra]['n1']
        N2 = elements[barra]['n2']
        
        # Determinação das coordenadas
        x1 = nodes[N1-1]['x']
        y1 = nodes[N1-1]['y']
        x2 = nodes[N2-1]['x']
        y2 = nodes[N2-1]['y']
        
        # Projeções nos eixos X e Y
        LX = x2 - x1
        LY = y2 - y1

        # Tamanho real da barra
        L = np.sqrt(LX**2 + LY**2)
        
        # Seno e cosseno
        seno = LY/L
        cosseno = LX/L 
        
        # Pendurando nas listas
        elements[barra]['L'] = L
        elements[barra]['sen'] = seno
        elements[barra]['cos'] = cosseno

    print(elements)

    # Montagem da matriz de rigidez 
    
    # Pré alocando a matriz de rigidez global
    maxgl = 2*n_nos
    K = np.zeros([maxgl, maxgl])
    K2 = np.zeros([maxgl, maxgl])

    print(np.shape(K))
    print(np.size(K))

    for barra in range(n_ele):
        N1, N2, A, E, L, sen, cos = elements[barra].values()
        
        # Matriz de rigidez no sistema local 
        Kl = E * A / L * np.array([[ 1, 0,-1, 0],
                                [ 0, 0, 0, 0], 
                                [-1, 0, 1, 0],
                                [ 0, 0, 0, 0]])

        # Matriz de rotação
        Mrot = np.array([[ cos,  sen,    0,   0],
                        [-sen,  cos,    0,   0],
                        [    0,   0,  cos, sen],
                        [    0,   0, -sen, cos]])
        
        # Rotação da matriz de rigidez
        Klr = np.dot(np.dot(Mrot.T, Kl), Mrot)
        
        # Determinação dos gls
        gl1 = int(2*N1-1)
        gl2 = int(2*N1)
        gl3 = int(2*N2-1)
        gl4 = int(2*N2)
        
        # Acoplamento da matriz global 
        K[gl1-1:gl2, gl1-1:gl2] += Klr[0:2, 0:2]
        K[gl3-1:gl4, gl1-1:gl2] += Klr[2:4, 0:2]
        K[gl1-1:gl2, gl3-1:gl4] += Klr[0:2, 2:4]
        K[gl3-1:gl4, gl3-1:gl4] += Klr[2:4, 2:4]
        
        # Método alternativo de alocação
        gls = -1 + np.array([[gl1, gl2, gl3, gl4]])
        K2[gls.T, gls] += Klr

    # Printa diferença entre métodos 
    print(np.max(np.abs(K2-K)))

    # Aplicando condições de contorno na matriz
    Kr = np.copy(K)

    # Impondo condições de apoio
    for no in range(n_nos):
        # Importando dados dos nós 
        RX, RY = nodes[no]['rx'], nodes[no]['ry']
        
        # Determinar graus de liberdade
        gl1 = int(2*(no+1)-1)
        gl2 = int(2*(no+1))
        
        # Desenhando os apoios
        if RX == 1:
            Kr[:, gl1-1] = 0
            Kr[gl1-1, :] = 0
            Kr[gl1-1, gl1-1] = 1
            print('Restringindo deslocamento em X no nó {}.'.format(no))
            
        if RY == 1:
            Kr[:, gl2-1] = 0
            Kr[gl2-1, :] = 0
            Kr[gl2-1, gl2-1] = 1
            print('Restringindo deslocamento em Y no nó {}.'.format(no))

    # Verificando consistencia da matriz de rigidez
    # plt.pcolormesh(K)
    # plt.colorbar()

    # Montagem do vetor de forças
    F = np.zeros([maxgl])

    for no in range(n_nos):
        # Importando dados dos nós 
        FX = nodes[no]['fx']
        FY = nodes[no]['fy']
        
        # Determinar graus de liberdade
        gl1 = int(2*(no+1)-1)
        gl2 = int(2*(no+1))
        
        # Se existir carga aplica no vetor
        if FX != 0: 
            F[gl1-1] = FX
            
        if FY != 0: 
            F[gl2-1] = FY

    print(F)
    print(Kr)
    print(K)

    # Resolução do sistema
    # A.x = b 
    print("Determinante da matriz K=", np.linalg.det(K))
    print("Determinante da matriz Kr=", np.linalg.det(Kr))

    D = np.linalg.solve(Kr, F)
    print(D)

    # Cálculo das reações
    R = np.dot(K, D)
    print(R)

    # Desenhando a estrutura
    plt.figure(3, figsize=(12,4.5))

    for barra in range(n_ele): 
        # Nós que compõem as barras
        N1, N2 = elements[barra] ['n1'], elements[barra] ['n2']
        
        # Determinação das coordenadas
        x1, y1 = nodes[N1-1] ['x'], nodes[N1-1] ['y']
        x2, y2 = nodes[N2-1] ['x'], nodes[N2-1] ['y']
        
        # Vetores de Xs e Ys
        X = np.array([x1, x2])
        Y = np.array([y1, y2])
        
        plt.plot(X, Y, color='black')
        
    for no in range(n_nos):
        # Importando dados dos nós 
        X, Y = nodes[no] ['x'], nodes[no] ['y']
        RX, RY = nodes[no] ['rx'], nodes[no] ['ry']
        
        # Desenhando rotulas
        plt.scatter(X, Y, s=50, color='black', marker="o") # 6 é restrição vertical e 5 na horizontal
        
        # Determinar graus de liberdade
        gl1 = int(2*(no+1)-1)
        gl2 = int(2*(no+1))
        
        # Desenhando os apoios
        if RX == 1:
            ReacX = R[gl1-1]
            if ReacX > 0:
                plt.arrow(X-1.5, Y, 1, 0, color='r', width=0.05)
                plt.text(X-.5, Y, '{:.2f}kN'.format(ReacX/1000), va='bottom')
            if ReacX < 0:
                plt.arrow(X+1.5, Y, -1, 0, color='r', width=0.05)
                plt.text(X+.5, Y, '{:.2f}kN'.format(ReacX/1000), va='bottom')

            
        if RY == 1:
            ReacY = R[gl2-1]

            if ReacY > 0:
                plt.arrow(X, Y-1.5, 0, 1, color='r', width=0.05)
                plt.text(X, Y-1.5, '{:.2f}kN'.format(ReacY/1000), va='bottom', rotation=90)
            if ReacY < 0:
                plt.arrow(X, Y+1.5, 0, -1, color='r', width=0.05)
                plt.text(X, Y+.5, '{:.2f}kN'.format(ReacY/1000), ha='right', rotation=90)
                
    # Exibe figura
    # plt.show()

    # Determinação dos esforços nas barras
    for barra in range(n_ele):
        N1, N2, A, E, L, sen, cos = elements[barra].values()

        # Matriz de rigidez no sistema local 
        Kl = E*A/L*np.array([[ 1, 0,-1, 0],
                            [ 0, 0, 0, 0], 
                            [-1, 0, 1, 0],
                            [ 0, 0, 0, 0]])

        # Matriz de rotação
        Mrot = np.array([[ cos,  sen,    0,   0],
                        [-sen,  cos,    0,   0],
                        [    0,   0,  cos, sen],
                        [    0,   0, -sen, cos]])
        
        # Determinação dos gls
        gl1 = int(2*N1-1)
        gl2 = int(2*N1)
        gl3 = int(2*N2-1)
        gl4 = int(2*N2)
        
        # Capturar os deslocamentos
        Dlg = np.zeros([4])
        Dlg[0] = D[gl1-1]
        Dlg[1] = D[gl2-1]
        Dlg[2] = D[gl3-1]
        Dlg[3] = D[gl4-1]
        
        # Rotaciona Dlg
        Dl = np.dot(Mrot, Dlg)
        
        # Determina esforços no sentido da barra 
        Fl = np.dot(Kl, Dl)
        FAx = Fl[2]

        # Colocando Esf no dataframe de barras
        elements[barra]['Esf'] = FAx

    # Colocando deslocamentos nodais em Nós
    Dx = []
    Dy = []

    for no in range(n_nos):
        gl1 = int(2*(no+1)-1)
        gl2 = int(2*(no+1))
        
        nodes[no]['Dx'] = gl1-1
        nodes[no]['Dy'] = gl2-1
        

    # Plotando esforços nas barras
    plt.figure(5, figsize=(16,9), dpi=70)
    plt.title('Esforços axiais em kN')

    print(elements)

    for barra in range(n_ele):
        N1, N2 = elements[barra] ['n1'], elements[barra] ['n2']
        Esf, sen, cos = elements[barra] ['Esf'], elements[barra] ['sen'], elements[barra] ['cos']
        x1, y1 = nodes[N1-1] ['x'], nodes[N1-1] ['y']
        x2, y2 = nodes[N2-1] ['x'], nodes[N2-1] ['y']
        
        if cos != 0:
            tg = sen/cos
            ang1 = np.arctan(tg)
            print(ang1)
            ang = 180*ang1/np.pi
            print(ang)
        else:
            ang = 90
        
        x = [x1, x2]
        y = [y1, y2]
        
        if Esf == 0:
            cor = 'k'
        elif Esf > 0:
            cor = 'r'
        else:
            # Esf < 0
            cor = 'b'
        plt.plot(x, y, cor, zorder=-1)
        
        plt.text(np.mean(x), np.mean(y),
                '{:.2f}kN'.format(Esf/1000),
                rotation = ang,
                horizontalalignment='center',
                verticalalignment='center',
                size = 14,
                weight ='bold'
                )
        
        # Desenhando rotulas
        plt.scatter(x, y, s=40, color='black', marker="o", zorder=0) # 6 é restrição vertical e 5 na horizontal

    for no in range(n_nos):

        # Importando dados dos nós 
        X, Y = nodes[no] ['x'], nodes[no] ['y']
        RX, RY = nodes[no] ['rx'], nodes[no] ['ry']
        FX, FY = nodes[no] ['fx'], nodes[no] ['fy']
        
        # Desenhando rotulas
        plt.scatter(X, Y, s=50, color='black', marker="o") # 6 é restrição vertical e 5 na horizontal
        
        # Determinar graus de liberdade
        gl1 = int(2*(no+1)-1)
        gl2 = int(2*(no+1))

        #Desenhando as forças externas
        if FX >0:
            plt.arrow(X-1.5,Y,1,0,width=0.05,color='r')
            plt.text(X-1.5,Y,'{:.2f}kN'.format(FX/1000),va='bottom')
        if FX <0:
            plt.arrow(X+1.5,Y,-1,0,width =0.05,color='r')
            plt.text(X+.5,Y,'{:.2f}kN'.format(FX/1000),va='bottom')
        if FY >0:
            plt.arrow(X,Y-1.5,0,1,width =0.05,color='r')
            plt.text(X,Y,'{:.2f}kN'.format(FY/1000),va='bottom',rotation=90)
        if FY <0:
            plt.arrow(X,Y+1.5,0,-1,width =0.05,color='r')
            plt.text(X,Y+.5,'{:.2f}kN'.format(FY/1000),ha='right',rotation=90)
        
        # Desenhando os apoios
        if RX == 1:
            ReacX = R[gl1-1]
            if ReacX > 0:
                plt.arrow(X-1.5, Y, 1, 0, color='r', width=0.05)
                plt.text(X-.5, Y, '{:.2f}kN'.format(ReacX/1000), va='bottom')
            if ReacX < 0:
                plt.arrow(X+1.5, Y, -1, 0, color='r', width=0.05)
                plt.text(X+.5, Y, '{:.2f}kN'.format(ReacX/1000), va='bottom')

            
        if RY == 1:
            ReacY = R[gl2-1]

            if ReacY > 0:
                plt.arrow(X, Y-1.5, 0, 1, color='r', width=0.05)
                plt.text(X, Y-1.5, '{:.2f}kN'.format(ReacY/1000), va='bottom', rotation=90)
            if ReacY < 0:
                plt.arrow(X, Y+1.5, 0, -1, color='r', width=0.05)
                plt.text(X, Y+.5, '{:.2f}kN'.format(ReacY/1000), ha='right', rotation=90)

    plt.show()