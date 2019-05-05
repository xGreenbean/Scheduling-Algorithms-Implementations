import numpy as np
# regex for replacement 214?+\d*..
global ids_arr,pj_arr,ej_arr,wj_arr,accepted_jobs,results,threshold
#for replacig with infinity later.
threshold = 2140000000

#to identify order after sorting
ids_arr = [1, 2, 3, 4, 5, 6]
pj_arr = [3, 1, 3, 2, 3, 3]
ej_arr = [4, 5, 6, 6, 1, 5]
wj_arr = [5, 6, 1, 1, 2, 4]
#for processing time/weight sorting.
pj_div_wj_arr = []

#number of jobs
n = 6
#?
E = 8
#total time
T = int(sum(iter(pj_arr)))
#the dynamic programming table
results = np.zeros((n + 1, E + 1, T + 1))

#sort
for j in range(n):
    pj_div_wj_arr.append((1. * pj_arr[j])/wj_arr[j])
to_sort = zip(pj_div_wj_arr, pj_arr,ej_arr, wj_arr, ids_arr)
to_sort = sorted(to_sort)

pj_arr = [x[1] for x in to_sort]
ej_arr = [x[2] for x in to_sort]
wj_arr = [x[3] for x in to_sort]
ids_arr = [x[4] for x in to_sort]


for t in range(T + 1):
    for e in range(E + 1):
        if t == 0:
            results[0][e][t] = 0
        else:
            results[0][e][t] = 2147483647

#doing the dynamic programming iterativly
for j in range(n):
    for t in range(T + 1):
        for e in range(E + 1):
            if pj_arr[j] > t and ej_arr[j] > e:
                results[j + 1][e][t] = 2147483647
            elif pj_arr[j] > t and ej_arr[j] <= e:
                results[j + 1][e][t] = results[j][e - ej_arr[j]][t]
            elif pj_arr[j] <= t and ej_arr[j] > e:
                results[j + 1][e][t] = results[j][e][t - pj_arr[j]]+ wj_arr[j]*t
            elif pj_arr[j] <= t and ej_arr[j] <= e:
                results[j + 1][e][t] = min((results[j][e][t - pj_arr[j]] + wj_arr[j]*t),
                                           (results[j][e - ej_arr[j]][t]))
accepted_jobs = []

#get min index
indexes = np.argmin(results[n])
row = int(indexes / T + 1)
col = int(indexes % (T + 1))


#stupid padding
pj_arr.insert(0, 0)
ej_arr.insert(0, 0)
wj_arr.insert(0, 0)

print(pj_arr)
def backtrack(j, e, t ):
    if j <= 0:
        return
    if pj_arr[j] > t and ej_arr[j] > e:
        return
    elif pj_arr[j] > t and ej_arr[j] <= e:
        backtrack(j - 1, e - ej_arr[j], t)
    elif pj_arr[j] <= t and ej_arr[j] > e:
        accepted_jobs.append(j)
        backtrack(j - 1, e, t - pj_arr[j])
    elif pj_arr[j] <= t and ej_arr[j] <= e:
        if wj_arr[j]*t + results[j - 1][e][t - pj_arr[j]] <= results[j - 1][e - ej_arr[j]][t]:
            accepted_jobs.append(j)
            backtrack(j-1, e, t - pj_arr[j])
        else:
            backtrack(j-1, e - ej_arr[j], t)

backtrack(n, row, col)

print("accepted jobs by id: ",[ids_arr[i -1] for i in accepted_jobs])

#for printing table to csv file
def print_to_csv():
    with open("results.csv", "w") as f:
        for j in range(n + 1):
            f.write('\n')
            f.write('\n')
            if j > 0:
                f.write("job id = " + str (ids_arr[j -1]) + ', ' +
                        "pj = " + str(pj_arr[j - 1]) + ', ' +
                        "ej = " + str(ej_arr[j - 1]) + ', ' +
                        "wj = " + str(wj_arr[j - 1]))
            for e in range(E + 1):
                f.write('\n')
                for t in range(T + 1):
                    if results[j][e][t] > threshold:
                        f.write('inf' + ',')
                    else:
                        f.write(str(np.round(results[j][e][t])) + ',')









