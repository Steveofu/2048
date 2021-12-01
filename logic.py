# 以下为此游戏的逻辑部分 我尽量写下详细注解

import random
import Define as Df


def new_game(n):
    matrix = []
    for i in range(n):
        matrix.append([0] * n)  # 建立一个n*n的矩阵 其实就是建立一个4*4的各自数据列表
    matrix = add_two(matrix)  # 开局在界面上只有两个数字 添加两个数字
    matrix = add_two(matrix)
    return matrix


def add_two(mat):
    a = random.randint(0, len(mat) - 1)  # 比如说我这个游戏是4*4的格子 行和列随机 选两个数字做行和列
    b = random.randint(0, len(mat) - 1)
    while mat[a][b] != 0:  # 当a行b列为空时 把这个数赋值为2  反之 就寻找下一个格子
        a = random.randint(0, len(mat)-1)
        b = random.randint(0, len(mat)-1)
    mat[a][b] = 2
    return mat





def game_state(mat):
    # 检查 是否到 2048
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 2048:
                return 'win'

    for i in range(len(mat)):  # len(mat) 表达的是数组的行 len（mat[0]）表达的是数组的列
        for j in range(len(mat[0])):
            if mat[i][j] == 0:
                return 'not over'

    # 检查本格子右边和下边两个元素 是否相等
    for i in range(len(mat)-1):
        for j in range(len(mat[0]) - 1):
            if mat[i][j] == mat[i+1][j] or mat[i][j+1] == mat[i][j]:
                return 'not over'

    # 因为刚才检查的是右边和下边的格子是否相等 但是最后一行没有下一行的格子但是有右侧 最后一列没有右侧的格子有下侧 所以需要单独处理
    for k in range(len(mat) - 1):
        if mat[len(mat) - 1][k] == mat[len(mat) - 1][k + 1]:
            return 'not over'

    # 同理 应该检查最后一列格子的下侧
    for j in range(len(mat) - 1):
        if mat[j][len(mat)-1] == mat[j + 1][len(mat) - 1]:
            return 'not over'
    return 'lose'


# https://www.cnblogs.com/secondtonone1/p/6907195.html 可以在这看一下
# ***实现矩阵的转置和逆置，这样只要实现一个方向的移动，通过转置和逆置就可以得到其他方向的移动。
# *************

# 矩阵的逆置 把每一行都反过来
def reverse(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0]) - j - 1])
    return new


# 矩阵的转置
def transpose(mat):
    new = []
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new


# 这里我感觉是实现了一个左移的功能 前提是都摆在右边
def cover_up(mat):
    new = []
    for j in range(Df.GRID_LEN):
        partial_new = []
        for i in range(Df.GRID_LEN):
            partial_new.append(0)
        new.append(partial_new)
    done = False
    for i in range(Df.GRID_LEN):
        count = 0
        for j in range(Df.GRID_LEN):
            if mat[i][j] != 0:
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1
    return new, done


# 向左边合并
def merge(mat, done):
    for i in range(Df.GRID_LEN):
        for j in range(Df.GRID_LEN-1):
            if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
                mat[i][j] *= 2
                mat[i][j+1] = 0
                done = True
    return mat, done


def up(game):
    print('up')
    game = transpose(game)  # 矩阵的转置
    game, done = cover_up(game)  # 左移
    game, done = merge(game, done)  # 合并
    game = cover_up(game)[0]
    game = transpose(game)  # 再次转置 还原
    return game, done


def down(game):
    print('down')
    game = reverse(transpose(game))  # 先转置 再逆置
    game, done = cover_up(game)  # 向左移动
    game, done = merge(game, done)  # 向左合并
    game = cover_up(game)[0]
    game = transpose(reverse(game))  # 先逆置再转置
    return game, done


def left(game):
    print("left")
    game, done = cover_up(game)  # 先向左移动
    game, done = merge(game, done)  # 合并
    game = cover_up(game)[0]
    return game, done


def right(game):
    print("right")
    game = reverse(game)  # 先逆置
    game, done = cover_up(game)  # 左移
    game, done = merge(game, done)  # 合并
    game = cover_up(game)[0]
    game = reverse(game)  # 逆置回来
    return game, done
