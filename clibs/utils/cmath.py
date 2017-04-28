

# 计算两点（欧几里得）距离
def calculate_distance_euclidean(a, b):
	sum_squares = sum([(a[i] - b[i]) ** 2 for i in range(len(a))])
	sqrt_sum = sum_squares ** 0.5
	return 1 / (1 + sqrt_sum)


# 计算两点的皮尔逊相关系数
def calculate_pearson_cc(a, b, reverse = False):
	result = 0
	cc_len = len(a)
	# 如果两者没有共同之处，则返回0
	if cc_len > 0:
		sum_a = sum([x for x in a])
		sum_b = sum([x for x in b])
		sum_a_squares = sum([x ** 2 for x in a])
		sum_b_squares = sum([x ** 2 for x in b])
		sum_ab_plus = sum([a[i] * b[i] for i in range(cc_len)])
		denominator = (sum_a_squares - sum_a ** 2 / cc_len) * (sum_b_squares - sum_b ** 2 / cc_len)
		numerator = sum_ab_plus - sum_a * sum_b / cc_len
		denominator = denominator ** 0.5
		if denominator == 0:
			denominator = numerator
		result = numerator / denominator
	if not reverse:
		return result
	return 1 - result


# 计算两点的皮尔逊相关系数(相似度越大的两个元素距离越近，才用1去减 )
def calculate_pearson_cc_reverse(a, b):
	return calculate_pearson_cc(a, b, reverse = True)


# 计算两点的Tanimoto系数
def calculate_tinimoto(a, b):
	c = [v for v in a if v in b]
	return float(len(c) / (len(a) + len(b) - len(c)))