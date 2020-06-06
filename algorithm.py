import csv

import pandas as pd
import numpy as np


def sieve_of_eratosthenes(n):
    primes = [True for i in range(n+1)]  # Start assuming all numbers are primes
    primes[0] = False  # 0 is not a prime
    primes[1] = False  # 1 is not a prime
    for i in range(2, int(np.sqrt(n)) + 1):
        if primes[i]:
            k = 2
            while i*k <= n:
                primes[i*k] = False
                k += 1
    return primes


def single_distance(dfcity, path, prev_city):
    city_num = prev_city+1
    step_num = city_num
    result = np.sqrt(pow((dfcity.X[path[city_num]] - dfcity.X[path[prev_city]]), 2) +
                     pow((dfcity.Y[path[city_num]] - dfcity.Y[path[prev_city]]), 2)) * \
                    (1 + 0.1*((step_num % 10 == 0)*int(not(prime_cities[prev_city]))))
    return result


def total_distance(dfcity, path):
    prev_city = path[0]
    distance = 0
    step_num = 1
    for city_num in path[1:]:
        next_city = city_num
        distance = distance + \
            np.sqrt(pow((dfcity.X[city_num] - dfcity.X[prev_city]), 2) +
                    pow((dfcity.Y[city_num] - dfcity.Y[prev_city]), 2)) * \
                   (1 + 0.1*((step_num % 10 == 0)*int(not(prime_cities[prev_city]))))
        prev_city = next_city
        step_num = step_num + 1
    return distance


def nearest_neighbour(dfcity):
    ids = dfcity.CityId.values[1:]
    xy = np.array([dfcity.X.values, dfcity.Y.values]).T[1:]
    path = [0, ]
    while len(ids) > 0:
        print(len(ids))
        last_x, last_y = dfcity.X[path[-1]], dfcity.Y[path[-1]]
        dist = ((xy - np.array([last_x, last_y]))**2).sum(-1)
        nearest_index = dist.argmin()
        path.append(ids[nearest_index])
        ids = np.delete(ids, nearest_index, axis=0)
        xy = np.delete(xy, nearest_index, axis=0)
    path.append(0)
    return path


def opt2(df_city, path, simplified):
    swap = False
    best_path = path
    best_improvement = 0
    for i in range(1, (len(path)-1)):
        print(i)
        for j in range(i+2, (len(path)-1)):

            start = single_distance(df_city, path, i-1) + single_distance(df_city, path, j-1)
            selected_path = []
            selected_path += path[:i]
            selected_path += list(reversed(path[i:j]))
            selected_path += path[j:]
            finish = single_distance(df_city, selected_path, i-1) + single_distance(df_city, selected_path, j-1)
            improvement = start - finish
            if best_improvement < improvement:
                best_path = selected_path
                best_improvement = improvement
                swap = True
            if simplified and swap:
                break
        if simplified and swap:
            break
    if swap:
        print("Next iteration of 2-opt?(y/n)")
        answer = input()
        if answer == "y":
            return opt2(df_city, best_path, simplified)
    return best_path


df_cities = pd.read_csv('input/cities2.csv')
prime_cities = sieve_of_eratosthenes(max(df_cities.CityId))
# # dumbest_path = list(df_cities.CityId[:].append(pd.Series([0])))
# # print(total_distance(df_cities, dumbest_path))
# # path = opt2(df_cities, dumbest_path)
# # print(path)
# # print(total_distance(df_cities, path))
#
#
# nnpath = nearest_neighbour(df_cities)
#
# nnpath_with_primes = nnpath.copy()
# for index in range(20, len(nnpath_with_primes)-30):
#     city = nnpath_with_primes[index]
#     if prime_cities[city] & ((index + 1) % 10 != 0):
#         for i in range(-1, 3):
#             tmp_path = nnpath_with_primes.copy()
#             swap_index = (int((index+1)/10) + i)*10 - 1
#             tmp_path[swap_index], tmp_path[index] = tmp_path[index], tmp_path[swap_index]
#             if total_distance(df_cities, tmp_path[min(swap_index, index) - 1 : max(swap_index, index) + 2]) < \
#                     total_distance(df_cities, nnpath_with_primes[min(swap_index, index) - 1: max(swap_index, index) + 2]):
#                 nnpath_with_primes = tmp_path.copy()
#                 break
#print('Total distance with the Nearest Neighbor With Prime Swaps ' + "is {:,}".format(total_distance(df_cities, nnpath_with_primes)))
# path = opt2(df_cities, nnpath_with_primes, False)
# print(total_distance(df_cities, path))
