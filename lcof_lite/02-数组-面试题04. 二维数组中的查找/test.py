# 题目描述
# 在一个 n * m 的二维数组中，每一行都按照从左到右递增的顺序排序，每一列都按照从上到下递增的顺序排序。请完成一个高效的函数，输入这样的一个二维数组和一个整数，判断数组中是否含有该整数。
# 示例:
# 现有矩阵 matrix 如下：
# [
#   [1,   4,  7, 11, 15],
#   [2,   5,  8, 12, 19],
#   [3,   6,  9, 16, 22],
#   [10, 13, 14, 17, 24],
#   [18, 21, 23, 26, 30]
# ]
# 给定 target = 5，返回 true。
# 给定 target = 20，返回 false。
# 限制：
# 0 <= n <= 1000
# 0 <= m <= 1000


def solve(matrix: list[list[int]], target: int):
    cnt_outer, cnt_inner = 0, 0
    for row in matrix:
        cnt_outer += 1
        if target == row[-1]:
            return True
        elif target < row[-1]:
            left = 0
            right = len(row) - 1
            while left <= right:
                cnt_inner += 1
                mid = (left + right) // 2
                val = row[mid]
                if target == val:
                    return True
                elif target < val:
                    right = mid - 1
                else:
                    left = mid + 1


if __name__ == "__main__":
    matrix = [
        [1, 4, 7, 11, 15],
        [2, 5, 8, 12, 19],
        [3, 6, 9, 16, 22],
        [10, 13, 14, 17, 24],
        [18, 21, 23, 26, 30],
    ]
    target = 16
    print(f"solve({target}) = {solve(matrix, target)}")
