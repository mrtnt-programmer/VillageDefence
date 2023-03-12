################################################################################Les Variables##############################################################################
def variable():
    global ecrantActuel
    ##META (qui permette de savoir des information hors du jeu et sure le jeu)
    ecrantActuel = "menu"#peux etre "jeu","bigmap","menu","editeur"
    
    ##qualite de vie
    global keyType
    keyType = "francais" # peux etre "english" ou "francais" pour les claviers different
    
    ##le monde
    #variable pour le noise()
    global seed,noiseScale#on utilise ce nombre pour avoir un hasard sous control(c'est a dire ,meme seed = meme resultat noise), utiliser pour noise() et random()
    seed = int(random(0,1000000))
    noiseScale = 0.01
    noiseSeed(seed)
    noiseDetail(4,0.57)
    print("seed : ",seed)
    
    #variable pour les dimentions du mond
    global zoom,mondeMargin
    zoom = 100#le nombre de bloc affiche en largeur
    mondeMargin = 15#le nombre de bloc hors ecrant que l'on ajout pour facilite les calculs
    global monde#contient les modifications du monde (par example pour ce souvenir de l'emplacement du village/donjon)
    monde = {}#contient un dictionnaire du type (x,y):biome, avec x et y des nombre(et non des string de text!)
    global mondeSizeX, mondeSizeY#contient le nombre de carre affichee sur l'ecrant
    mondeSizeX = zoom+1+mondeMargin*2# +1 pour que si on arondit vers le bas tout l'ecrant sera quand meme recouvert
    mondeSizeY = (height/(width/zoom))+1+mondeMargin*2#calcule pour avoir une nombre de carre proportionelle a l'ecrant(toujour avec +1)
    global mondeVu#MondeVu contient seulement les cases vu(+des cases en plus(margin) pour pouvoir calculer les cases vue)
    global mondeVuCouleur#pour un affichage rapide on calcule avant et on stock les couleur ici
    global mondeVuDecallage #mondeVuDecallage se souvient a quelle distance on est des coordonnee d'origine
    mondeVu = [[0 for x in range(mondeSizeX+1)] for y in range(mondeSizeY+1)]
    mondeVuCouleur = [[0 for x in range(mondeSizeX+1)] for y in range(mondeSizeY+1)]
    mondeVuDecallage = {"x":1000,"y":200}#decalage du point haut gauche, on mette des valeur grand car en ce point le monde est symetrique, ce qui casse l'immersion(aucune difference de rapidite selon la grandeur de ces valeurs)
    global biomeCouleur
    biomeCouleur = {
        "eau":[35,72,98],
        "herbeClair":[74,106,94],
        "herbeFonce":[49,82,64],
        "terre":[123,106,96],
        "montagne":[160,160,160],
        "hautMontagne":[255,255,255],
        "villageTuile":[255,0,0],
        "villageMur":[200,50,50],
        "noir":[0,0,0],
        "tronc":[70,51,47],
        "feuille":[44,76,60],
        "roche":[126,131,127]
    }
    global coorVillage,villageWidth,villageHeight,coorDonjon
    coorVillage = {"x":mondeVuDecallage["x"] + mondeSizeX /2,"y":mondeVuDecallage["y"]+mondeSizeX/2}#on centre le village
    villageWidth = 31
    villageHeight = 31    
    
    #le hero
    global heroX,heroY,heroSize
    heroX = zoom/2#contient les coordonnes du hero(par rapport a l'ecrant)
    heroY = (height/(width/zoom))/2
    heroSize = width/zoom
    global heroUp,heroDown,heroLeft,heroRight
    heroUp = False
    heroDown = False
    heroLeft = False
    heroRight = False
    global heroMouvementKeys
    if keyType == "english":
        heroMouvementKeys = {"haut":"z","bas":"s","gauche":"q","droit":"d","bigmap":"m"}
    elif keyType == "francais":
        heroMouvementKeys = {"haut":UP,"bas":DOWN,"gauche":LEFT,"droit":RIGHT,"bigmap":"m"}
    
    #les outil
    #bigmap(qui permette de voir une plus grand partie de la map)
    global bigmapZoom
    global bigmapSizeX,bigmapSizeY
    bigmapZoom = (width/4)+1 #le nombre de bloc a afficher (on mette une bigmap avec des carres de 4pixel de largeur)
    bigmapSizeX = bigmapZoom
    bigmapSizeY = height/(width/bigmapZoom)
    
