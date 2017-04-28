import sys
sys.path.append('../../../clibs/')
import utils.cmath as cmath

import data.critics as critics


dataset = critics.dataset
print(dataset['Lisa Rose'])
print(dataset['Lisa Rose']['Lady in the Water'])

print(dataset['Toby'])
# dataset['Toby']['Snake on a Plane'] = 4.5
# print(dataset['Toby'])


import math
distance = math.sqrt((4.5 - 4) ** 2 + (1 - 2) ** 2)
print(distance)
dist_rec = 1 / (1 + distance)
print(dist_rec)


import recommendations as rec
sim_dist = rec.similar_distance(dataset, 'Lisa Rose', 'Gene Seymour')
print(sim_dist)


sim_pearson = rec.similar_pearson(dataset, 'Lisa Rose', 'Gene Seymour')
print(sim_pearson)


print("---------------------------------------------------------------------")
test_a1 = [3.5, 4.5]
test_a2 = [1.5, 2.5]
test_b = [1.5, 3.5]
print(cmath.calculate_pearson_cc(test_a1, test_b))
print(cmath.calculate_pearson_cc(test_a2, test_b))
print(cmath.calculate_distance_euclidean(test_a1, test_b))
print(cmath.calculate_distance_euclidean(test_a2, test_b))


print("---------------------------------------------------------------------")
top_matches = rec.get_top_matches(dataset, 'Toby', n = 3)
print(top_matches)
top_matches = rec.get_top_matches(dataset, 'Toby', n = 3, \
	similarity = rec.similar_distance)
print(top_matches)


print("---------------------------------------------------------------------")
print(rec.get_recommendations(dataset, 'Toby'))
print(rec.get_recommendations(dataset, 'Toby', \
	similarity = rec.similar_distance))


print("---------------------------------------------------------------------")
movies = rec.transform_dataset(dataset)
print(movies)
print(rec.get_top_matches(movies, 'Superman Returns'))
print(rec.get_recommendations(movies, 'Just My Luck'))


print("---------------------------------------------------------------------")
print(rec.calculate_similar_items(dataset))


print("---------------------------------------------------------------------")
print(rec.get_recommended_items(dataset, rec.calculate_similar_items(dataset), 'Toby'))





