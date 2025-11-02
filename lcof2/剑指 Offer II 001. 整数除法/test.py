# 题目描述
# 给定两个整数 a 和 b ，求它们的除法的商 a/b ，要求不得使用乘号 '*'、除号 '/' 以及求余符号 '%' 。

# 注意：

# 整数除法的结果应当截去（truncate）其小数部分，例如：truncate(8.345) = 8 以及 truncate(-2.7335) = -2
# 假设我们的环境只能存储 32 位有符号整数，其数值范围是 [−2^31, 2^31−1]。本题中，如果除法结果溢出，则返回 2^31 − 1

from turtle import right


def solve(a: int, b: int):
    # 1. << 表示左移位，乘以2的幂函数，>> 表示右移位
    if b == 1:
        return a
    if a == -(2**31) and b == -1:
        return 2**31 - 1
    sign = (a < 0 and b < 0) or (a > 0 and b > 0)
    a = -a if a > 0 else a
    b = -b if b > 0 else b
    ans = 0
    while a <= b:
        # 每次循环时验证a是否b，然后a尽量一次剪掉最大程度的b的b倍数
        x = b
        cnt = 1
        # 计算小于当前a的最大b的倍数x，同时要注意计算x时因为条件中有x<<1，所以必须满足x>-(2**30),这样x<<1才不会溢出
        while x >= (-(2**30)) and a <= (x << 1):
            x = x << 1
            cnt = cnt << 1
        # 一次性减掉范围内最大的b的番数，相当于用2进制的乘法与b计算去拼装一个a
        a -= x
        ans += cnt
    # 因为是乘除法，最后带上符号即可
    return ans if sign else -ans


if __name__ == "__main__":
    import random

    # a,b = (int(e) for e in input("请输入a,b,用空格隔开：").split(' '))
    # print(f"solve({a} ,{b})={solve(a ,b)}")
    # print(f"a//b = {a//b}")
    right_ans = 0
    wrong_ans = 0
    for _ in range(100):
        a = random.randint(-(2**31), 2**31 - 1)
        b = random.randint(-(2**31), 2**31 - 1)
        if b == 0:
            right_ans += 1
            continue
        ans1 = solve(a, b)
        ans2 = int(a / b)
        if ans1 == ans2:
            right_ans += 1
        else:
            wrong_ans += 1
    print(f"correct_rate:{right_ans}%")
