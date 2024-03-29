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
    zoom = 80#1366#le nombre de bloc affiche en largeur
    mondeMargin = 6#le nombre de bloc hors ecrant que l'on ajout pour facilite les calculs, doit etre >1 pour les mouvements et >taille des ressources
    global monde#contient les modifications du monde (par example pour ce souvenir de l'emplacement du village/donjon)
    monde = {}#contient un dictionnaire du type (x,y):biome, avec x et y des nombre(et non des string de text!)
    global mondeSizeX, mondeSizeY#contient le nombre de carre affichee sur l'ecrant
    mondeSizeX = zoom+mondeMargin*2# +1 pour que si on arondit vers le bas tout l'ecrant sera quand meme recouvert
    mondeSizeY = (height/(width/zoom))+mondeMargin*2#calcule pour avoir une nombre de carre proportionelle a l'ecrant(toujour avec +1)
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
    heroX = zoom/2#contient les coordonnes du hero(par rapport a mondeVu)
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
    
    #editeur
    global editeurVariables
    #variables pour l'editeur, dans un dictionnaire pour qu'on peux cree des variables
    editeurVariables = {"zoom":40,
                        "mondesizeX":0,#certain variable vont etre definit dans editeurInitialiser()
                        "mondesizeY":0}
    
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
    #print(frameRate)
    global ecrantActuel
    if ecrantActuel == "menu":
        drawMenu()
    elif ecrantActuel == "jeu":
        global heroX,heroY,heroSize
        drawMonde()
        heroMouvement()#mouvement et actualisation du mond et collision
        fill(0,255,255)
        blocWidth = ceil(float(width)/float(zoom))
        rect(blocWidth*heroX,blocWidth*heroY,heroSize,heroSize)
        text(frameRate,100,100)
    elif ecrantActuel == "bigmap":
        drawBigmap()
    elif ecrantActuel == "editeur":
        drawEditeur()
        

#####################################################################################Le menu######################################################################################
def drawMenu():
    background(200)
    fill(225,0,0)
    textAlign(CENTER, CENTER);
    textSize(width/8)
    text("Village Defence",width/2,height/5)  
    boutonMenu(width/4,height*3/4,width/8,height/12,"Jouer","jeu")
    boutonMenu(width*3/4,height*3/4,width/8,height/12,"cree","editeur")
    
def boutonMenu(buttonX,buttonY,buttonWidth,buttonHeight,Text,prochainEcrant):   
    global ecrantActuel
    #arriere plan
    fill(225,0,0)
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
        if prochainEcrant == "editeur":
            editeurInitialiser()
            ecrantActuel = "editeur"                    
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
        

def mondeVuActualise(mouvements):#remet a jour le mondeVu(lors d'un mouvement seulement) ,cette fonction trouve les carres a afficher et les stocke dans la list mondeVu,ainsi que precalculer les couleur
    #mouvements est de forme {"x":0,"y":0}
    global mondeVu,mondeVuDecallage
    global heroCameraX,heroCameraY
    global zoom
    global mondeSizeX, mondeSizeY,mondeMargin
    global mondeVuDecallage
    global mondeVuCouleur,monde,biomeCouleur
    global seed,noiseScale
    mondeVuDecallage["x"] += mouvements["x"]
    mondeVuDecallage["y"] += mouvements["y"]

    #on vas seulement recalculer les nouveaus pixels et les margins(pour afficher les ressources correctement)
    newMondeVu = [[0 for x in range(mondeSizeX+1)] for y in range(mondeSizeY+1)]
    #les Case vu ne sont pas a recalculer donc on les stock dans la memoire pour les decaller
    for y in range(mondeMargin,mondeSizeY-mondeMargin):
        for x in range(mondeMargin,mondeSizeX-mondeMargin):
            newMondeVu[y][x] = mondeVu[y+mouvements["y"]][x+mouvements["x"]]
            
                                                                                                                    
    for y in range(mondeMargin,mondeSizeY-mondeMargin):
        for x in range(mondeMargin,mondeSizeX-mondeMargin):
            if newMondeVu[y][x] != 0:
                mondeVu[y][x] = newMondeVu[y][x]
    
    #mantenant pour les calculs des margins
    creeMonde(0,0,mondeSizeX,mondeMargin)#top
    creeMonde(0,mondeSizeY-mondeMargin,mondeSizeX,mondeMargin)#bottom
    creeMonde(0,0,mondeMargin,mondeSizeY)#left
    creeMonde(mondeSizeX-mondeMargin,0,mondeMargin,mondeSizeY)#right

    #creeMonde(0,0,mondeSizeX,mondeSizeY)#la veille facon
    
    #on calcule les couleur pour l'affichage
    creeMondeCouleur(mondeMargin,mondeMargin,mondeSizeX-mondeMargin,mondeSizeY-mondeMargin)
    
    
