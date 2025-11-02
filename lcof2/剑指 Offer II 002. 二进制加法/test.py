# 题目描述
# 给定两个 01 字符串 a 和 b ，请计算它们的和，并以二进制字符串的形式输出。

# 输入为 非空 字符串且只包含数字 1 和 0。

# 示例 1:

# 输入: a = "11", b = "10"
# 输出: "101"
# 示例 2:

# 输入: a = "1010", b = "1011"
# 输出: "10101"

# 提示：

# 每个字符串仅由字符 '0' 或 '1' 组成。
# 1 <= a.length, b.length <= 10^4
# 字符串如果不是 "0" ，就都不含前导零。

import random


def solve(a: str, b: str):
    i = len(a) - 1
    j = len(b) - 1
    ans = []
    tc = 0
    while i >= 0 or j >= 0:
        # 求当前进制位上的数字之和 0+0=0 ，1+1=2，这个和divmod(,2)后就是向前进位的数字和当前位的变化
        sc = (int(a[i]) if i >= 0 else 0) + (int(b[j]) if j >= 0 else 0)
        # 此时sc的值有3中：0, 1, 2，初始tc等于0，往后的每一轮循环中tc为sc除2的整数部分，y为余数部分，即tc和y的值只可能是0或者1
        # sc+=tc相当于计算前一位求和的进贡值与当前位的求和值，是历史累加的真实和
        # 此时sc的值最大位max([0,1,2])+max([0,1])=3
        sc += tc
        # 计算当前位的进贡值与余数，tc和y的值只可能是0或者1
        tc, y = divmod(sc, 2)
        # 从低数位开始追加2进制每一位的值，最后只需要翻转即可
        ans.append(str(y))
        # /进入下一轮循环
        i, j = i - 1, j - 1
    if tc > 0:
        ans.append(str(tc))
    ans.reverse()
    # 返回最后的字符串
    return ''.join(ans)


def generate(n: int) -> list:
    """
    生成 n 个符合要求的测试用例

    Args:
        n: 测试用例数量

    Returns:
        list: 包含 n 个 (a, b) 元组的列表，每个元组是一对二进制字符串
    """
    test_cases = []

    def generate_binary_string(length: int) -> str:
        """
        生成指定长度的二进制字符串（无前导零）
        """
        if length == 1:
            # 长度为1时，可以是 "0" 或 "1"
            return random.choice(['0', '1'])
        else:
            # 长度大于1时，第一位必须是 '1'（不能有前导零）
            first_bit = '1'
            # 其余位随机生成
            rest_bits = ''.join(random.choice(['0', '1']) for _ in range(length - 1))
            return first_bit + rest_bits

    for i in range(n):
        # 生成不同长度的测试用例，覆盖边界情况
        if i == 0:
            # 边界情况1: 两个 "0"
            a, b = "0", "0"
        elif i == 1:
            # 边界情况2: 一个 "0"，一个非零
            a, b = "0", "1"
        elif i == 2:
            # 边界情况3: 两个 "1"
            a, b = "1", "1"
        elif i == 3:
            # 边界情况4: 需要多次进位
            a, b = "1111", "1"
        elif i == 4:
            # 边界情况5: 长度差异大
            a, b = "1", "1111111111"
        elif i < n // 2:
            # 前半部分：生成较短的字符串（1-100位）
            len_a = random.randint(1, 100)
            len_b = random.randint(1, 100)
            a = generate_binary_string(len_a)
            b = generate_binary_string(len_b)
        else:
            # 后半部分：生成较长的字符串（100-1000位）
            len_a = random.randint(100, 1000)
            len_b = random.randint(100, 1000)
            a = generate_binary_string(len_a)
            b = generate_binary_string(len_b)

        test_cases.append((a, b))

    return test_cases


def evaluate(a: str, b: str, result: str) -> tuple:
    """
    评估 solve 方法的结果是否正确

    Args:
        a: 第一个二进制字符串
        b: 第二个二进制字符串
        result: solve 方法的输出结果

    Returns:
        tuple: (是否正确, 预期结果)
    """
    # 方法1: 使用 Python 内置的二进制转换
    expected = bin(int(a, 2) + int(b, 2))[2:]  # [2:] 去掉 '0b' 前缀

    # 比较结果
    is_correct = result == expected

    return is_correct, expected


if __name__ == '__main__':
    # 生成测试用例
    num_tests = 100
    test_cases = generate(num_tests)

    # 统计结果
    passed = 0
    failed = 0
    error_examples = []

    for idx, (a, b) in enumerate(test_cases, 1):
        try:
            result = solve(a, b)
            is_correct, expected = evaluate(a, b, result)

            if is_correct:
                passed += 1
            else:
                failed += 1
                if len(error_examples) < 3:
                    error_examples.append(
                        {
                            'idx': idx,
                            'a': a,
                            'b': b,
                            'result': result,
                            'expected': expected,
                        }
                    )
        except Exception as e:
            failed += 1
            if len(error_examples) < 3:
                error_examples.append({'idx': idx, 'a': a, 'b': b, 'error': str(e)})

    # 输出结果
    print(f"\n总测试数: {num_tests}")
    print(f"通过: {passed}")
    print(f"失败: {failed}")
    print(f"通过率: {passed / num_tests * 100:.1f}%")

    if error_examples:
        print("\n错误样例：")
        for err in error_examples:
            print(f"\n  测试 #{err['idx']}:")
            print(f"    a = {err['a'][:50]}{'...' if len(err['a']) > 50 else ''}")
            print(f"    b = {err['b'][:50]}{'...' if len(err['b']) > 50 else ''}")
            if 'error' in err:
                print(f"    错误: {err['error']}")
            else:
                print(
                    f"    得到: {err['result'][:50]}{'...' if len(err['result']) > 50 else ''}"
                )
                print(
                    f"    期望: {err['expected'][:50]}{'...' if len(err['expected']) > 50 else ''}"
                )

    print("\n" + "=" * 70)
    print("测试完成！")
    print("=" * 70)
