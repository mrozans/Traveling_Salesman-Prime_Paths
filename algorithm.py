import pandas as pd
from list_organizing import sieve_of_eratosthenes
from list_organizing import total_distance
from list_organizing import nearest_neighbour
from list_organizing import nn_with_primes
from list_organizing import opt2
import os.path

df_cities = pd.read_csv('input/cities2.csv')
prime_cities = sieve_of_eratosthenes(max(df_cities.CityId))
if os.path.isfile("path.csv"):
    order = pd.read_csv('path.csv')
    path = list(order.Path[:].append(pd.Series([0])))
    print('Start distance is ' + "is {:,}".format(total_distance(df_cities, path, prime_cities)))
else:
    dumbest_path = list(df_cities.CityId[:].append(pd.Series([0])))
    print('Start distance is ' + "is {:,}".format(total_distance(df_cities, dumbest_path, prime_cities)))
    path = nearest_neighbour(df_cities)
    print('Total distance with the Nearest Neighbor' + "is {:,}".format(total_distance(df_cities, path, prime_cities)))
    path = nn_with_primes(path, prime_cities, df_cities)
    print('Total distance with Prime Swaps ' + "is {:,}".format(total_distance(df_cities, path, prime_cities)))
group = 100
jump = 50
start = -1
end = 0
while True:
    print(start)
    if start == -1:
        start = 0
    else:
        start = start + jump
    if start >= (len(path) - 1):
        break
    end = start + group
    if end >= len(path):
        end = len(path) - 1
    opt_path = path[start:end].copy()
    print(total_distance(df_cities, opt_path, prime_cities))
    opt_path = opt2(df_cities, opt_path, False, 1, prime_cities)
    print(total_distance(df_cities, opt_path, prime_cities))
    path[start:end] = opt_path
    if end == len(path) - 2:
        break
print('Total distance with 2-opt ' + "is {:,}".format(total_distance(df_cities, path, prime_cities)))
pd.DataFrame({'Path': path}).to_csv('path.csv', index=False)