def creeMonde(newMondeX,newMondeY,newMondeW,newMondeH):#calcul et dessin les bloc contenu dans ce rectangle
    global mondeVu,mondeVuDecallage
    global heroCameraX,heroCameraY
    global zoom
    global mondeSizeX, mondeSizeY#rempl
    global mondeVuDecallage
    global mondeVuCouleur,monde,biomeCouleur
    global seed,noiseScale
    
    for y in range(newMondeY,newMondeH+newMondeY):
        for x in range(newMondeX,newMondeW+newMondeX):
            mondeVu[y][x] = TrouveBiome(x+mondeVuDecallage["x"],y+mondeVuDecallage["y"])#le probleme avec cette ligne c'est quelle lag trop
                
    #modification avec les bloc en memoire dans "monde"
    for coor in monde.keys():#pour chaque modification
        #on verifie d'abord si il est a etre afficher sur l'ecran
        if coor[0] <= mondeVuDecallage["x"]+newMondeW and coor[0] >= mondeVuDecallage["x"]:
            if coor[1] <= mondeVuDecallage["y"]+newMondeH and coor[1] >= mondeVuDecallage["y"]:
                #modification
                mondeVu[coor[1]-mondeVuDecallage["y"]][coor[0]-mondeVuDecallage["x"]] = monde[coor]
    
    #creation des ressource
    
    """
    #la Distribution des ressources de forme : "biome":[("ressourceCouleur",pourcentage),...]
    ressourceDistribution = {"herbeFonce":[("arbre1",2)]}
    
    #l'affichage des ressources de forme "ressource";[(x,y,biomeAAficher),...]
    ressourceCouleur = {"arbre1":[(0,0,"feuille"),(1,0,"feuille")]}
    
    print('starting')
    for y in range(newMondeY,newMondeH+newMondeY):
        for x in range(newMondeX,newMondeW+newMondeX):
            #pour chaque type de biome
            for biome in ressourceDistribution.keys:
                #pour chaque ressources
                for ressource in ressourceDistribution[biome]:
                    #pour chaque couleur
                    for couleur in ressourceCouleur[ressource]:
                        #si possible(si les coordonnees sont compris dans le terrain modifier)
                        if x+couleur[0] > newMondeX and x+couleur[0] < newMondeW+newMondeX and y+couleur[1] > newMondeY and y+couleur[1] < newMondeH+newMondeY:
                            mondeVu[y+couleur[0]][x+couleur[0]] = couleur[3]
                            #on affiche
    
                    
    """
    for y in range(newMondeY,newMondeH+newMondeY):
        for x in range(newMondeX,newMondeW+newMondeX):
            if x + 6 <= len(mondeVu[0]) and y + 6 <= len(mondeVu) and x - 1 >= 0 and y - 1 >= 0:  #si on ne depasse pas mondeVu
                if mondeVu[y][x] == "herbeFonce":
                    randomSeed(int(noise((x+mondeVuDecallage["x"]) * noiseScale,(y+mondeVuDecallage["y"]))*100000000))#un noise c'est 12 apres la virgule et on le transform en nombre entier
                    a = random(0,100)
                    if a <= 8:#le pourcentage de case qui von contenir la resource
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
    
    #on calcule a l'avance les couleurs
    creeMondeCouleur(newMondeX,newMondeY,newMondeW,newMondeH)    

