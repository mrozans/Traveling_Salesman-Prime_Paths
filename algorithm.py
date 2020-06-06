import pandas as pd
from list_organizing import sieve_of_eratosthenes
from list_organizing import total_distance
from list_organizing import nearest_neighbour
from list_organizing import nn_with_primes
from list_organizing import opt2
import genetic_algorithm

df_cities = pd.read_csv('input/cities2.csv')
prime_cities = sieve_of_eratosthenes(max(df_cities.CityId))
dumbest_path = list(df_cities.CityId[:].append(pd.Series([0])))
print('Start distance is ' + "is {:,}".format(total_distance(df_cities, dumbest_path, prime_cities)))
path = nearest_neighbour(df_cities)
print('Total distance with the Nearest Neighbor' + "is {:,}".format(total_distance(df_cities, path, prime_cities)))
path = nn_with_primes(path, prime_cities, df_cities)
print('Total distance with Prime Swaps ' + "is {:,}".format(total_distance(df_cities, path, prime_cities)))
group = 50
jump = 250
start = 0
end = 0
while True:
    if start == 0:
        start = 1
    else:
        start = start + jump
    end = start + group
    if end >= len(path):
        end = len(path) - 1
    gen_path = path[start:end].copy()
    gen = genetic_algorithm.GeneticAlgorithm(gen_path, df_cities, path[start-1], path[end], prime_cities)
    selected_path = gen.calculate()
    a = total_distance(df_cities, path[start - 1:end + 1], prime_cities)
    b = total_distance(df_cities, [path[start - 1]] + selected_path + [path[end]], prime_cities)
    print(a)
    print(b)
    if a > b:
        path[start:end] = selected_path
    if end == len(path) - 2:
        break
print('Total distance genetic algorithm ' + "is {:,}".format(total_distance(df_cities, path, prime_cities)))
path = opt2(df_cities, path, True, 3, prime_cities)
print('Total distance with 2-opt ' + "is {:,}".format(total_distance(df_cities, path, prime_cities)))
pd.DataFrame({'Path': path}).to_csv('path.csv', index=False)