##################################################################################La boucle principale#############################################################################

def setup():
    frameRate(40)
    fullScreen()
    variable()
    background(0,0,0)
    textSize(40)
    text("loading",width/2,height/2)
    noStroke()

def draw():
    print(frameRate)
    global ecrantActuel
    if ecrantActuel == "menu":
        drawMenu()
    if ecrantActuel == "jeu":
        global heroX,heroY,heroSize
        drawMonde()
        heroMouvement()#mouvement et actualisation du mond et collision
        fill(0,255,255)
        rect((width/zoom)*heroX,(width/zoom)*heroY,heroSize,heroSize)
    elif ecrantActuel == "bigmap":
        drawBigmap()

#####################################################################################Le menu######################################################################################
def drawMenu():
    background(0)
    #nom du jeu 
    background(200)
    fill(225,0,0)
    textAlign(CENTER, CENTER);
    textSize(width/8)
    text("Village Defence",width/2,height/5)  
    boutonMenu(width/4,height*3/4,width/8,height/12,"Jouer","jeu")
    
def boutonMenu(buttonX,buttonY,buttonWidth,buttonHeight,Text,prochainEcrant):   
    global ecrantActuel
    #arriere plan
    rect(buttonX,buttonY,buttonWidth,buttonHeight)
    #
    fill(0)
    textAlign(CENTER,CENTER);
    textSize(width/24)
    text(Text,buttonX+buttonWidth/2,buttonY+buttonHeight/2)
    #si on appuye sur le bouton on commance le jeu
    if(mouseX>buttonX and mouseX<buttonX+buttonWidth and mouseY>buttonY and mouseY<buttonY+buttonHeight and mousePressed):
        if prochainEcrant == "jeu":
            mondeInitialiser()
            ecrantActuel = "jeu"
                    
#####################################################################################Le Monde######################################################################################


def drawMonde():
    global mondeVu,mondeVuCouleur
    global biomeCouleur
    global zoom,mondeMargin
    global mondeSizeX, mondeSizeY
    global creatures,creatureImage
    #coloriage du carre selon sont type dans le monde
    for y in range(mondeMargin,mondeSizeY-mondeMargin):#on affiche les pixels que le hero voit
        for x in range(mondeMargin,mondeSizeX-mondeMargin): 
            #dessine le carre
            fill(mondeVuCouleur[y][x][0],mondeVuCouleur[y][x][1],mondeVuCouleur[y][x][2])
            blocWidth = ceil(float(width)/float(zoom))
            rect(blocWidth*(x-mondeMargin),blocWidth*(y-mondeMargin),blocWidth,blocWidth)
        

