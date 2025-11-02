#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重命名题目文件夹，添加分类顺序和名称前缀
按照从基础到高级的学习顺序排列
"""
import os
import shutil

# 当前脚本所在目录
base_path = os.path.dirname(os.path.abspath(__file__))

# 定义题目的分类和顺序
# 格式：(序号, 分类名称, 原文件夹名)
problems_order = [
    # 一、数组与哈希（3题）- 基础数据结构
    ("01", "数组", "面试题03. 数组中重复的数字"),
    ("02", "数组", "面试题04. 二维数组中的查找"),
    ("03", "数组", "剑指 Offer II 010. 和为 k 的子数组"),
    # 二、链表（4题）- 指针操作基础
    ("04", "链表", "面试题06. 从尾到头打印链表"),
    ("05", "链表", "面试题22. 链表中倒数第k个节点"),
    ("06", "链表", "面试题24. 反转链表"),
    ("07", "链表", "剑指 Offer II 022. 链表中环的入口节点"),
    # 三、二叉树（1题）- 树结构
    ("08", "树", "面试题07. 重建二叉树"),
    # 四、栈与队列（2题）- 特殊数据结构
    ("09", "栈", "面试题09. 用两个栈实现队列"),
    ("10", "栈", "面试题30. 包含min函数的栈"),
    # 五、动态规划（4题）- 核心算法思想
    ("11", "DP", "面试题10- I. 斐波那契数列"),
    ("12", "DP", "面试题42. 连续子数组的最大和"),
    ("13", "DP", "剑指 Offer II 088. 爬楼梯的最少成本"),
    ("14", "DP", "剑指 Offer II 095. 最长公共子序列"),
    # 六、搜索算法（1题）- DFS/BFS
    ("15", "搜索", "面试题12. 矩阵中的路径"),
    # 七、双指针/滑动窗口（2题）- 常用技巧
    ("16", "双指针", "面试题48. 最长不含重复字符的子字符串"),
    ("17", "双指针", "剑指 Offer II 016. 不含重复字符的最长子字符串"),
    # 八、二分查找（1题）- 高效搜索
    ("18", "二分", "面试题11. 旋转数组的最小数字"),
    # 九、位运算（1题）- 底层操作
    ("19", "位运算", "面试题15. 二进制中1的个数"),
    # 十、回溯算法（1题）- 暴力搜索优化
    ("20", "回溯", "剑指 Offer II 079. 所有子集"),
]


def rename_folders(dry_run=True):
    """
    重命名文件夹

    Args:
        dry_run: 如果为True，只显示将要执行的操作，不实际重命名
    """
    print("=" * 80)
    print("题目文件夹重命名工具")
    print("=" * 80)
    print(f"\n工作目录: {base_path}\n")

    if dry_run:
        print("[!] 当前为预览模式，不会实际重命名文件夹")
        print("如需执行重命名，请将 dry_run 参数设置为 False\n")
    else:
        print("[*] 开始执行重命名操作...\n")

    renamed_count = 0
    not_found = []

    for num, category, old_name in problems_order:
        old_path = os.path.join(base_path, old_name)
        new_name = f"{num}-{category}-{old_name}"
        new_path = os.path.join(base_path, new_name)

        # 检查文件夹是否存在
        if not os.path.exists(old_path):
            not_found.append(old_name)
            print(f"[X] [{num}] 未找到: {old_name}")
            continue

        # 检查新名称是否已存在
        if os.path.exists(new_path):
            print(f"[>] [{num}] 已存在: {new_name}")
            continue

        # 显示操作
        print(f"{'[预览]' if dry_run else '[执行]'} {num}. {category}")
        print(f"   旧: {old_name}")
        print(f"   新: {new_name}")

        # 执行重命名
        if not dry_run:
            try:
                os.rename(old_path, new_path)
                print(f"   [OK] 重命名成功")
                renamed_count += 1
            except Exception as e:
                print(f"   [ERROR] 重命名失败: {e}")
        else:
            renamed_count += 1

        print()

    # 显示统计信息
    print("=" * 80)
    print("统计信息")
    print("=" * 80)
    print(f"预计{'处理' if dry_run else '已处理'}: {renamed_count}/{len(problems_order)} 个文件夹")

    if not_found:
        print(f"\n未找到的文件夹 ({len(not_found)}):")
        for name in not_found:
            print(f"  - {name}")

    if dry_run:
        print("\n[OK] 预览完成！如需执行重命名，请运行:")
        print("   rename_folders(dry_run=False)")
    else:
        print(f"\n[OK] 重命名完成！成功处理 {renamed_count} 个文件夹")


def restore_folders(dry_run=True):
    """
    恢复文件夹原始名称（去掉前缀）

    Args:
        dry_run: 如果为True，只显示将要执行的操作，不实际重命名
    """
    print("=" * 80)
    print("恢复文件夹原始名称")
    print("=" * 80)
    print(f"\n工作目录: {base_path}\n")

    if dry_run:
        print("[!] 当前为预览模式，不会实际重命名文件夹")
        print("如需执行恢复，请将 dry_run 参数设置为 False\n")
    else:
        print("[*] 开始执行恢复操作...\n")

    restored_count = 0

    for num, category, original_name in problems_order:
        prefixed_name = f"{num}-{category}-{original_name}"
        old_path = os.path.join(base_path, prefixed_name)
        new_path = os.path.join(base_path, original_name)

        # 检查带前缀的文件夹是否存在
        if not os.path.exists(old_path):
            continue

        # 检查原始名称是否已存在
        if os.path.exists(new_path):
            print(f"[>] 原始名称已存在: {original_name}")
            continue

        # 显示操作
        print(f"{'[预览]' if dry_run else '[执行]'} {num}. 恢复")
        print(f"   旧: {prefixed_name}")
        print(f"   新: {original_name}")

        # 执行重命名
        if not dry_run:
            try:
                os.rename(old_path, new_path)
                print(f"   [OK] 恢复成功")
                restored_count += 1
            except Exception as e:
                print(f"   [ERROR] 恢复失败: {e}")
        else:
            restored_count += 1

        print()

    # 显示统计信息
    print("=" * 80)
    print("统计信息")
    print("=" * 80)
    print(f"预计{'恢复' if dry_run else '已恢复'}: {restored_count} 个文件夹")

    if dry_run and restored_count > 0:
        print("\n[OK] 预览完成！如需执行恢复，请运行:")
        print("   restore_folders(dry_run=False)")
    elif not dry_run:
        print(f"\n[OK] 恢复完成！成功处理 {restored_count} 个文件夹")
    else:
        print("\n没有需要恢复的文件夹")


def show_order():
    """显示题目的学习顺序"""
    print("=" * 80)
    print("题目学习顺序")
    print("=" * 80)
    print()

    current_category = None
    category_map = {
        "数组": "一、数组与哈希",
        "链表": "二、链表",
        "树": "三、二叉树",
        "栈": "四、栈与队列",
        "DP": "五、动态规划",
        "搜索": "六、搜索算法",
        "双指针": "七、双指针/滑动窗口",
        "二分": "八、二分查找",
        "位运算": "九、位运算",
        "回溯": "十、回溯算法",
    }

    for num, category, name in problems_order:
        if category != current_category:
            if current_category is not None:
                print()
            print(f"\n{category_map[category]}")
            print("-" * 80)
            current_category = category

        print(f"{num}. {name}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    import sys

    # 显示使用帮助
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "show":
            # 显示题目顺序
            show_order()

        elif command == "preview":
            # 预览重命名（默认）
            rename_folders(dry_run=True)

        elif command == "rename":
            # 执行重命名
            confirm = input("\n[!] 确认要重命名所有文件夹吗？(输入 yes 确认): ")
            if confirm.lower() == "yes":
                rename_folders(dry_run=False)
            else:
                print("[X] 操作已取消")

        elif command == "restore":
            # 执行恢复
            confirm = input("\n[!] 确认要恢复所有文件夹的原始名称吗？(输入 yes 确认): ")
            if confirm.lower() == "yes":
                restore_folders(dry_run=False)
            else:
                print("[X] 操作已取消")

        elif command == "help" or command == "-h" or command == "--help":
            print("\n使用方法:")
            print("  python rename_folders.py show     - 显示题目学习顺序")
            print("  python rename_folders.py preview  - 预览重命名操作（不实际执行）")
            print("  python rename_folders.py rename   - 执行重命名操作")
            print("  python rename_folders.py restore  - 恢复文件夹原始名称")
            print("  python rename_folders.py help     - 显示此帮助信息")
            print()

        else:
            print(f"[X] 未知命令: {command}")
            print("运行 'python rename_folders.py help' 查看帮助")

    else:
        # 默认：显示顺序 + 预览重命名
        show_order()
        print("\n")
        rename_folders(dry_run=True)

        print("\n" + "=" * 80)
        print("使用说明")
        print("=" * 80)
        print("\n运行以下命令:")
        print("  python rename_folders.py show     - 显示题目学习顺序")
        print("  python rename_folders.py preview  - 预览重命名操作")
        print("  python rename_folders.py rename   - 执行重命名操作")
        print("  python rename_folders.py restore  - 恢复原始名称")
        print("  python rename_folders.py help     - 显示帮助")
        print()
