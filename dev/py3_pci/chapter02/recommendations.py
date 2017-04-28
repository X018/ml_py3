import utils.cmath as cmath


def get_similar_data(dataset, p1, p2):
	shared_item = [item for item in dataset[p1] if item in dataset[p2]]
	shared_item_p1 = [dataset[p1][item] for item in shared_item]
	shared_item_p2 = [dataset[p2][item] for item in shared_item]
	return shared_item_p1, shared_item_p2


def similar_distance(dataset, p1, p2):
	shared_item_p1, shared_item_p2 = get_similar_data(dataset, p1, p2)
	return cmath.calculate_distance_euclidean(shared_item_p1, shared_item_p2)


def similar_pearson(dataset, p1, p2):
	shared_item_p1, shared_item_p2 = get_similar_data(dataset, p1, p2)
	return cmath.calculate_pearson_cc(shared_item_p1, shared_item_p2)

# 为评论者打分
# 从反映偏好的字典中返回最为匹配者
# 返回结果的个数和相似度函数均为可选参数
def get_top_matches(dataset, p, n = 5, similarity = similar_pearson):
	matches = [(similarity(dataset, p, other), other) for other in dataset if p != other]
	
	# 对列表进行排序，评价值最高者排在最前面
	matches.sort()
	matches.reverse()
	return matches[0:n]

# 推荐物品
# 利用所有他人评价值的加权平均，为某人提供建议
def get_recommendations(dataset, p, similarity = similar_pearson):
	totals, sim_sums = {}, {}
	for other in dataset:
		# 不要和自己做比较
		if p == other : continue
		sim = similarity(dataset, p, other)

		# 忽略评价值为零或小于零的情况
		if sim < 0 : continue

		for item in dataset[other]:
			# 只对自己还未曾看过的影片进行评价
			if item not in dataset[p] or dataset[p][item] == 0:
				# 相似度*评价值
				totals.setdefault(item, 0)
				totals[item] += dataset[other][item] * sim
				# 相似度之和
				sim_sums.setdefault(item, 0)
				sim_sums[item] += sim

	# 建立一个归一化的列表(total / sim_sums[item]结果为评分均值)
	rankings = [(total / sim_sums[item], item) for item, total in totals.items()]
	
	# 排序列表
	rankings.sort()
	rankings.reverse()
	return rankings

# 匹配商品
# 商品与人员对换:将用户对电影的评分改为，电影对用户的适应度
def transform_dataset(dataset):
	result = {}
	for p in dataset:
		for item in dataset[p]:
			# 将物品和人员对调
			result.setdefault(item, {})
			result[item][p] = dataset[p][item]
	return result

# 预先进行计算（计算物品相似度）
def calculate_similar_items(dataset, n = 10, similarity = similar_distance):
	# 把用户对物品的评分，改为物品对用户的适应度 
	items = transform_dataset(dataset)
	# 相似物品的字典
	return dict([(item, get_top_matches(items, item, n, similarity)) for item in items])


def get_recommended_items(dataset, item_similar, p):
	scores = {}
	total_similar = {}
	user_rating = dataset[p]
	# 循环遍历由当前用户评分的物品  
	for (item, rating) in user_rating.items():
		# 循环遍历与当前物品相近的物品
		for (similar, item2) in item_similar[item]:
			# 如果该用户已经对当前物品做过评价，则将其忽略
			if item2 in user_rating: continue

			# 打分和相似度的加权之和
			scores.setdefault(item2, 0)
			scores[item2] += similar * rating

			# 某一电影的与其他电影的相似度之和
			total_similar.setdefault(item2, 0)
			total_similar[item2] += similar

	# 将经过加权的评分除以相似度，求出对这一电影的评分
	rankings = [(score / total_similar[item], item) for item, score in scores.items()]
	rankings.sort()
	rankings.reverse()
	return rankings




			