import numpy as np

class extractionSTL():
    def __init__(self, chemin):
        self.__cheminSTL = chemin
        self.__listeFacette = []
        self.__listeNormales = []

    def extractionDesListes(self):
        fileHandle = open(self.__cheminSTL,"r")
        chaine = fileHandle.read()
        lst = chaine.split("\n")
        lst.remove(lst[0])
        lst.remove(lst[-1])
        x = len(lst)
        while x > 1 :
            self.lectureBlocDeSeptLignes(lst[:7])
            x = x-7
            lst = lst[-x:]

        return self.__listeNormales, self.__listeFacette

    def lectureBlocDeSeptLignes(self, lst):
        lst.remove(lst[-1])
        lst.remove(lst[-1])
        lst.remove(lst[1])
        for elt in range(0, 4):
            lst[elt] = lst[elt].split(" ")
        self.__listeNormales.append([float(lst[0][-3]), float(lst[0][-2]), float(lst[0][-1])])
        lst.remove(lst[0])
        Vertex3 = []
        for elt2 in range(0, 3) :
            liste = [float(lst[elt2][-3]), float(lst[elt2][-2]), float(lst[elt2][-1])]
            Vertex3.append(liste)
        self.__listeFacette.append(Vertex3)
        return

class operationSurLesFacettesEtLesNormales():
    def __init__(self, listeNormales, listeFacettes):
        self.__listeN = listeNormales
        self.__listeF = listeFacettes
        self.__coodDeG = []
        self.__forcesPression = []

    def calculDesCoordonneesDesG(self):
        x = len(self.__listeF)-1
        for elt in range(0, x) :
            g = []
            X = (self.__listeF[elt][0][0] + self.__listeF[elt][1][0] + self.__listeF[elt][2][0]) / 3
            Y = (self.__listeF[elt][0][1] + self.__listeF[elt][1][1] + self.__listeF[elt][2][1]) / 3
            Z = (self.__listeF[elt][0][2] + self.__listeF[elt][1][2] + self.__listeF[elt][2][2]) / 3
            g.append(X)
            g.append(Y)
            g.append(Z)
            self.__coodDeG.append(g)
        return self.__coodDeG


    def calculDePressionFacetteImergee(self, indice):
        if self.__coodDeG[indice][2] < 0.1 :
            rot = 1025
            g = 9.8
            pression = rot*g*self.__coodDeG[indice][2]
            return pression
        else:
            return 0

    def calculDesForcesDesPressions(self):
        x = len(self.__listeF)-1
        for elt in range(0, x) :
            AB = np.array([self.__listeF[elt][1][0]-self.__listeF[elt][0][0],self.__listeF[elt][1][1]-self.__listeF[elt][0][1],self.__listeF[elt][1][2]-self.__listeF[elt][0][2]])
            AC = np.array([ self.__listeF[elt][2][0]-self.__listeF[elt][0][0],self.__listeF[elt][2][1]-self.__listeF[elt][0][1],self.__listeF[elt][2][2]-self.__listeF[elt][0][2]])
            vectSurface = np.cross(AB, AC) / 2
            normeSurface = np.vdot(vectSurface, vectSurface)**2
            forcePression = self.calculDePressionFacetteImergee(elt) * normeSurface
            self.__forcesPression.append(forcePression)
        return self.__forcesPression

    def pousseeArchimede(self, nbFacetteImm):
        PA = 0
        x = int(nbFacetteImm) - 1
        for i in range(0, x):
            PA += self.__forcesPression[i]
        return PA

    def translationDesFacette(self, indiceDeTranslation):
        x = indiceDeTranslation
        for elt in range(0, len(self.__listeF)-1) :
            for elt2 in range(0, 3):
                self.__listeF[elt][elt2][-1] = self.__listeF[elt][elt2][-1] + x
        #print("affichage liste Facettes apres transalation : ")
        #print(self.__listeF)
        return self.__listeF
    def poids(self):
        masse = 1000
        return 9.81 * masse
    def coordGrandGz(self):
        listeZG = []
        sommeZg = 0
        for i in lstCoordonneesDeG:
            listeZG.append(i[2])
        for i in range(0, len(listeZG)-1):
            sommeZg += listeZG[i]
        coordGrandGz = sommeZg / len(listeZG)
        return coordGrandGz
    def calculNbFacettesImm(self):
        listeZG = []
        n = 0
        for i in lstCoordonneesDeG:
            listeZG.append(i[2])
        for i in listeZG:
            if i != 0.0:
                n +=1
        return n
    def calculHauteurImm(self,borneInf, borneSup, epsilon):
        listeZG = self.triZG()
        lst = self.resolutionTirantDeau(borneInf, borneSup, epsilon)
        print(lst[-2])
        nbFacetteImm = int(abs(lst[-2]))
        listeFImm = listeZG[:nbFacetteImm]
        facetteLaPlusProfonde = min(listeFImm)
        hauteurEau = 0.1
        hauteurImm = hauteurEau - facetteLaPlusProfonde
        return hauteurImm

    def triZG(self):
        listeZG = []
        for i in lstCoordonneesDeG:
            listeZG.append(i[2])
        listeZG.sort()
        return listeZG


    def equationTirantDeau(self,hauteurImm):
        eq = self.pousseeArchimede(hauteurImm) - self.poids()
        return eq
    def resolutionTirantDeau(self,borneInf, borneSup, epsilon):
        debut = borneInf
        fin = borneSup
        ecart = np.sqrt((borneSup - borneInf)**2)
        n = 0
        lst1=[]
        while ecart > epsilon:
            m = (debut+fin)/2
            if self.equationTirantDeau(m)*self.equationTirantDeau(borneInf)<0:
                fin = m
                self.translationDesFacette()
            else:
                debut = m
                ecart = fin-debut
                self.translationDesFacette()
            lst1.append(m)
            n+=1
        lst = [lst1,m,n]
        return lst


#Programme Principal
chemin = r"Rectangular_HULL.stl"
STL1 = extractionSTL(chemin)
listeN, listeF = STL1.extractionDesListes()
print(listeN)
print(listeF)

objetSTL1 = operationSurLesFacettesEtLesNormales(listeN, listeF)

lstCoordonneesDeG = objetSTL1.calculDesCoordonneesDesG()
print("coordonnees de tous les g : ")
print(lstCoordonneesDeG)

forcesDePression = objetSTL1.calculDesForcesDesPressions()
print("Toutes les forces de pressions des facettes immergees : ")
print(forcesDePression)

PA = objetSTL1.pousseeArchimede(21)
print("pousse Archimede : ")
print(PA)

print("coordonnée de G en Z :")
print(objetSTL1.coordGrandGz())

print("nombre de facettes immergées :")
print(objetSTL1.calculNbFacettesImm())

print("le tirant d'eau est :")
print(objetSTL1.resolutionTirantDeau(1,12,10**(-5)))

print("hauteurImm :")
print(objetSTL1.calculHauteurImm(1,12,10**(-5)))