def mondeVuActualise():#remet a jour le mondeVu(lors d'un mouvement seulement) , cette fonction trouve les carres a afficher et les stocke dans la list mondeVu,ainsi que precalculer les couleur
    global mondeVu,mondeVuDecallage
    global heroCameraX,heroCameraY
    global zoom
    global mondeSizeX, mondeSizeY
    global mondeVuDecallage
    global mondeVuCouleur,monde,biomeCouleur
    global seed,noiseScale

    for y in range(mondeSizeY):
        for x in range(mondeSizeX):
            mondeVu[y][x] = TrouveBiome(x+mondeVuDecallage["x"],y+mondeVuDecallage["y"])#le probleme avec cette ligne c'est quelle lag trop
                
    #modification avec les bloc en memoire dans "monde"
    for coor in monde.keys():#pour chaque modification
        #on verifie d'abord si il est a etre afficher sur l'ecran
        if coor[0] <= mondeVuDecallage["x"]+mondeSizeX and coor[0] >= mondeVuDecallage["x"]:
            if coor[1] <= mondeVuDecallage["y"]+mondeSizeY and coor[1] >= mondeVuDecallage["y"]:
                #modification
                mondeVu[coor[1]-mondeVuDecallage["y"]][coor[0]-mondeVuDecallage["x"]] = monde[coor]
    ##########################################################################################################################################################################
    ##########################################################################################################################################################################
    ##########################################################################################################################################################################
    ########################################################################a travailler#######################################################################
    ##########################################################################################################################################################################
    ##########################################################################################################################################################################
    #creation des ressource
    for y in range(mondeSizeY):
        for x in range(mondeSizeX):
            if x + 6 <= len(mondeVu[0]) and y + 6 <= len(mondeVu) and x - 1 >= 0 and y - 1 >= 0:  #si on ne depasse pas mondeVu
                if mondeVu[y][x] == "herbeFonce":
                    randomSeed(int(noise((x+mondeVuDecallage["x"]) * noiseScale,(y+mondeVuDecallage["y"]))*100000000))#un noise c'est 12 apres la virgule et on le transform en nombre entier
                    a = random(0,100)
                    if a <= 10:#le pourcentage de case qui von contenir la resource
                        if a <= 10/3:
                            if detectionRessources("tree",1,x,y) == True:  #il y a maitenant 3 types d'arbre
                                mondeVu[y][x] = "feuille"
                                mondeVu[y+1][x] = "feuille"
                        elif a <= (10/3)*2:
                            if detectionRessources("tree",2,x,y) == True:  #detecte avec le def
                                mondeVu[y][x] = "feuille"
                                mondeVu[y][x+1] = "feuille"
                                mondeVu[y+1][x] = "feuille"
                                mondeVu[y+1][x+1] = "feuille"
                                mondeVu[y+1][x+2] = "feuille"
                                mondeVu[y+2][x+1] = "tronc"
                                mondeVu[y+3][x+1] = "tronc"
                        else:
                            if detectionRessources("tree",3,x,y) == True:
                                #creation de la ressource
                                mondeVu[y][x+1] = "feuille"
                                mondeVu[y][x+2] = "feuille"
                                mondeVu[y+1][x] = "feuille"
                                mondeVu[y+1][x+1] = "feuille"
                                mondeVu[y+1][x+2] = "feuille"
                                mondeVu[y+1][x+3] = "feuille"
                                mondeVu[y+2][x] = "feuille"
                                mondeVu[y+2][x+1] = "feuille"
                                mondeVu[y+2][x+2] = "feuille"
                                mondeVu[y+2][x+3] = "feuille"
                                mondeVu[y+3][x+1] = "tronc"
                                mondeVu[y+3][x+2] = "tronc"
                                mondeVu[y+4][x+1] = "tronc"
                                mondeVu[y+4][x+2] = "tronc"
                if mondeVu[y][x] == "terre":
                    randomSeed(int(noise((x+mondeVuDecallage["x"]) * noiseScale,(y+mondeVuDecallage["y"]))*100000000))#un noise c'est 12 apres la virgule et on le transform en nombre entier
                    a = random(0,100)
                    if a <= 5:
                        if a <= 5/3:
                            if detectionRessources("rock",1,x,y) == True:
                                mondeVu[y][x] = "roche"
                                mondeVu[y+1][x] = "roche"
                                mondeVu[y+1][x+1] = "roche"
                        elif a <= (5/3)*2:
                            if detectionRessources("rock",2,x,y) == True:
                                mondeVu[y][+1] = "roche"
                                mondeVu[y+1][x] = "roche"
                                mondeVu[y+1][x+1] = "roche"
                                mondeVu[y+2][x] = "roche"
                                mondeVu[y+2][x+1] = "roche"
                                mondeVu[y+2][x+2] = "roche"
                        else:
                            if detectionRessources("rock",3,x,y) == True:
                                mondeVu[y][x+2] = "roche"
                                mondeVu[y+1][x+1] = "roche"
                                mondeVu[y+1][x+2] = "roche"
                                mondeVu[y+1][x+3] = "roche"
                                mondeVu[y+2][x] = "roche"
                                mondeVu[y+2][x+1] = "roche"
                                mondeVu[y+2][x+2] = "roche"
                                mondeVu[y+2][x+3] = "roche"
                                mondeVu[y+3][x] = "roche"
                                mondeVu[y+3][x+1] = "roche"
                                mondeVu[y+3][x+2] = "roche"
                                mondeVu[y+3][x+3] = "roche"
##########################################################################################################################################################################

    
    #on calcule a l'avance les couleurs
    for y in range(mondeSizeY):
        for x in range(mondeSizeX): 
            #d'abord on regard pour les modification dans "monde"
            for biome in biomeCouleur.keys():
                if mondeVu[y][x] == biome:
                    mondeVuCouleur[y][x] = biomeCouleur[biome]
                    