def creeMondeCouleur(newMondeX,newMondeY,newMondeW,newMondeH):
    global mondeVuCouleur,biomeCouleur
    for y in range(newMondeY,newMondeH+newMondeY):
        for x in range(newMondeX,newMondeW+newMondeX):
            #on cherche le biome correspondant et on memorise la couleur
            for biome in biomeCouleur.keys():
                if mondeVu[y][x] == biome:
                    mondeVuCouleur[y][x] = biomeCouleur[biome]
    



def mondeInitialiser():#creation des construction et on mette leur bloc dans "monde", une seul foit aux debut
    global coorVillage,villageWidth,villageHeight,coorDonjon
    global mondeSizeX,mondeSizeY
    makeVillage(coorVillage["x"]-villageWidth/2,coorVillage["y"]-villageHeight/2,coorVillage["x"]+villageWidth/2,coorVillage["y"]+villageHeight/2)
    creeMonde(0,0,mondeSizeX,mondeSizeY)
                    
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
    actualise = {"x":0,"y":0}#les mouvements a fair
    if(heroUp == True):
        actualise["y"] += -distance
    if(heroDown == True):
        actualise["y"] += distance
    if(heroLeft == True):
        actualise["x"] += -distance
    if(heroRight == True):
        actualise["x"] += distance
        
    if actualise["x"] != 0 or actualise["y"] != 0 :#de cette facon on actualise que lors d'un mouvement
        mondeVuActualise(actualise)
        
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
    creeMonde(0,0,mondeSizeX,mondeSizeY)

########################################################################################editeur######################################################################################
def editeurInitialiser():
    global editeurVariables
    global mondeSizeX,mondeSizeY
    creeMonde(0,0,mondeSizeX,mondeSizeY)
    
def drawEditeur():
    global editeurVariables
    drawMonde()
    #bar de modification de variable
    barX = width*7/8 
    barY = 0
    barW = width/8
    barH = height
    fill(200)
    rect(barX,barY,barW,barH)
    #les dimention du monde cree
    editeurVariables["x"] = editeurTextInput(barX+barW/8,barY+barH*1/18,barW*6/8,barH/18,"10","width")
    #on cree des slider pour pouvoir changer des variable en live
    editeurVariables["zoom"] = editeurSlider(barX+barW/8,barY+barH*2/18,barW*6/8,barH/18,0,100,1,editeurVariables["zoom"],"zoom")
    
def editeurTextInput(x,y,w,h,data,nom):
    push()
    #background
    fill(160)
    rect(x,y,w,h)
    #text 
    fill(0)
    textSize(14)
    text(nom+": "+data,x,y,w,h)
    if mousePressed:
        print("hum")
    pop()
    
def editeurSlider(x,y,w,h,minValue,Maxvalue,interval,initialValue,name):
    push()
    #background
    fill(160)
    rect(x,y,w,h)
    #text
    fill(0)
    textSize(14)
    text(name,x,y,w*4/10,h)
    #detection et calcule du slider
    scrollDebut = w*4/10
    scrollFin = w*9/10
    valeur = initialValue
    extemum = True#si on sort de la zone de slide a gauche ou a droit,on met la valeur a l'extremum corespondant
    if(mouseX>x+scrollDebut and mouseX<x+w and mouseY>y and mouseY<y+h and mousePressed):
        valeur = minValue+(mouseX-(x+scrollDebut))*(Maxvalue-minValue)/(w-scrollDebut)#on calcul le pourcentage de ou on est sur le slider(pas forcement sur 100, mais par Maxvalue)
        extemum = True
    if extemum and mousePressed:
        if mouseX<x:
            valeur = minValue
        if mouseX>x+w:
            valeur = Maxvalue
    text(str(valeur),x,y+100,w*4/10,h)
    #affichage du slider
    stroke(0)
    strokeWeight(2)
    line(x+scrollDebut,y+h/2,x+scrollFin,y+h/2)#ligne horizontale
    line(x+scrollDebut+valeur,y+(h/4),x+scrollDebut+valeur,y+(h*3/4))#line verticale
    pop()
    return valeur
    

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
