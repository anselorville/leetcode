# 题目：  有一个
def solve(n_list):
    n_list.sort()
    left = 0
    right = len(n_list) - 1

    if n_list[0] != 0:
        return 0
    if n_list[-1] != len(n_list):
        return len(n_list)

    while left <= right:
        mid = (left + right) // 2
        val = n_list[mid]
        if val == (mid + 1):
            return mid
        elif val == (mid - 1):
            return mid - 1
        elif val < (mid - 1):
            right = mid - 1
        else:
            left = mid + 1


if __name__ == '__main__':
    test = [3, 0, 1]
    print(solve(test))
