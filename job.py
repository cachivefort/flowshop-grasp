#!/usr/bin/env python
# coding: utf-8

""" Classe Job """

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019'

class Job():
    def __init__(self, numero, tab_durees=[]):
        # numéro du job
        self.num = numero
        # nombre d'opérations
        self.nb_op = len(tab_durees)
        # durées des opérations
        self.duree_op = [i for i in tab_durees]
        # date de début des opérations quand le job est ordonnancé
        self.date_deb = [None for i in tab_durees]
        # durée totale du job
        self.duree_job = self.calculer_duree_job()

    def numero(self):
        return self.num

    def duree_operation(self, operation):
        return self.duree_op[operation]

    def duree(self):
        return self.duree_job

    def calcul_distance_euclidienne(self):
        distance_euclidienne = 0
        for i in range(self.nb_op - 1):
            distance_euclidienne += abs(self.duree_op[i] - self.duree_op[i + 1])**2
            distance_euclidienne = distance_euclidienne ** (1 / 2)
        return distance_euclidienne

    def calcul_distance_euclidienne(self):
        distance_euclidienne = 0
        for i in range(self.nb_op - 1):
            distance_euclidienne += abs(self.duree_op[i] - self.duree_op[i + 1])
            distance_euclidienne = distance_euclidienne ** (1 / 2)
        return distance_euclidienne

    def afficher(self):
        print("Job", self.numero(),"de durée totale", self.duree(), ":")
        for num in range(len(self.duree_op)):
            duree = self.duree_op[num]
            debut = self.date_deb[num]
            print("  opération", num, ": durée =", duree, "début =", debut)       

    def calculer_duree_job(self):
        return sum(self.duree_op)    

# "main" pour tester la classe
if __name__ == "__main__":
    a = Job(1,[1,3,5,18,23])
    a.afficher()