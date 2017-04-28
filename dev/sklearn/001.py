# 基于 Python 和 Scikit-Learn 的机器学习介绍
 # http://python.jobbole.com/81721/


import os
import numpy as np
import urllib.request
from sklearn import preprocessing


# ----------------------------------------------------------------------
# 数据读取（网络加载）
# @param data_url: url with dataset
def get_net_data(data_url = 'pima-indians-diabetes/pima-indians-diabetes.data'):
	# download the file
	databases_url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/'
	return  urllib.request.urlopen(databases_url + data_url)

# 数据读取（本地读取）
def get_local_data(data_file_name = 'pima-indians-diabetes.data'):
	data_file_path = os.path.join('data', data_file_name)
	data_file = open(data_file_path)
	content = data_file.readlines()
	data_file.close()
	return content

# ----------------------------------------------------------------------
# 生成数据集
def generate_dataset(data):
	# load the CSV file as a numpy matrix
	dataset = np.loadtxt(data, delimiter = ',')
	# separate the data from the target attributes
	X = dataset[:,0:7]	#attributes 特征值数组
	Y = dataset[:,8]	#label 目标变量
	return X, Y

# ----------------------------------------------------------------------
# 数据标准化(规格化)
# 标准化包括替换所有特征的名义值，让它们每一个的值在0和1之间。
# 而对于规格化，它包括数据的预处理，使得每个特征的值有0和1的离差。
def normalize_scale_data(X):
	# normalize the data attributes
	normalized_X = preprocessing.normalize(X)
	# standardize the data attributes
	standardized_X = preprocessing.scale(X)

# ----------------------------------------------------------------------
# 特征的选取
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier






# ----------------------------------------------------------------------
# raw_data = get_net_data()
data = get_local_data()
X, Y = generate_dataset(data)
# normalize_scale_data(X)





# from sklearn import metrics
# from sklearn.ensemble import ExtraTreesClassifier
# model = ExtraTreesClassifier()
# model.fit(X, y)
# # display the relative importance of each attribute
# print(model.feature_importances_)


# from sklearn.feature_selection import RFE
# from sklearn.linear_model import LogisticRegression
# model = LogisticRegression()
# # create the RFE model and select 3 attributes
# rfe = RFE(model, 3)
# rfe = rfe.fit(X, y)
# # summarize the selection of the attributes
# print(rfe.support_)
# print(rfe.ranking_)