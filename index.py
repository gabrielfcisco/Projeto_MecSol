import math
import numpy
import tkinter        as tk
import customtkinter  as ctk 
import truss_calculus as tc

#________________________________________________________________________________________________________________________________
window = ctk.CTk()                  # Cria a nossa janela de coleta de dados
window._set_appearance_mode('system') 
window.title('Projeto Mecânica dos Sólidos')
sw = window.winfo_screenwidth()
sh = window.winfo_screenheight()
ww = int(5*sw/6)
wh = int(5*sh/6)
who = int(1*(sh-wh)/3)
wwo = int((sw-ww)/2)
window.minsize(800,600)
winsize = str(ww)+'x'+str(wh)+'+'+str(wwo)+'+'+str(who) 
window.geometry(winsize)

                            # Configuração dos frames
window.columnconfigure([0,1], weight=1)
window.rowconfigure(1, weight=1)
titleframe = ctk.CTkFrame(window,bg_color='#47525d')  # Frame do Titulo
guiframe = ctk.CTkFrame(window,bg_color='#7b8994')    # Frame Principal
titleframe.grid(row=0,
                column=0,
                columnspan=2,
                sticky='nsew')
guiframe.grid(row=1,
              column=0,
              columnspan=2,
              sticky='nsew')

                            # Frame Do Título
titleframe.columnconfigure(0, weight=1)
titlelbl = ctk.CTkLabel(titleframe, text='Calculadora de Treliças',bg_color='#007ee5',text_color='white')
titlelbl.grid(row=0,column=0,sticky='nsew')

                            # Frame Principal
guiframe.columnconfigure(0, weight=1)
guiframe.rowconfigure(0, weight=1)
guiframe.grid_propagate(0)

guicanvs = ctk.CTkCanvas(guiframe, highlightthickness=0,background='#7b8994',)                             
guivscrol = ctk.CTkScrollbar(guiframe, orientation='vertical', command=guicanvs.yview, bg_color='#7b8994')  #scrollbar esquerda
guihscrol = ctk.CTkScrollbar(guiframe, orientation='horizontal', command=guicanvs.xview, bg_color='#7b8994') #scrollbar direita
guicanvs.grid(row=0,column=0,sticky='nsew')
guivscrol.grid(row=0,column=1,rowspan=2,sticky='nsew')
guihscrol.grid(row=1,column=0,sticky='nsew')

guicanvs.columnconfigure(0, weight=1)
guicanvs.rowconfigure(0, weight=1)
containerframe = ctk.CTkFrame(guicanvs,fg_color='#7b8994') # ContainerFrame 
containerframe.grid(row=0,column=0,sticky='nsew')

guicanvs.create_window((0,0), width=ww/2-17, window=containerframe, anchor='nw', tags=('736F6E61'))

containerframe.bind('<Configure>', lambda e: guicanvs.configure(scrollregion=guicanvs.bbox('all')))
guicanvs.configure(yscrollcommand=guivscrol.set, xscrollcommand=guihscrol.set)

containerframe.columnconfigure([0,1,2], weight=1)

#________________________________________________________________________________________________________________________________
                                   # funções do sistema
        
        # informações usadas para realizar os calculos:

nodes_coords = [] # lista/matriz contendo as coordenadas de cada nó [(n do nó)-1][0 =  pos X, 1 = pos Y]
links = [] # lista/matriz contendo qual o nó inical e o nó final de cada barra [(n da barra)-1][0 =  nó inicial, 1 = nó final]
supports = [] # lista/matriz contendo os apoios em cada nó [(n do nó)-1][0 = apoio em  X (boolean), 1 = apoio em Y (boolean)]
forces = [] # lista/matriz contendo as forças em cada nó [(n do nó)-1][0 = força em X (float), 1 = força em Y (float)]

def set_forces_matrix(x,y,node):
    global forces
    all_set = 0

    list_nodes = []
    for n in range(0, n_nodes):
        list_nodes.append(n)

    for j in range(0, n_forces):

        X = x[j].get()
        Y = y[j].get()
        ns = int(node[j].get())-1

        print(j, ns, X, Y)
        if (int(ns) in list_nodes):
            forces[ns] = [float(X),float(Y)]
            force_x[j].configure(state="readonly")
            force_y[j].configure(state="readonly")
            force_node[j].configure(state="readonly")

            all_set += 1
        
    if all_set == n_forces:
        print(forces)

