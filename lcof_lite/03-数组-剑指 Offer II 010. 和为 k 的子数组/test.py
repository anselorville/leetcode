# 题目描述
# 给定一个整数数组和一个整数 k ，请找到该数组中和为 k 的连续子数组的个数。

# 示例 1 :
# 输入:nums = [1,1,1], k = 2
# 输出: 2
# 解释: 此题 [1,1] 与 [1,1] 为两种不同的情况

# 示例 2 :
# 输入:nums = [1,2,3], k = 3
# 输出: 2

# 提示:
# 1 <= nums.length <= 2 * 104
# -1000 <= nums[i] <= 1000
# -107 <= k <= 107


def solve_brute_force(n_list: list[int], k: int):
    """暴力解法：时间复杂度 O(n²)，空间复杂度 O(1)"""
    count = 0
    for i in range(len(n_list)):
        sum_val = 0  # 从i开始的累加和
        for j in range(i, len(n_list)):
            sum_val += n_list[j]  # 累加当前元素
            if sum_val == k:
                count += 1
    return count


def solve(n_list: list[int], k: int):
    """
    最优解法：前缀和 + 哈希表
    时间复杂度：O(n)
    空间复杂度：O(n)

    核心思想：
    - preSum[i] 表示 nums[0...i] 的和
    - 子数组 nums[i...j] 的和 = preSum[j] - preSum[i-1]
    - 如果 preSum[j] - preSum[i-1] = k，则 preSum[i-1] = preSum[j] - k
    - 用哈希表记录每个前缀和出现的次数
    """
    count = 0
    pre_sum = 0  # 当前前缀和
    # 哈希表：key为前缀和，value为该前缀和出现的次数
    # 初始化：前缀和为0出现1次（表示空数组，用于处理从索引0开始的子数组）
    prefix_sum_count = {0: 1}

    for num in n_list:
        pre_sum += num  # 计算当前前缀和

        # 查找是否存在前缀和 = pre_sum - k
        # 如果存在，说明有子数组的和为k
        if (pre_sum - k) in prefix_sum_count:
            count += prefix_sum_count[pre_sum - k]

        # 将当前前缀和加入哈希表
        prefix_sum_count[pre_sum] = prefix_sum_count.get(pre_sum, 0) + 1

    return count


if __name__ == '__main__':
    # 测试用例1
    nums1 = [1, 1, 1]
    k1 = 2
    print(f"示例1: nums={nums1}, k={k1}")
    print(f"暴力解法: {solve_brute_force(nums1, k1)}")
    print(f"最优解法: {solve(nums1, k1)}")
    print(f"期望输出: 2\n")

    # 测试用例2
    nums2 = [1, 2, 3]
    k2 = 3
    print(f"示例2: nums={nums2}, k={k2}")
    print(f"暴力解法: {solve_brute_force(nums2, k2)}")
    print(f"最优解法: {solve(nums2, k2)}")
    print(f"期望输出: 2\n")

    # 测试用例3：包含负数
    nums3 = [1, -1, 1, 1, 1]
    k3 = 2
    print(f"示例3: nums={nums3}, k={k3}")
    print(f"暴力解法: {solve_brute_force(nums3, k3)}")
    print(f"最优解法: {solve(nums3, k3)}")

    # 测试用例4：单个元素
    nums4 = [3]
    k4 = 3
    print(f"\n示例4: nums={nums4}, k={k4}")
    print(f"暴力解法: {solve_brute_force(nums4, k4)}")
    print(f"最优解法: {solve(nums4, k4)}")
    print(f"期望输出: 1")
