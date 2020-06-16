import numpy as np

class stl():

    """" Cette classe permet de créer un objet, cet objet est la structure du bateau.
Les methodes de cette classe permettent d'extraire les informations utiles (données numériques)
qui vont permettre de tracer ce bateau

Une methode permet aussi de réaliser une translation de toutes les facettes
"""

    def __init__(self):
        self.__stl = r"Rectangular_HULL.stl"
        self.__listeFacette = []
        self.__listeNormal = []

    def ObtentionDesListes(self):
        fileHandle = open(self.__stl,"r")
        chaine = fileHandle.read()
        lst = chaine.split("\n")
        lst.remove(lst[0])
        lst.remove(lst[-1])
        x = len(lst)
        while len(lst) > 1 :
            self.lectureBlocDeSeptLignes(lst[:7])
            x = x-7
            lst = lst[-x:]

    def lectureBlocDeSeptLignes(self, lst):
        lst.remove(lst[-1])
        lst.remove(lst[-1])
        lst.remove(lst[1])
        for elt in range(0, 4):
            lst[elt] = lst[elt].split(" ")
        self.__listeNormal.append([float(lst[0][-3]), float(lst[0][-2]), float(lst[0][-1])])
        lst.remove(lst[0])
        Vertex3 = []
        for elt2 in range(0, 3) :
            liste = [float(lst[elt2][-3]), float(lst[elt2][-2]), float(lst[elt2][-1])]
            Vertex3.append(liste)
        self.__listeFacette.append(Vertex3)
        return

    def affichageDesListes(self):
        self.ObtentionDesListes()
        print("L'affichage de la liste des normales est le suivant : ")
        print(self.__listeNormal)
        print("L'affichage de la liste des listes de coordonnées : ")
        print(self.__listeFacette)
        return self.__listeNormal, self.__listeFacette

    def translationDesFacette(self):
        x = -1
        for elt in range(0, len(self.__listeFacette)-1):
            for elt2 in range(0, 3):
                self.__listeFacette[elt][elt2][-1] = self.__listeFacette[elt][elt2][-1] + x
        print(self.__listeFacette)

A1 = stl()
listeN, listeF = A1.affichageDesListes()
A1.translationDesFacette()
