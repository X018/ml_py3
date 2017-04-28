# py3_pci/chapter003/hierachical_clustering.py
# “集体智慧编程”之第三章：“发现群组”的 分级聚类



import sys
sys.path.append('../../../clibs/')

import utils.cmath as cmath
import utils.cfile as cfile

import PIL.Image as PILImage
import PIL.ImageDraw as PILImageDraw


# 数据对象聚类(叶节点是原始数据,枝节点数据为其叶节点的均值)
class cluster_node:
	def __init__(self, vec, id = None, distance = 0.0, left = None, right = None):
		self.id = id
		self.vec = vec
		self.distance = distance
		self.right = right
		self.left = left


######################################################################################## 
# 分级聚类
def hierachical_cluster(rows, similarity = cmath.calculate_pearson_cc_reverse):
	# 数据对间距离值字典(避免重复计算)
	distance_dict = {}
	merge_node_id = -1
	nodes = [cluster_node(rows[i], id = i) for i in range(len(rows))]
	while len(nodes) > 1:
		lowerst_pair = (0, 1)
		# 相似度越大的两个元素距离越近，所以才取相关值 
		nearest_distance = similarity(nodes[0].vec, nodes[1].vec)

		# 遍历每一对节点，找到相关系数最小的  
		nodes_len = len(nodes)
		for i in range(nodes_len):
			for j in range(i + 1, nodes_len):
				id_ij = (nodes[i].id, nodes[j].id)
				if id_ij not in distance_dict:
					distance_dict[id_ij] = similarity(nodes[i].vec, nodes[j].vec)
				distance = distance_dict[id_ij]
				if distance < nearest_distance:
					lowerst_pair = (i, j)
					nearest_distance = distance

		# 利用找到的相关系数最小的数据对，生成新的数据聚类 （取平均值）
		l0, l1 = lowerst_pair[0], lowerst_pair[1]
		merge_vec = [(nodes[l0].vec[i] + nodes[l1].vec[i]) / 2 for i in range(len(nodes[0].vec))]
		new_node = cluster_node(merge_vec, id = merge_node_id, distance = nearest_distance,
			left = nodes[l0], right = nodes[l1])
		del nodes[l1], nodes[l0]
		nodes.append(new_node)
		merge_node_id -= 1

	return nodes[0]

# 计算高度(枝节点的高度就是叶节点之和)
def get_node_height(node):
	if node.left == None and node.right == None: return 1
	return get_node_height(node.left) + get_node_height(node.right)


def get_node_depth(node):
	if node.left == None and node.right == None: return 0
	return max(get_node_depth(node.left), get_node_depth(node.right)) + node.distance


# 打印数据聚类节点，形式是和文件系统层级结构
def print_cluster_nodes(node, labels = None, n = 0):
	if node == None: return
	for i in range(n): print(' ', end ='')
	node_id = node.id
	if node_id < 0:
		print('-')
	else:
		if labels == None:
			print(node_id)
		else:
			print(labels[node_id])
	if node.left != None:
		print_cluster_nodes(node.left, labels = labels, n = n+1)
	if node.right != None:
		print_cluster_nodes(node.right, labels = labels, n = n+1)


######################################################################################## 
# 画出树状图
def draw_dendrogram(node, labels, jpeg = 'cluster_h.jpg'):
	img_width = 1200
	node_depth = get_node_depth(node)
	node_height = get_node_height(node) * 20
	scale = float(img_width - 150) / node_depth
	node_height_half = node_height / 2

	line_file = (255, 0, 0)
	bg_fill = (255, 255, 255)
	img = PILImage.new('RGB', (img_width, node_height), bg_fill)
	draw = PILImageDraw.Draw(img)
	draw.line((0, node_height_half, 10, node_height_half), fill = line_file)
	draw_node(draw, node, 10, node_height_half, scale, labels)
	img.save(jpeg, 'JPEG')


def draw_node(draw, node, x, y, scale, labels):
	line_file = (255, 0, 0)
	text_fill = (0,0,0)
	node_id = node.id
	if node_id < 0:
		left, right = node.left, node.right
		hr = get_node_height(right) * 20	# height_left
		hl = get_node_height(left) * 20		# height_right
		hrh = hr / 2
		hlh = hl /2
		hh = hrh + hlh						# height_half
		top = y - hh
		bottom = y + hh
		ll = node.distance * scale
		draw.line((x, top + hlh, x, bottom - hrh), fill = line_file)
		draw.line((x, top + hlh, x + ll, top + hlh), fill = line_file)
		draw.line((x, bottom - hrh, x + ll, bottom - hrh), fill = line_file)

		draw_node(draw, left, x + ll, top + hlh, scale, labels)
		draw_node(draw, right, x + ll, bottom - hrh, scale, labels)

	else:
		draw.text((x+5, y-7), labels[node_id], text_fill)
