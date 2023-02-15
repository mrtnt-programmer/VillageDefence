################################################################################Les Variables##############################################################################
def variable():  #es que ca marche
    #qualite de vie
    global keyType
    keyType = "francais" # peux etre "english" ou "francais" pour les claviers different
    
    #le monde
    global seed#on utilise ce nombre pour avoir un hasard sous control(c'est a dire ,meme seed = meme resultat noise), utiliser pour noise() et random()
    seed = int(random(0,1000000))
    print("seed : ",seed)
    global zoom#le nombre de block affiche en largeur
    zoom = 75
    global monde#contient les modifications du monde (par example pour ce souvenir de l'emplacement du village/donjon)
    monde = {}#contient un dictionnaire du type (x,y):biome, avec x et y des nombre(et non des string de text!)
    global mondeSizeX, mondeSizeY#contient le nombre de carre affichee sur l'ecrant
    mondeSizeX = zoom+1# +1 pour que si on arondit vers le bas tout l'ecrant sera quand meme recouvert
    mondeSizeY = (height/(width/zoom))+1#calcule pour avoir une nombre de carre proportionelle a l'ecrant(toujour avec +1)
    global mondeVu#MondeVu contient seulement les cases vu
    global mondeVuCouleur#pour un affichage rapide on calcule avant et on stock les couleur ici
    global mondeVuDecallage #mondeVuDecallage se souvient a quelle distance on est des coordonnee d'origine
    mondeVu = [[0 for x in range(mondeSizeX+1)] for y in range(mondeSizeY+1)]
    mondeVuCouleur = [[0 for x in range(mondeSizeX+1)] for y in range(mondeSizeY+1)]
    mondeVuDecallage = {"x":1000,"y":200}#decalage du point haut gauche, on mette des valeur grand car en ce point le monde est symetrique, ce qui casse l'immersion(aucune difference de rapidite selon la grandeur de ces valeurs)
    global biomeCouleur
    biomeCouleur = {
        "eau":[41,162,240],
        "herbeClair":[89,173,54],
        "herbeFonce":[13,98,2],
        "terre":[100,66,10],
        "montagne":[160,158,156],
        "hautMontagne":[242,242,242],
        "villageTuile":[255,0,0],
        "villageMur":[200,50,50]
    }
    
    #le hero
    global heroX,heroY
    heroX = width/2
    heroY = height/2
    global heroUp,heroDown,heroLeft,heroRight
    heroUp = False
    heroDown = False
    heroLeft = False
    heroRight = False
    global heroMouvementKeys
    if keyType == "english":
        heroMouvementKeys = {"haut":"z","bas":"s","gauche":"q","droit":"d","zoomIn":"+","zoomOut":"-"}
    elif keyType == "francais":
        heroMouvementKeys = {"haut":UP,"bas":DOWN,"gauche":LEFT,"droit":RIGHT,"zoomIn":"+","zoomOut":"-"}
        
##################################################################################La boucle principale#############################################################################

def setup():
    fullScreen()
    variable()
    background(0,0,0)
    textSize(40)
    text("loading",width/2,height/2)
    noStroke()
    mondeInitialiser()

    mondeVuActualise()
        
def draw():
    print(frameRate)
    global heroX,heroY
    #mondeVuActualise() #on a seulement besoin d'actualiser si on bouge
    drawMonde()
    heroMouvement()
    fill(0)
    circle(heroX,heroY,20)
        
#####################################################################################Le Monde######################################################################################
    
def drawMonde():
    global mondeVu,mondeVuCouleur
    global biomeCouleur
    global zoom
    global mondeSizeX, mondeSizeY
    #coloriage du carre selon sont type dans le monde
    for y in range(mondeSizeY):#on affiche les pixels que le hero voit
        for x in range(mondeSizeX): 
            #dessine le carre
            fill(mondeVuCouleur[y][x][0],mondeVuCouleur[y][x][1],mondeVuCouleur[y][x][2])
            rect((width/zoom)*x,(width/zoom)*y,width/zoom,width/zoom)

