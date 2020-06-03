import csv

import pandas as pd
import numpy as np

# using sieve of eratosthenes


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


def total_distance(dfcity, path):
    prev_city = path[0]
    distance = 0
    step_num = 1
    for city_num in path[1:]:
        next_city = city_num
        distance = distance + \
            np.sqrt(pow((dfcity.X[city_num] - dfcity.X[prev_city]), 2) + pow((dfcity.Y[city_num] - dfcity.Y[prev_city]), 2)) * \
            (1 + 0.1*((step_num % 10 == 0)*int(not(prime_cities[prev_city]))))
        prev_city = next_city
        step_num = step_num + 1
    return distance


def nearest_neighbour():
    cities = pd.read_csv("input/cities.csv")
    ids = cities.CityId.values[1:]
    xy = np.array([cities.X.values, cities.Y.values]).T[1:]
    path = [0, ]
    while len(ids) > 0:
        #print(len(ids))
        last_x, last_y = cities.X[path[-1]], cities.Y[path[-1]]
        dist = ((xy - np.array([last_x, last_y]))**2).sum(-1)
        nearest_index = dist.argmin()
        path.append(ids[nearest_index])
        ids = np.delete(ids, nearest_index, axis=0)
        xy = np.delete(xy, nearest_index, axis=0)
    path.append(0)
    return path


df_cities = pd.read_csv('input/cities.csv')
prime_cities = sieve_of_eratosthenes(max(df_cities.CityId))

nnpath = nearest_neighbour()

nnpath_with_primes = nnpath.copy()
for index in range(20, len(nnpath_with_primes)-30):
    city = nnpath_with_primes[index]
    if prime_cities[city] & ((index + 1) % 10 != 0):
        for i in range(-1, 3):
            tmp_path = nnpath_with_primes.copy()
            swap_index = (int((index+1)/10) + i)*10 - 1
            tmp_path[swap_index], tmp_path[index] = tmp_path[index], tmp_path[swap_index]
            if total_distance(df_cities, tmp_path[min(swap_index, index) - 1 : max(swap_index, index) + 2]) < \
                    total_distance(df_cities, nnpath_with_primes[min(swap_index, index) - 1: max(swap_index, index) + 2]):
                nnpath_with_primes = tmp_path.copy()
                break
print('Total distance with the Nearest Neighbor With Prime Swaps ' + "is {:,}".format(total_distance(df_cities, nnpath_with_primes)))