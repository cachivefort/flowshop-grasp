def rank(candidate_list, result):
    #Condition d'arret
    if len(candidate_list)>0:
        #Initialisation
        index_min = 0
        minimum = 0
        for j in range(len(candidate_list[0])):
            minimum = calcul_distance_euclidienne(candidate_list[0])

        #Hérédité
        for i in range(len(candidate_list)):
            distance_euclidienne = 0
            job = candidate_list[i]
            for j in range(len(job)):
                distance_euclidienne = calcul_distance_euclidienne(job)
            if distance_euclidienne < minimum:
                minimum = distance_euclidienne
                index_min = i
        result.append(candidate_list[index_min])
        candidate_list.pop(index_min)
        rank(candidate_list, result)
    #Conclusion
    return result


def calcul_distance_euclidienne(job):
    distance_euclidienne = 0
    for i in range(len(job)-1):
        distance_euclidienne += abs(job[i]-job[i+1])
        distance_euclidienne = distance_euclidienne**(1/2)
    return distance_euclidienne


    #test de la fonction rank
job1 = [2, 2, 7, 8, 2, 4, 6]
job2 = [2, 3, 8, 9, 3, 5, 7]
job3 = [3, 3, 7, 7, 1, 2, 9]
job4 = [3, 4, 9, 9, 4, 1, 7]
candidate_list = [job1, job2, job3, job4]
result = []
print(rank(candidate_list, result))
print(calcul_distance_euclidienne(job1))
print(calcul_distance_euclidienne(job2))
print(calcul_distance_euclidienne(job3))
print(calcul_distance_euclidienne(job4))



   #fonction qui retourne un RCL trié selon un mediateur epsilon
    '''def rank(self, candidate_list, eps):
        if eps > 0.5 :
            copie = []
            for job in candidate_list:
                distance_euclidienne = 0
                for i in range(len(job)):
                    distance_euclidienne += abs(job[i] - job[i+1])**2
                distance_euclidienne = distance_euclidienne**(1/2)
                if distance_euclidienne < eps:
                    copie.append(job)
                    candidate_list.remove(job)
            for job_restant in candidate_list:
                copie.append(job_restant)
            rank(self, copie, eps/2)
        return copie
'''