def get_forces():
    ctk.CTkLabel (containerframe , text = "Fx(em N)",text_color='white').grid(row=8+n_nodes+n_links+n_supports,column=2,sticky='nsew')
    ctk.CTkLabel (containerframe , text = "Fy(em N)",text_color='white').grid(row=8+n_nodes+n_links+n_supports,column=3,sticky='nsew')
    ctk.CTkLabel (containerframe , text = "+Y(Cima)/+X(Direita)",text_color='white').grid(row=8+n_nodes+n_links+n_supports,column=1,sticky='nsew')
    ctk.CTkLabel (containerframe , text = "Qual Nó",text_color='white').grid(row=8+n_nodes+n_links+n_supports,column=4,sticky='nsew')

    global force_x,force_y,force_node
    force_x = []
    for fx in range(0 , n_forces):
        force_x.append(0)

    force_y = []
    for fy in range(0 , n_forces):
        force_y.append(0)
    
    force_node = []
    for fn in range(0 , n_forces):
        force_node.append(0)
    
    for i in range(0, n_forces):
        ctk.CTkLabel (containerframe , text = "Força "+ str(i+1) + ":",text_color='white').grid(row=9+n_nodes+n_links+n_supports+i,column=1,sticky='nsew')

        force_x[i] = ctk.CTkEntry(containerframe)
        force_x[i].grid(row=9+n_nodes+n_links+n_supports+i,column=2,sticky='nsew')
        force_y[i] = ctk.CTkEntry(containerframe)
        force_y[i].grid(row=9+n_nodes+n_links+n_supports+i,column=3,sticky='nsew')
        force_node[i] = ctk.CTkEntry(containerframe)
        force_node[i].grid(row=9+n_nodes+n_links+n_supports+i,column=4,sticky='nsew')
    
    btn_getforces = ctk.CTkButton(containerframe, text='Inserir Apoios', command = lambda: set_forces_matrix(force_x, force_y,force_node))
    btn_getforces.grid(row=9+n_nodes+n_links+n_supports+n_forces,column=2, columnspan=2,sticky='nsew') 

def set_supports_matrix(x,y,node):
    global supports
    all_set = 0

    list_nodes = []
    for n in range(0, n_nodes):
        list_nodes.append(n)

    for j in range(0, n_supports):

        X = x[j].get()
        Y = y[j].get()
        ns = int(node[j].get())-1

        if (str(X) == 's' or str(X) == 'n') and (str(Y) == 's' or str(Y) == 'n'):
            if (int(ns) in list_nodes):
                supports[ns] = [(0 if (str(X) == 'n') else 1),(0 if (str(Y) == 'n') else 1)]
                support_x[j].configure(state="readonly")
                support_y[j].configure(state="readonly")
                support_node[j].configure(state="readonly")

                all_set += 1
        
    if all_set == n_supports:
        get_forces()

def get_supports(): # gerar input boxes para os apoios
    ctk.CTkLabel (containerframe , text = "Apoio em X",text_color='white').grid(row=7+n_nodes+n_links,column=2,sticky='nsew')
    ctk.CTkLabel (containerframe , text = "Apoio em Y",text_color='white').grid(row=7+n_nodes+n_links,column=3,sticky='nsew')
    ctk.CTkLabel (containerframe , text = "Apoios (s/n)",text_color='white').grid(row=7+n_nodes+n_links,column=1,sticky='nsew')
    ctk.CTkLabel (containerframe , text = "Qual Nó",text_color='white').grid(row=7+n_nodes+n_links,column=4,sticky='nsew')

    global support_x,support_y,support_node
    support_x = []
    for sx in range(0 , n_supports):
        support_x.append(0)

    support_y = []
    for sy in range(0 , n_supports):
        support_y.append(0)
    
    support_node = []
    for sn in range(0 , n_supports):
        support_node.append(0)
    
    for i in range(0, n_supports):
        ctk.CTkLabel (containerframe , text = "Apoio "+ str(i+1) + ":",text_color='white').grid(row=8+n_nodes+n_links+i,column=1,sticky='nsew')

        support_x[i] = ctk.CTkEntry(containerframe)
        support_x[i].grid(row=8+n_nodes+n_links+i,column=2,sticky='nsew')
        support_y[i] = ctk.CTkEntry(containerframe)
        support_y[i].grid(row=8+n_nodes+n_links+i,column=3,sticky='nsew')
        support_node[i] = ctk.CTkEntry(containerframe)
        support_node[i].grid(row=8+n_nodes+n_links+i,column=4,sticky='nsew')
    
    btn_getsupports = ctk.CTkButton(containerframe, text='Inserir Apoios', command = lambda: set_supports_matrix(support_x, support_y,support_node))
    btn_getsupports.grid(row=8+n_nodes+n_links+n_supports,column=2, columnspan=2,sticky='nsew') 


