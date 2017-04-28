

# 对置矩阵行列
def rotate_matrix(matrix):
	new_matrix = []
	for col in range(len(matrix[0])):
		new_row = [matrix[row][col] for row in range(len(matrix))]
		new_matrix.append(new_row)
	return new_matrix
		