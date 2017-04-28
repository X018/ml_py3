import sys
sys.path.append('../../../clibs/')

import os
import utils.cmath as cmath
import utils.cfile as cfile
import utils.cmatrix as cmatrix
import hierachical_clustering as hclustering
import kmeans_clustering as kclustering



BIN_DIR = 'bin'
DATA_DIR = 'data'


blog_names, words, data = cfile.read_file(os.path.join(DATA_DIR, 'blogdata.txt'))


def test_hierachical_clustering():
	cluster_node = hclustering.hierachical_cluster(data)
	hclustering.print_cluster_nodes(cluster_node, labels = blog_names)
	hclustering.draw_dendrogram(cluster_node, blog_names, jpeg = os.path.join(BIN_DIR, 'hclustering_pearson.jpg'))

	cluster_node = hclustering.hierachical_cluster(data, similarity = cmath.calculate_distance_euclidean)
	hclustering.draw_dendrogram(cluster_node, blog_names, jpeg = os.path.join(BIN_DIR, 'hclustering_euclidean.jpg'))

	cluster_node = hclustering.hierachical_cluster(data, similarity = cmath.calculate_tinimoto)
	hclustering.draw_dendrogram(cluster_node, blog_names, jpeg = os.path.join(BIN_DIR, 'hclustering_tinimoto.jpg'))


	rotate_data = cmatrix.rotate_matrix(data)
	cluster_node = hclustering.hierachical_cluster(rotate_data)
	hclustering.print_cluster_nodes(cluster_node, labels = words)
	hclustering.draw_dendrogram(cluster_node, words, jpeg = os.path.join(BIN_DIR, 'column_clustering.jpg'))


def test_kmeans_clustering():
	best_matches = kclustering.kmeans_cluster(data, k = 10)
	print([[blog_names[i] for i in matches] for matches in best_matches])


# test_hierachical_clustering()
test_kmeans_clustering()