def set_link_matrix(inicial,final): # atribuir valor para a matriz dos nós
    global links
    all_set = 0

    list_nodes = []
    for n in range(0, n_nodes):
        list_nodes.append(n+1)

    for j in range(0, n_links):

        X = inicial[j].get()
        Y = final[j].get()

        if (int(X) != int(Y)):
            if (int(X) in list_nodes) and (int(Y) in list_nodes):
                links[j] = [int(X), int(Y)]
                link_i[j].configure(state="readonly")
                link_f[j].configure(state="readonly")

                all_set += 1
        
    if all_set == n_links:
        get_supports()

def get_links(): # gerar input boxes para as barras

    ctk.CTkLabel (containerframe , text = "Nó inicial",text_color='white').grid(row=6+n_nodes,column=2,sticky='nsew')
    ctk.CTkLabel (containerframe , text = "Nó final",text_color='white').grid(row=6+n_nodes,column=3,sticky='nsew')

    global link_i,link_f
    link_i = []
    for li in range(0 , n_links):
        link_i.append(0)

    link_f = []
    for lf in range(0 , n_links):
        link_f.append(0)
    
    for i in range(0, n_links):
        ctk.CTkLabel (containerframe , text = "Barra B"+ str(i+1) + ":",text_color='white').grid(row=7+n_nodes+i,column=1,sticky='nsew')

        link_i[i] = ctk.CTkEntry(containerframe)
        link_i[i].grid(row=7+n_nodes+i,column=2,sticky='nsew')
        link_f[i] = ctk.CTkEntry(containerframe)
        link_f[i].grid(row=7+n_nodes+i,column=3,sticky='nsew')
    
    btn_getlinks = ctk.CTkButton(containerframe, text='Inserir Barras', command = lambda: set_link_matrix(link_i, link_f))
    btn_getlinks.grid(row=7+n_nodes+n_links,column=2, columnspan=2,sticky='nsew')

def set_nodes_matrix(x,y): # atribuir valor para a matriz dos nós
    global nodes_coords

    all_set = 0
    for j in range(0, n_nodes):

        X = x[j].get()
        Y = y[j].get()

        if (X != '') and (Y != ''):                             
            if (X.isnumeric()) and (Y.isnumeric()):
                    if (float(X) >= 0) and (float(Y) >= 0):            
                        nodes_coords[j] = [float(X), float(Y)]
                        node_x[j].configure(state="readonly")
                        node_y[j].configure(state="readonly")

                        all_set += 1
        
    if all_set == n_nodes:
        get_links()
    
def get_nodes(): # gerar input boxes para os nós

    ctk.CTkLabel (containerframe , text = "X",text_color='white').grid(row=5,column=2,sticky='nsew')
    ctk.CTkLabel (containerframe , text = "Y",text_color='white').grid(row=5,column=3,sticky='nsew')

    global node_x,node_y
    node_x = []
    for nx in range(0 , n_nodes):
        node_x.append(0)

    node_y = []
    for ny in range(0 , n_nodes):
        node_y.append(0)
    
    for i in range(0, n_nodes):
        ctk.CTkLabel (containerframe , text = "Nó "+ str(i+1) + ":",text_color='white').grid(row=5+i+1,column=1,sticky='nsew')

        node_x[i] = ctk.CTkEntry(containerframe)
        node_x[i].grid(row=5+i+1,column=2,sticky='nsew')
        node_y[i] = ctk.CTkEntry(containerframe)
        node_y[i].grid(row=5+i+1,column=3,sticky='nsew')
    
    btn_getnode_coords = ctk.CTkButton(containerframe, text='Inserir Nós', command = lambda: set_nodes_matrix(node_x, node_y))
    btn_getnode_coords.grid(row=5+n_nodes+1,column=2, columnspan=2,sticky='nsew') 


