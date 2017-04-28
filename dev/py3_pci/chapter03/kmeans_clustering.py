# -*- coding: utf-8 -*-


import sys
sys.path.append('../../../clibs/')
import utils.cmath as cmath
import utils.cfile as cfile
import random


def kmeans_cluster(rows, similarity = cmath.calculate_pearson_cc_reverse, k = 4, iter_num = 100):
    row0 = rows[0]
    # 收集每一行的最大值和最小值
    ranges = [((min([row[i] for row in rows])), max([row[i] for row in rows])) for i in range(len(row0))]
    # 创建k个随机的聚类点
    nodes = [[random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0] for i in range(len(row0))] for j in range(k)]

    last_matches = None
    best_matches = None
    for itern in range(iter_num):
        print('Iteration %d' % itern)
        best_matches = [[] for i in range(k)]
        # 在每一行中寻找距离最近的中心点
        for i in range(len(rows)):
            row = rows[i]
            best_match = 0
            for j in range(k):
                distance = similarity(nodes[j], row)
                if distance < similarity(nodes[best_match], row):
                    best_match = j
            best_matches[best_match].append(i)
        # 如果迭代的过程中，与上次相同，那么就停止
        print(best_matches == last_matches)
        if best_matches == last_matches:
            break
        last_matches = best_matches

        # 中心点移动到其所有成员的平均位置处
        for i in range(k):
            avgs = [0.0] * len(row0)
            if len(best_matches[i]) > 0:
                for j in best_matches[i]:
                    for m in range(len(rows[j])):
                        avgs[m] += rows[j][m]
                for n in range(len(avgs)):
                    avgs[j] /= len(best_matches[i])
                nodes[i] = avgs

    return best_matches