def mondeInitialiser():#creation des construction et on mette leur bloc dans "monde", une seul foit aux debut
    global coorVillage,villageWidth,villageHeight,coorDonjon
    makeVillage(coorVillage["x"]-villageWidth/2,coorVillage["y"]-villageHeight/2,coorVillage["x"]+villageWidth/2,coorVillage["y"]+villageHeight/2)
    mondeVuActualise()
                    
def makeVillage(startX,startY,endX,endY):#on lui donne les corrdonne(haut gauche)et(bas droit) du carre #pour l'instan cette fonction n'est que pour replacer des coordonne en rouge
    villageBlocs = {}#contient tout les blocs du village
    for y in range(startY,endY+1):
        for x in range(startX,endX+1):
             villageBlocs[x,y] = "villageTuile"
             if(x == startX or x == endX):
                villageBlocs[x,y] = "villageMur"
             if(y == startY or y == endY):
                villageBlocs[x,y] = "villageMur" 
    injectBlocs(villageBlocs)

def detectionRessources(type,num,xStart,yStart):
    global mondeVu
    materiaux = ["feuille","tronc","roche"]
    """ cette partie cree des beug avec l'affichage des ressources, a revoir
    if type == "tree":
        if num == 1:
            for y in range(3):  #fait une boucle pour entourer la ressource et verifie si un block se trouve dessus
                for x in range(3):
                    if mondeVu[y+yStart-1][x+xStart-1] in materiaux:
                        return False
        elif num == 2:
            for y in range(5):
                for x in range(5):
                    if mondeVu[y+yStart-1][x+xStart-1] in materiaux:
                        return False
        else:
            for y in range(6):
                for x in range(6):
                    if mondeVu[y+yStart-1][x+xStart-1] in materiaux:
                        return False
    elif type == "rock":
        if num == 1:
            for y in range(3):
                for x in range(4):
                    if mondeVu[y+yStart-1][x+xStart-1] in materiaux:
                        return False
        elif num == 2:
            for y in range(4):
                for x in range(5):
                    if mondeVu[y+yStart-1][x+xStart-1] in materiaux:
                        return False
        else:
            for y in range(5):
                    for x in range(6):
                        if mondeVu[y+yStart-1][x+xStart-1] in materiaux:
                            return False
    """
    return True    
#####################################################################################Le Hero######################################################################################"
    
def heroMouvement():
    global heroX,heroY,heroUp,heroDown,heroLeft,heroRight
    global mondeVuDecallage,mondeVu,mondeMargin
    heroBouge(1)
    #verification que le mouvement n'est pas en collision avec un murs
    if mondeVu[heroY+mondeMargin][heroX+mondeMargin] == "eau":
        heroBouge(-1)
        #il a une collision, donc defait le mouvement
        
def heroBouge(distance):#bouge le personnage
    global heroUp,heroDown,heroLeft,heroRight
    global mondeVuDecallage
    actualise = False
    if(heroUp == True):
        mondeVuDecallage["y"] -= distance
        actualise = True
    if(heroDown == True):
        mondeVuDecallage["y"] += distance
        actualise = True
    if(heroLeft == True):
        mondeVuDecallage["x"] -= distance
        actualise = True
    if(heroRight == True):
        mondeVuDecallage["x"] += distance
        actualise = True
        
    if actualise:#de cette facon on actualise q'une foit par frame
        mondeVuActualise()
        
########################################################################################bigmap####################################################################################""
def drawBigmap():
    global mondeVu,mondeVuCouleur
    global biomeCouleur    
    global bigmapZoom 
    global bigmapSizeX,bigmapSizeY
    #coloriage du carre selon sont type dans le monde        
    for y in range(-bigmapSizeY/2,bigmapSizeY/2):
        for x in range(-bigmapSizeX/2,bigmapSizeX/2):
            #dessine le carre
            fill(mondeVuCouleur[y][x][0],mondeVuCouleur[y][x][1],mondeVuCouleur[y][x][2])
            blocWidth = ceil(float(width)/float(bigmapZoom))#on aroundit la valeur vers le haut avec ciel() pour etre sur que l'affichage prendra tout l'ecrant(ou plus)
            rect(blocWidth*(x+bigmapSizeX/2),blocWidth*(y+bigmapSizeY/2),blocWidth,blocWidth)
    