def set_values(ywend): # definir os valores de quantidade para cada elemento de treliça
    global n_nodes
    n_nodes = 0
    global n_links
    global n_supports
    global n_forces

    all_set = 0 #varivel para verificar se todas as quantidades de elementos da treliça ja estao definidos
    
    # verificacoes de valores
    if nodes_entry.get() != '':                             
        if nodes_entry.get().isnumeric():
            if float(nodes_entry.get()).is_integer():
                if int(nodes_entry.get()) >= 3:             # quantida minima de nós = 3
                    n_nodes = int(nodes_entry.get())
                    nodes_entry.configure(state="readonly")
                    
                    global nodes_coords             #zerar a matriz de posicoes
                    for j in range(0, n_nodes):
                        nodes_coords.append([0,0])

                    all_set += 1

    if links_entry.get() != '':
        if links_entry.get().isnumeric():
            if float(links_entry.get()).is_integer():
                if int(links_entry.get()) >= 1:             # quantida minima de barras = 1
                    n_links = int(links_entry.get())
                    links_entry.configure(state="readonly")

                    global links             #zerar a matriz de barras
                    for j in range(0, n_links):
                        links.append([0,0])

                    all_set += 1

    if supports_entry.get() != '':
        if supports_entry.get().isnumeric():
            if float(supports_entry.get()).is_integer():
                if int(supports_entry.get()) >= 1:          # quantida minima de nós com apoio = 1
                    if int(supports_entry.get()) <= int(nodes_entry.get()):
                        n_supports = int(supports_entry.get())
                        supports_entry.configure(state="readonly")

                        global supports            #zerar a matriz de apoios
                        for j in range(0, n_nodes):
                            supports.append([0,0])

                        all_set += 1

    if forces_entry.get() != '':
        if forces_entry.get().isnumeric():
            if float(forces_entry.get()).is_integer():
                if int(forces_entry.get()) >= 0:            # quantida minima de nós com forças = 0
                    if int(forces_entry.get()) <= n_nodes:
                        n_forces = int(forces_entry.get())
                        forces_entry.configure(state="readonly")

                        global forces            #zerar a matriz de forças
                        for j in range(0, n_nodes):
                            forces.append([0,0])

                        all_set += 1
    
    if all_set == 4:
        get_nodes()
                        
#________________________________________________________________________________________________________________________________
                            # Tela principal
ctk.CTkLabel (containerframe , text = "N de nós:",text_color='white').grid(row=1,column=1,sticky='nsew')
ctk.CTkLabel (containerframe , text = "N de barras:",text_color='white').grid(row=2,column=1,sticky='nsew')
ctk.CTkLabel (containerframe , text = "N de apoios:",text_color='white').grid(row=3,column=1,sticky='nsew')
ctk.CTkLabel (containerframe , text = "N de forças:",text_color='white').grid(row=4,column=1,sticky='nsew')

nodes_entry = ctk.CTkEntry(containerframe)
nodes_entry.grid(row=1,column=2,sticky='nsew')
links_entry = ctk.CTkEntry(containerframe)
links_entry.grid(row=2,column=2,sticky='nsew')
supports_entry = ctk.CTkEntry(containerframe)
supports_entry.grid(row=3,column=2,sticky='nsew')
forces_entry = ctk.CTkEntry(containerframe)
forces_entry.grid(row=4,column=2,sticky='nsew')

btn_n_values = ctk.CTkButton(containerframe, text='OK', command = lambda: set_values('ichliebe'))
btn_n_values.grid(row=1,column=3,rowspan=4,sticky='nsew')

window.mainloop()