def mondeVuActualise():#remet a jour le mondeVu(lors d'un mouvement seulement) , cette fonction trouve les carres a afficher et les stocke dans la list mondeVu,ainsi que precalculer les couleur
    global mondeVu,mondeVuDecallage
    global heroCameraX,heroCameraY
    global zoom
    global mondeSizeX, mondeSizeY
    global mondeVuDecallage
    global mondeVuCouleur,monde,biomeCouleur
    global seed
    noiseSeed(seed)
    noiseScale = 0.01
    noiseDetail(4,0.57)
    for y in range(mondeSizeY):
        for x in range(mondeSizeX):
            #a partire d'un seed on construit un tableau de valeur entre 1 et 0 avec la fonctrion noise()
            mondeVu[y][x] = noise((x+mondeVuDecallage["x"]) * noiseScale,(y+mondeVuDecallage["y"]) * noiseScale)
            #conversion du tableau de valeur en nom de dessin(du type 'montagne' ou 'lac')
            if mondeVu[y][x] < 0.35:
                mondeVu[y][x] = "eau"
            elif mondeVu[y][x] < 0.45:
                mondeVu[y][x] = "herbeClair"
            elif mondeVu[y][x] < 0.6:
                mondeVu[y][x] = "herbeFonce"
            elif mondeVu[y][x] < 0.7:
                mondeVu[y][x] = "terre"
            elif mondeVu[y][x] < 0.8:
                mondeVu[y][x] = "montagne"
            else :#mondeVu[y][x] < 0.9
                mondeVu[y][x] = "hautMontagne"
                
    #modification avec ce q'il a dans "monde"
    for coor in monde.keys():#pour chaque modification
        #on verifie d'abord si il est a etre afficher sur l'ecran
        if coor[0] <= mondeVuDecallage["x"]+mondeSizeX and coor[0] >= mondeVuDecallage["x"]:
            if coor[1] <= mondeVuDecallage["y"]+mondeSizeY and coor[1] >= mondeVuDecallage["y"]:
                #modification
                mondeVu[coor[1]-mondeVuDecallage["y"]][coor[0]-mondeVuDecallage["x"]] = monde[coor]

    
    #on calcule a l'avance les couleurs
    for y in range(mondeSizeY):
        for x in range(mondeSizeX): 
            #d'abord on regard pour les modification dans "monde"
            for biome in biomeCouleur.keys():
                if mondeVu[y][x] == biome:
                    mondeVuCouleur[y][x] = biomeCouleur[biome]

def mondeInitialiser():#creation des construction et on mette leur bloc dans "monde", une seul foit aux debut
    makeVillage(mondeVuDecallage["x"]-10,mondeVuDecallage["y"]-10,mondeVuDecallage["x"]+10,mondeVuDecallage["y"]+10)
                    
def makeVillage(startX,startY,endX,endY):#on lui donne les corrdonne(haut gauche)et(bas droit) du carre #pour l'instan cette fonction n'est que pour replacer des coordonne en rouge
    villageBlocs = {}#contient tout les blocs du village
    for y in range(startY,endY+1):
        for x in range(startX,endX+1):
             villageBlocs[x,y] = "villageTuile"
             if(x == startX or x == endX):
                villageBlocs[x,y] = "villageMur"
             if(y == startY or y == endY):
                villageBlocs[x,y] = "villageMur" 
    injectBloc(villageBlocs)

def injectBloc(blocs):#recoit une dictionnaire de forme x,y:"biome" et l'integre dans l'affichage du monde
    global monde
    for bloc in blocs.keys():
        blocX = bloc[0]
        blocY = bloc[1]
        monde[blocX,blocY] = blocs[bloc]
    
#####################################################################################Le Hero######################################################################################"
    
def heroMouvement():
    global heroUp,heroDown,heroLeft,heroRight
    global mondeVuDecallage
    if(heroUp == True):
        mondeVuDecallage["y"] -= 1
        mondeVuActualise()
    if(heroDown == True):
        mondeVuDecallage["y"] += 1
        mondeVuActualise()
    if(heroLeft == True):
        mondeVuDecallage["x"] -= 1
        mondeVuActualise()
    if(heroRight == True):
        mondeVuDecallage["x"] += 1
        mondeVuActualise()
        
def keyPressed():
    #detection du clavier pour le systeme de mouvement pour le personage
    global heroUp,heroDown,heroLeft,heroRight
    global heroMouvementKeys
    if(keyCode == heroMouvementKeys["haut"] or key == heroMouvementKeys["haut"] ):
        heroUp = True
    if(keyCode == heroMouvementKeys["bas"] or key == heroMouvementKeys["bas"] ):
        heroDown = True
    if(keyCode == heroMouvementKeys["gauche"] or key == heroMouvementKeys["gauche"] ):
        heroLeft = True
    if(keyCode == heroMouvementKeys["droit"] or key == heroMouvementKeys["droit"] ):
        heroRight = True
        
def keyReleased():
    global heroUp,heroDown,heroLeft,heroRight
    global heroMouvementKeys
    if(keyCode == heroMouvementKeys["haut"] or key == heroMouvementKeys["haut"] ):
        heroUp = False
    if(keyCode == heroMouvementKeys["bas"] or key == heroMouvementKeys["bas"] ):
        heroDown = False
    if(keyCode == heroMouvementKeys["gauche"] or key == heroMouvementKeys["gauche"] ):
        heroLeft = False
    if(keyCode == heroMouvementKeys["droit"] or key == heroMouvementKeys["droit"] ):
        heroRight = False
