

import os


def read_file(file_name, title_row = 0, key_col = 0, split_tag = '\t'):
	lines = [line for line in open(file_name).readlines()]
	# 第一行是列标题，也就是被统计的单词是哪些 
	p_title = lines[title_row].strip()
	titles = p_title.split(split_tag)
	col_names = titles[key_col+1:]
	row_names = []
	data = []
	# 第二列开始才是对不同的单词的计数
	p_datas = lines[title_row+1:]
	for line in p_datas:
		p = line.strip().split(split_tag)
		# 每行的第一列都是行名
		row_names.append(p[key_col])
		# data是一个列表，这个列表里每一个元素都是一个列
		data.append([float(x) for x in p[1:]])
	return row_names, col_names, data