def mondeVuActualiseBigmap():#fait une seul foit pour cree les bloc de la bigmap
    global mondeVu,mondeVuDecallage
    global mondeVuDecallage
    global mondeVuCouleur,biomeCouleur
    global bigmapZoom
    global bigmapSizeX,bigmapSizeY
    resizeMonde(bigmapSizeX,bigmapSizeY)
    for y in range(-bigmapSizeY/2,bigmapSizeY/2):
        for x in range(-bigmapSizeX/2,bigmapSizeX/2):
            mondeVu[y][x] = TrouveBiome(x+mondeVuDecallage["x"],y+mondeVuDecallage["y"])#le probleme avec cette ligne c'est quelle lag trop
        
    for y in range(-bigmapSizeY/2,bigmapSizeY/2):
        for x in range(-bigmapSizeX/2,bigmapSizeX/2):
            #d'abord on regard pour les modification dans "monde"
            for biome in biomeCouleur.keys():
                if mondeVu[y][x] == biome:
                    mondeVuCouleur[y][x] = biomeCouleur[biome]

def enleveBigmap():
    global mondeSizeX, mondeSizeY
    resizeMonde(mondeSizeX,mondeSizeY)
    mondeVuActualise()

########################################################################################clavier######################################################################################

def keyPressed():
    #detection du clavier pour le systeme de mouvement pour le personage
    global heroUp,heroDown,heroLeft,heroRight
    global heroMouvementKeys
    global ecrantActuel
    if(keyCode == heroMouvementKeys["haut"] or key == heroMouvementKeys["haut"] ):
        heroUp = True
    if(keyCode == heroMouvementKeys["bas"] or key == heroMouvementKeys["bas"] ):
        heroDown = True
    if(keyCode == heroMouvementKeys["gauche"] or key == heroMouvementKeys["gauche"] ):
        heroLeft = True
    if(keyCode == heroMouvementKeys["droit"] or key == heroMouvementKeys["droit"] ):
        heroRight = True
    if(keyCode == heroMouvementKeys["bigmap"] or key == heroMouvementKeys["bigmap"] ):
        if ecrantActuel == "bigmap":#on revient au jeu  si on affiche le bigmap
            ecrantActuel = "jeu"
            enleveBigmap();
        elif ecrantActuel == "jeu":#si on joue on met le bigmap
            ecrantActuel = "bigmap"
            mondeVuActualiseBigmap();
        
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
        
#########################################################################outil######################################################################################################

def resizeMonde(taileX,taileY):#on redimention le mond
    global mondeVu,mondeVuCouleur
    mondeVu = [[0 for x in range(taileX)] for y in range(taileY)]
    mondeVuCouleur = [[0 for x in range(taileX)] for y in range(taileY)]

def TrouveBiome(X,Y):#a partir de coordonne x,y on peux donne le biome du bloc
    global noiseScale
    #on trouve la valeur entre 1 et 0 avec la fonction noise(), cette valeur est la meme si le seed et les coordonnes sont les meme
    blocNoise = noise(X * noiseScale,Y * noiseScale)
    blocBiome = "noir"#pour debug
    #on convertie la valeur en nom de dessin(du type 'montagne' ou 'lac')
    if blocNoise < 0.35:
        blocBiome = "eau"
    elif blocNoise < 0.45:
        blocBiome = "herbeClair"
    elif blocNoise < 0.6:
        blocBiome = "herbeFonce"
    elif blocNoise < 0.7:
        blocBiome = "terre"
    elif blocNoise < 0.8:
        blocBiome = "montagne"
    else :#mondeVu[y][x] < 0.9
        blocBiome = "hautMontagne";
    return blocBiome

def TrouveRandomPourcentage(X,Y,Pourcentage):#a partir de coordonne x,y et d'un pourcentage, retourn True ou False , utile pour le placement des ressources
    global noiseScale
    #noiseDetail(4,0.57)
    #on trouve la valeur entre 1 et 0 avec la fonction noise(), cette valeur est la meme si le seed et les coordonnes sont les meme
    blocNoise = noise(X * noiseScale,Y * noiseScale)
    randomSeed(int(blocNoise*10000000))#un noise semble avoir 12 nombre apres la virgule donc il faut le transformer en nombre entier(un seed doit etre entier)
    a = random(0,100)
    if a < Pourcentage:#test du pourcentage
        return True
    return False

def injectBlocs(blocs):#recoit une dictionnaire de forme x,y:"biome" et l'integre dans l'affichage du monde
    global monde
    for bloc in blocs.keys():
        blocX = bloc[0]
        blocY = bloc[1]
        monde[blocX,blocY] = blocs[bloc]
