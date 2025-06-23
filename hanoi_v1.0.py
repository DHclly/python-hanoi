import os
import time

def clear_console():
    """清空控制台内容，根据操作系统类型使用不同命令
       Windows系统使用cls命令，macOS/Linux系统使用clear命令"""
    if os.name == 'nt':  # Windows系统
        os.system('cls')
    else:  # macOS 和 Linux
        os.system('clear')

def fill_zero(num):
    """将数字转换为两位数格式，小于10的数字前补零
    Args:
        num (int): 需要格式化的数字
    Returns:
        str: 两位数字符串
    """
    return f"0{num}" if num < 10 else str(num)

def hanoi(levels, column_from, column_tmp, column_to, move_action):
    """汉诺塔递归算法核心函数
    Args:
        levels (int): 当前要移动的盘子层级
        column_from (str): 起始柱子名称
        column_tmp (str): 临时中转柱子名称
        column_to (str): 目标柱子名称
        move_action (function): 移动操作的回调函数
    """
    if levels == 1:
        move_action(levels, column_from, column_to)
    else:
        hanoi(levels - 1, column_from, column_to, column_tmp, move_action)
        move_action(levels, column_from, column_to)
        hanoi(levels - 1, column_tmp, column_from, column_to, move_action)

def move_disk(level, column_from, column_to):
    """执行具体的盘子移动操作，更新视图并记录步数
    Args:
        level (int): 盘子大小（层级）
        column_from (str): 移动起始柱子
        column_to (str): 移动目标柱子
    """
    global steps
    if auto_move:
        time.sleep(auto_move_wait_time)
    else:
        input("按任意键(如 enter 键)进行下一步")
    clear_console()
    steps += 1
    print(f"第 {steps}/{total_steps} 步：从柱子 {column_from} 移动盘子 [  {fill_zero(level)}   ] 到 {column_to}")
    show_hanoi_view(column_from, column_to)

def show_hanoi_view(column_from, column_to):
    """可视化显示汉诺塔当前状态
    Args:
        column_from (str): 移动起始柱子名称
        column_to (str): 移动目标柱子名称
    """
    global line_from, line_tmp, line_to
    
    lines = {
        line_from_name: line_from,
        line_tmp_name: line_tmp,
        line_to_name: line_to
    }
    
    if column_from is not None and column_to is not None:
        lf = lines[column_from]
        lt = lines[column_to]
        lt.append(lf.pop())
    
    line_from_strs = []
    line_tmp_strs = []
    line_to_strs = []
    
    from_diffs = total_level - len(line_from)
    tmp_diffs = total_level - len(line_tmp)
    to_diffs = total_level - len(line_to)
    if from_diffs > 0:
        line_from_strs.extend(['[     ]'] * from_diffs)
    if tmp_diffs > 0:
        line_tmp_strs.extend(['[     ]'] * tmp_diffs)
    if to_diffs > 0:
        line_to_strs.extend(['[     ]'] * to_diffs)
    
    line_from_disk_strs = [f'[ {fill_zero(i)}  ]' for i in reversed(line_from)]
    line_tmp_disk_strs = [f'[ {fill_zero(i)}  ]' for i in reversed(line_tmp)]
    line_to_disk_strs = [f'[ {fill_zero(i)}  ]' for i in reversed(line_to)]
    
    line_from_strs.extend(line_from_disk_strs)
    line_tmp_strs.extend(line_tmp_disk_strs)
    line_to_strs.extend(line_to_disk_strs)
    
    line_from_strs.extend(['-------', f'[  {line_from_name}  ]'])
    line_tmp_strs.extend(['-------', f'[  {line_tmp_name}  ]'])
    line_to_strs.extend(['-------', f'[  {line_to_name}  ]'])
     
    view = ''
    for i in range(len(line_from_strs)):
        view += f"{line_from_strs[i]}|{line_tmp_strs[i]}|{line_to_strs[i]}\n"
    print(view) 

if __name__ == '__main__': 
    try:
        # 设置汉诺塔的层数，默认为3
        total_level=3
        try:
            total_level_str = input("请输入汉诺塔的层数(默认为3)：")
            total_level = int(total_level_str)
        except Exception:
            pass
        
        # 设置自动移动标志为 False，如果为 False 则程序会等待用户确认每一步
        # 设置自动移动标志为 True，如果为 True 则程序会自动执行每一步，不需要手动确认
        auto_move = True
        auto_move_str = input("是否自动移动？(y/n, 默认y)：")
        if auto_move_str.lower() == 'n':
            auto_move = False

        # 自动移动时每次移动之间的等待时间（秒），仅在auto_move为True时有效
        auto_move_wait_time = 3.0
        if auto_move is True:
            try:
                auto_move_wait_time_str = input("请输入每次移动之间的等待时间(秒，默认为3.0)：")
                auto_move_wait_time = float(auto_move_wait_time_str)
            except Exception:
                pass
        
        # 定义起始柱子的名称为'A'
        line_from_name = 'A'
        # 定义辅助柱子的名称为'B'
        line_tmp_name = 'B'
        # 定义目标柱子的名称为'C'
        line_to_name = 'C'
        # 初始化起始柱子上的盘子列表
        line_from = [i for i in range(total_level,0, -1)]
        # 初始化辅助柱子为空列表
        line_tmp = []
        # 初始化目标柱子为空列表
        line_to = []
        # 初始化步数计数器为0，用于记录已经完成的移动次数
        steps = 0
        # 计算并设置总共需要进行的移动次数，根据汉诺塔问题的解法，共需要(2^total_level - 1)步
        total_steps = 2 ** total_level - 1
        
        clear_console()
        print(f"当前汉诺塔为 {total_level} 层，需要移动 {total_steps} 步, 汉诺塔初始状态：")
        show_hanoi_view(line_from_name,None)
        hanoi(total_level, line_from_name, line_tmp_name, line_to_name, move_disk)
    except KeyboardInterrupt:
        print("\n\n停止汉诺塔运行，拜拜~")