#!/usr/bin/env python
#ressource : https://sci2s.ugr.es/sites/default/files/files/Teaching/GraduatesCourses/Metaheuristicas/Bibliography/GRASP.pdf

"""Résolution du flowshop de permutation :

 - par algorithme NEH
 - par une méthode évaluation-séparation
 """

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019'

import job
import ordonnancement
import sommet

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
            j = job.Job(i, l)
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
                ordo=ordonnancement.Ordonnancement(self.nb_machines)
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
        sommet=sommet.Sommet([],self.l_job,1000, 1)
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
                ordo=ordonnancement.Ordonnancement(self.nb_machines)
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
        ordo=ordonnancement.Ordonnancement(self.nb_machines)
        ordo.ordonnancer_liste_job(sequence)
        return [(ordo.duree()),ordo]

    def test(self,alpha):
        resultat1=[]
        resultat2=[]
        for i in range(10):
            resultat1.append(self.greedyrandomised(alpha)[0])
            resultat2.append(self.greedyrandomised2(alpha)[0])
            print(i)
        print(min(resultat1))
        print(min(resultat2))
        print(mean(resultat1))
        print(mean(resultat2))

    def greedyrandomised_rank(self):
        alpha=random()

        liste_jobs_restant = self.l_job.copy()
        sequence=[]

        while len(liste_jobs_restant)>1:

            duree_ordo=[]
            RCL=[]

            for job in liste_jobs_restant:
                #On mesure les durées de l'ordonnancement où on rajoute le job i, et on l'ajoute à une liste
                ordo=ordonnancement.Ordonnancement(self.nb_machines)
                ordo.ordonnancer_liste_job(sequence)
                ordo.ordonnancer_job(job)
                duree_ordo.append(ordo.duree())
            #On défini l'intervalle de séléction des jobs
            range_time=(max(duree_ordo)-min(duree_ordo))*alpha
            #on selectionne les jobs qui sont dans cet intervale et on les ajoute à la liste RCL
            for i in range(len(duree_ordo)):
                if duree_ordo[i] <= min(duree_ordo)+range_time:
                    RCL.append(liste_jobs_restant[i])
            RCL_probabilise=self.RCL_probabilise(self.rank(RCL))
            #On choisit un job au hasard parmis la liste RCL et on l'ajoute à la séquence
            candidat=RCL_probabilise[randint(0,len(RCL_probabilise)-1)]

            numero=0
            for i in range(len(liste_jobs_restant)):
                if liste_jobs_restant[i].calcul_distance_euclidienne()==candidat.calcul_distance_euclidienne():
                    numero=i

            sequence.append(liste_jobs_restant[numero])
            del(liste_jobs_restant[numero])

        sequence.append(liste_jobs_restant[0])
        #on a un ordonnancement complet, on peut maintenant le renvoyer
        ordo=ordonnancement.Ordonnancement(self.nb_machines)
        ordo.ordonnancer_liste_job(sequence)
        return [(ordo.duree()),ordo]




    def greedyrandomised2(self,alpha):

        liste_jobs_restant = self.l_job.copy()
        sequence=[]

        while len(liste_jobs_restant)>1:

            duree_ordo=[]
            RCL=[]
            duree=0
            for job in liste_jobs_restant:
                #On mesure les durées de l'ordonnancement où on rajoute le job i, et on l'ajoute à une liste
                ordo=ordonnancement.Ordonnancement(self.nb_machines)
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
        ordo=ordonnancement.Ordonnancement(self.nb_machines)
        ordo.ordonnancer_liste_job(sequence)
        return[(ordo.duree()),ordo]

    # on cherche des meilleurs ordonnacement que celui initilal, on changeant à chaque fois l'ordre de deux job
    def recherchel_echange_job_radom(self,iteration,ordonnancement):
        duree_test=ordonnancement.duree_ordo()
        sequence_test=ordonnancement.seq()
        for i in range (iteration):
            ordo = ordonnancement.Ordonnancement(self.nb_machines)
            new_sequence=sequence_test
            index1=random.randint(0,self.nb_jobs-1)
            index2=random.randint(0,self.nb_jobs-1)
            new_sequence[index1]=sequence_test[index2]
            new_sequence[index2]=sequence_test[index1]
            ordo.ordonnancer_liste_job(new_sequence)
            if ordo.duree()<duree_test:
                duree_test=ordo.duree()
                sequence_test=new_sequence
        ordonnancement_final=ordonnancement.Ordonnancement(self.nb_machines)
        ordonnancement_final.ordonnacer_liste_jpb(sequence_test)
        return ordonnancement_final

    def recherchel_echange_job_total(self,ordonnancement_debut):
        duree_test=ordonnancement_debut.duree()
        print("dure")
        print(duree_test)
        sequence_test=ordonnancement_debut.sequence()
        sequence_final=[]
        for i in range (self.nb_jobs):
            for j in range (self.nombre_jobs()):
                if j!=i:

                    ordo = ordonnancement.Ordonnancement(self.nb_machines)
                    new_sequence=sequence_test

                    new_sequence[i]=sequence_test[j]
                    new_sequence[j]=sequence_test[i]
                    ordo.ordonnancer_liste_job(new_sequence)
                    if ordo.duree()<duree_test:
                        duree_test=ordo.duree()
                        sequence_final=ordo.sequence()

        ordonnancement_final=ordonnancement.Ordonnancement(self.nb_machines)

        ordonnancement_final.ordonnancer_liste_job(sequence_final)
        return ordonnancement_final

    def grasp(self,nb_candidat):
        alpha=0.5
        liste_ordonnacement=[]
        for i in range(nb_candidat):
            ordo_first=self.greedyrandomised_rank()[1]

            ordo=self.recherchel_echange_job_total(ordo_first)
            liste_ordonnacement.append(ordo)

        min=1000000000
        ordonnacement_final=ordonnancement.Ordonnancement(self.nb_machines)
        for j in range(len(liste_ordonnacement)):
            if liste_ordonnacement[j].duree()<min:
                min=liste_ordonnacement[j].duree()
                ordonnacement_final=liste_ordonnacement[j]
        return ordonnacement_final,ordonnacement_final.duree()



    def rank_recursive(self, candidate_list, result):
        # Condition d'arret
        if len(candidate_list) > 0:
            # Initialisation
            index_min = 0
            minimum = 0

            minimum = candidate_list[0].calcul_distance_euclidienne()

            # Hérédité
            for i in range(len(candidate_list)):
                distance_euclidienne = 0
                job = candidate_list[i]
                for j in range(len(job)):
                    distance_euclidienne = job.calcul_distance_euclidienne()
                if distance_euclidienne < minimum:
                    minimum = distance_euclidienne
                    index_min = i
            result.append(candidate_list[index_min])
            candidate_list.pop(index_min)
            self.rank(candidate_list, result)
        # Conclusion
        return result

    def rank(self, candidate_list):
        list_eucli=[]
        resultat=[]

        index_min = 0
        minimum = 10000000000000

        for j in range(len(candidate_list)):
            distance_euclidienne_c=candidate_list[j].calcul_distance_euclidienne()
            list_eucli.append(distance_euclidienne_c)
            if minimum>distance_euclidienne_c:
                minimum=distance_euclidienne_c
                index_min=j

        resultat.append(candidate_list[index_min])



        for i in range (len(candidate_list)):
            max=10000000000


            for j in range(len(candidate_list)):

                if list_eucli[j]<max and list_eucli[j] > minimum:
                    minimum=list_eucli[j]
                    index_min=j
            resultat.append(candidate_list[index_min])
        return resultat

    def RCL_probabilise(self, rank_list):
        RCL_prob = []
        for rang in range(len(rank_list), 1, -1):
            for i in range(rang):
                RCL_prob.append(rank_list[len(rank_list) - rang])
        return RCL_prob







if __name__ == "__main__":



    #flow=Flowshop(10,7,[job1,job2,job3,job4,job5,job6,job7,job8,job9,job10])
    #flow.creer_liste_NEH()
    #flow.evaluation_separation()
    flow=Flowshop(0,0,[])
    flow.definir_par("tai51.txt")


    print(flow.grasp(10))


