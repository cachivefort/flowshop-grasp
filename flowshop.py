#!/usr/bin/env python
#ressource : https://sci2s.ugr.es/sites/default/files/files/Teaching/GraduatesCourses/Metaheuristicas/Bibliography/GRASP.pdf

"""Résolution du flowshop de permutation :

 - par algorithme NEH
 - par une méthode évaluation-séparation
 """

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019'

from statistics import mean
import heapq
from copy import deepcopy
from random import *

class Flowshop():
    def __init__(self, nb_jobs=0, nb_machines=0, l_job=[]):
        self.nb_jobs = nb_jobs
        self.nb_machines = nb_machines
        self.l_job = l_job

    def nombre_jobs(self):
        return self.nb_jobs

    def nombre_machines(self):
        return self.nb_machines

    def liste_jobs(self, num):
        return self.l_job[num]

    def definir_par(self, nom):
        """ crée un problème de flowshop à partir d'un fichier """
        # ouverture du fichier en mode lecture
        fdonnees = open(nom,"r")
        # lecture de la première ligne
        ligne = fdonnees.readline()
        l = ligne.split() # on récupère les valeurs dans une liste
        self.nb_jobs = int(l[0])
        self.nb_machines = int(l[1])

        for i in range(self.nb_jobs):
            ligne = fdonnees.readline()
            l = ligne.split()
            # on transforme les chaînes de caractères en entiers
            l = [int(i) for i in l]
            j = Job(i, l)
            self.l_job += [j]
        # fermeture du fichier
        fdonnees.close()


    # Ordonnancement selon l'ordre NEH
    def creer_liste_NEH(self):
        """renvoie une liste selon l'ordre NEH"""
        l1=self.l_job.copy()
        l2=[]
        #on trie la liste des jobs par durée croissante
        l1.sort(key = lambda job: job.duree_job, reverse=True)
        for job in l1:
            a=[0,0]
            #On teste les différentes durées des ordonnancements ou l'on place le job à la place 0, 1, ..., j.
            for i in range (len(l2)):
                l2.insert(i,job)
                ordo=Ordonnancement(self.nb_machines)
                ordo.ordonnancer_liste_job(l2)
                if a[0]<ordo.dur:
                    a[0]=ordo.dur
                    a[1]=i
                l2.remove(job)
            l2.insert(a[1],job)
        print('Ordre des jobs avec la liste NEH :')
        for job in l2:
            print(job.num)
        print('Durée des jobs avec cette méthode :', ordo.dur, '\n')


    # exo 5 A REMPLIR

    # calcul de r_kj tenant compte d'un ordo en cours
    def calculer_date_dispo(self, ordo, machine, job):
            a=ordo.date_disponibilite(0)
            for i in range (machine):
                a=max(a,ordo.date_disponibilite(i))+job.duree_operation(i)
            return(a)

    # calcul de q_kj tenant compte d'un ordo en cours
    def calculer_duree_latence(self, ordo, machine, job):
        if machine == self.nb_machines-1:
            return(0)
        a=ordo.date_disponibilite(machine+1)
        for i in range(machine+1,self.nb_machines):
            a=max(a,ordo.date_disponibilite(i))+job.duree_operation(i)
        return(a)

    # calcul de la somme des durées des opérations d'une liste
    # exécutées sur une machine donnée
    def calculer_duree_jobs(self, machine, liste_jobs):
        a=0
        for job in liste_jobs:
            a+=job.duree_operation(machine)
        return(a)


    # calcul de la borne inférieure en tenant compte d'un ordonnancement en cours
    def calculer_borne_inf(self, ordo, liste_jobs):
        #on calcule tous les rij, qij, et finalement les LBi
        if liste_jobs==[]:
            return(ordo.duree())
        r=[[self.calculer_date_dispo(ordo,machine,job) for job in liste_jobs] for machine in range(self.nb_machines)]
        q=[[self.calculer_duree_latence(ordo,machine,job) for job in liste_jobs] for machine in range(self.nb_machines)]
        LB=[min(r[machine])+self.calculer_duree_jobs(machine,liste_jobs)+min(q[machine])for machine in range(self.nb_machines)]
        #On retourne LB
        return(max(LB))



    # exo 6 A REMPLIR
    # procédure par évaluation et séparation
    def evaluation_separation(self):

        #Initialisation des différentes listes et variables que l'on va utiliser :
        sommet=Sommet([],self.l_job,1000, 1)
        file=[] #file ou on stocke les sommets. On push ensuite le premier sommet :
        heapq.heappush(file, sommet)
        opt=1000
        eval=0
        seq_opt=[]
        i=2

        #tant que la file heap n'est pas vide, on va la parcourir :
        while(file != []):
            sommet=heapq.heappop(file) #on sort le dernier sommet

            if sommet.jobs_non_places() != []:

                for job in sommet.jobs_non_places(): #si il reste des jobs à placer, on les parcours et on va en placer un et tester l'évaluation du sommet

                    sequence = sommet.sequence().copy()
                    sequence.append(job) #on récupere la sequence des jobs et on ajoute le job actuel
                    ordo=Ordonnancement(self.nombre_machines()) #On réalise ensuite un ordonnancement avec cette sequence
                    ordo.ordonnancer_liste_job(sequence)

                    jobs_non_places=sommet.jobs_non_places().copy() #On copie la liste des jobs restant du sommet actuel
                    jobs_non_places.remove(job) #on lui enlève le job en question

                    eval=self.calculer_borne_inf(ordo, jobs_non_places) #évaluation

                    if eval < opt: #si l'évaluation est en dessous de l'optimal actuel, on push dans la file ce sommet.
                        heapq.heappush(file, Sommet(sequence,jobs_non_places,eval,i))
                        i=i+1

            else :
                sequence= sommet.sequence().copy()#on récupere la sequence des jobs
                ordo=Ordonnancement(self.nombre_machines()) #On réalise ensuite un ordonnancement avec cette sequence
                ordo.ordonnancer_liste_job(sequence)

                if ordo.duree() < opt :
                    seq_opt=sequence
                    opt=ordo.duree()

        #Affichage des solutions
        print('Ordre des jobs avec la méthode évaluation / séparation:')
        for job in seq_opt:
            print(job.num)
        print('Durée des jobs avec cette méthode :')
        print(opt)


    def greedyrandomised(self,alpha):

        liste_jobs_restant = self.l_job.copy()
        sequence=[]

        while len(liste_jobs_restant)>1:

            duree_ordo=[]
            RCL=[]

            for job in liste_jobs_restant:
                #On mesure les durées de l'ordonnancement où on rajoute le job i, et on l'ajoute à une liste
                ordo=Ordonnancement(self.nb_machines)
                ordo.ordonnancer_liste_job(sequence)
                ordo.ordonnancer_job(job)
                duree_ordo.append(ordo.duree())
            #On défini l'intervalle de séléction des jobs
            range_time=(max(duree_ordo)-min(duree_ordo))*alpha
            #on selectionne les jobs qui sont dans cet intervale et on les ajoute à la liste RCL
            for i in range(len(duree_ordo)):
                if duree_ordo[i] <= min(duree_ordo)+range_time:
                    RCL.append(liste_jobs_restant[i])
            #On choisit un job au hasard parmis la liste RCL et on l'ajoute à la séquence
            numero=randint(0,len(RCL)-1)
            sequence.append(liste_jobs_restant[numero])
            del(liste_jobs_restant[numero])

        sequence.append(liste_jobs_restant[0])
        #on a un ordonnancement complet, on peut maintenant le renvoyer
        ordo=Ordonnancement(self.nb_machines)
        ordo.ordonnancer_liste_job(sequence)
        return(ordo.duree())

    def test(self,alpha):
        resultat1=[]
        resultat2=[]
        for i in range(10):
            resultat1.append(self.greedyrandomised(alpha))
            resultat2.append(self.greedyrandomised2(alpha))
            print(i)
        print(min(resultat1))
        print(min(resultat2))
        print(mean(resultat1))
        print(mean(resultat2))


    def greedyrandomised2(self,alpha):

        liste_jobs_restant = self.l_job.copy()
        sequence=[]

        while len(liste_jobs_restant)>1:

            duree_ordo=[]
            RCL=[]
            duree=0
            for job in liste_jobs_restant:
                #On mesure les durées de l'ordonnancement où on rajoute le job i, et on l'ajoute à une liste
                ordo=Ordonnancement(self.nb_machines)
                ordo.ordonnancer_liste_job(sequence)
                duree_debut=ordo.duree()
                ordo.ordonnancer_job(job)
                duree_fin=ordo.duree()
                duree_ordo.append((duree_fin-duree_debut)/(ordo.duree())**(1/2))
            #On défini l'intervalle de séléction des jobs
            range_time=(max(duree_ordo)-min(duree_ordo))*alpha
            #on selectionne les jobs qui sont dans cet intervale et on les ajoute à la liste RCL
            for i in range(len(duree_ordo)):
                if duree_ordo[i] <= min(duree_ordo)+range_time:
                    RCL.append(liste_jobs_restant[i])
            #On choisit un job au hasard parmis la liste RCL et on l'ajoute à la séquence
            numero=randint(0,len(RCL)-1)
            sequence.append(liste_jobs_restant[numero])
            del(liste_jobs_restant[numero])

        sequence.append(liste_jobs_restant[0])
        #on a un ordonnancement complet, on peut maintenant le renvoyer
        ordo=Ordonnancement(self.nb_machines)
        ordo.ordonnancer_liste_job(sequence)
        return(ordo.duree())



if __name__ == "__main__":
    job1=Job(1,[2,2,7,8,2,4,6])
    job2=Job(2,[2,3,8,9,3,5,7])
    job3=Job(3,[3,3,7,7,1,2,9])
    job4=Job(4,[3,4,9,9,4,1,7])
    job5=Job(5,[4,2,7,9,2,8,3])
    job6=Job(6,[3,3,1,8,1,8,6])
    job7=Job(7,[4,3,6,6,5,6,8])
    job8=Job(8,[1,3,4,7,4,1,9])
    job9=Job(9,[2,3,8,7,6,9,1])
    job10=Job(10,[3,3,7,4,2,2,5])



    #flow=Flowshop(10,7,[job1,job2,job3,job4,job5,job6,job7,job8,job9,job10])
    #flow.creer_liste_NEH()
    #flow.evaluation_separation()
    flow=Flowshop(0,0,[])
    flow.definir_par("tai51.txt")

    flow.test(0.5)


