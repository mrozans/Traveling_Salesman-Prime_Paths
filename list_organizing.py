import numpy as np


def sieve_of_eratosthenes(n):
    primes = [True for i in range(n + 1)]  # Start assuming all numbers are primes
    primes[0] = False  # 0 is not a prime
    primes[1] = False  # 1 is not a prime
    for i in range(2, int(np.sqrt(n)) + 1):
        if primes[i]:
            k = 2
            while i * k <= n:
                primes[i * k] = False
                k += 1
    return primes


def single_distance(dfcity, path, prev_city, prime_cities):
    city_num = prev_city + 1
    step_num = city_num
    result = np.sqrt(pow((dfcity.X[path[city_num]] - dfcity.X[path[prev_city]]), 2) +
                     pow((dfcity.Y[path[city_num]] - dfcity.Y[path[prev_city]]), 2)) * \
             (1 + 0.1 * ((step_num % 10 == 0) * int(not (prime_cities[prev_city]))))
    return result


def total_distance(dfcity, path, prime_cities):
    prev_city = path[0]
    distance = 0
    step_num = 1
    for city_num in path[1:]:
        next_city = city_num
        distance = distance + \
                   np.sqrt(pow((dfcity.X[city_num] - dfcity.X[prev_city]), 2) +
                           pow((dfcity.Y[city_num] - dfcity.Y[prev_city]), 2)) * \
                   (1 + 0.1 * ((step_num % 10 == 0) * int(not (prime_cities[prev_city]))))
        prev_city = next_city
        step_num = step_num + 1
    return distance


def nearest_neighbour(dfcity):
    ids = dfcity.CityId.values[1:]
    xy = np.array([dfcity.X.values, dfcity.Y.values]).T[1:]
    path = [0, ]
    while len(ids) > 0:
        last_x, last_y = dfcity.X[path[-1]], dfcity.Y[path[-1]]
        dist = ((xy - np.array([last_x, last_y])) ** 2).sum(-1)
        nearest_index = dist.argmin()
        path.append(ids[nearest_index])
        ids = np.delete(ids, nearest_index, axis=0)
        xy = np.delete(xy, nearest_index, axis=0)
    path.append(0)
    return path


def nn_with_primes(nnpath_with_primes, prime_cities, df_cities):
    for index in range(20, len(nnpath_with_primes) - 30):
        city = nnpath_with_primes[index]
        if prime_cities[city] & ((index + 1) % 10 != 0):
            for i in range(-1, 3):
                tmp_path = nnpath_with_primes.copy()
                swap_index = (int((index + 1) / 10) + i) * 10 - 1
                tmp_path[swap_index], tmp_path[index] = tmp_path[index], tmp_path[swap_index]
                if total_distance(df_cities, tmp_path[min(swap_index, index) - 1: max(swap_index, index) + 2],
                                  prime_cities) < total_distance(df_cities,
                                                                 nnpath_with_primes[min(swap_index, index) -
                                                                                    1: max(swap_index, index) + 2],
                                                                 prime_cities):
                    nnpath_with_primes = tmp_path.copy()
                    break
    return nnpath_with_primes


def opt2(df_city, path, simplified, limit, prime_cities):
    swap = False
    best_path = path
    best_improvement = 0
    for i in range(1, (len(path) - 1)):
        for j in range(i + 2, (len(path) - 1)):
            start = single_distance(df_city, path, i - 1, prime_cities) + single_distance(df_city, path, j - 1,
                                                                                          prime_cities)
            selected_path = []
            selected_path += path[:i]
            selected_path += list(reversed(path[i:j]))
            selected_path += path[j:]
            finish = single_distance(df_city, selected_path, i - 1, prime_cities) + single_distance(df_city,
                                                                                                    selected_path,
                                                                                                    j - 1, prime_cities)
            improvement = start - finish
            if best_improvement < improvement:
                best_path = selected_path
                best_improvement = improvement
                swap = True
            if simplified and swap:
                break
        if simplified and swap:
            break
    limit = limit - 1
    if swap and limit > 0:
        return opt2(df_city, best_path, simplified, limit, prime_cities)
    return best_path
