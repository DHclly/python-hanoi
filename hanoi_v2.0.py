import os
import time

class HanoiTower:
    """汉诺塔游戏类"""
    def __init__(self):
        # 设置汉诺塔的层数，默认为3
        self.total_level = 3
        # 设置自动移动标志为 False，如果为 False 则程序会等待用户确认每一步
        # 设置自动移动标志为 True，如果为 True 则程序会自动执行每一步，不需要手动确认
        self.auto_move = True
        # 自动移动时每次移动之间的等待时间（秒），仅在auto_move为True时有效
        self.auto_move_wait_time = 3.0
        # 定义起始柱子的名称为'A'
        self.line_from_name = 'A'
        # 定义辅助柱子的名称为'B'
        self.line_tmp_name = 'B'
        # 定义目标柱子的名称为'C'
        self.line_to_name = 'C'
        # 初始化起始柱子上的盘子列表
        self.line_from = []
        # 初始化辅助柱子为空列表
        self.line_tmp = []
        # 初始化目标柱子为空列表
        self.line_to = []
        # 初始化步数计数器为0，用于记录已经完成的移动次数
        self.steps = 0
        # 计算并设置总共需要进行的移动次数，根据汉诺塔问题的解法，共需要(2^total_level - 1)步
        self.total_steps = 0

    def clear_console(self):
        """清空控制台内容，根据操作系统类型使用不同命令
        Windows系统使用cls命令，macOS/Linux系统使用clear命令"""
        if os.name == 'nt':  # Windows系统
            os.system('cls')
        else:  # macOS 和 Linux
            os.system('clear')

    def fill_zero(self,num):
        """将数字转换为两位数格式，小于10的数字前补零
        Args:
            num (int): 需要格式化的数字
        Returns:
            str: 两位数字符串
        """
        return f"0{num}" if num < 10 else str(num)

    def hanoi(self,level, column_from, column_tmp, column_to):
        """汉诺塔递归算法核心函数
        Args:
            levels (int): 当前要移动的盘子层级
            column_from (str): 起始柱子名称
            column_tmp (str): 临时中转柱子名称
            column_to (str): 目标柱子名称
        """
        if level == 1:
            self.move_disk(level, column_from, column_to)
        else:
            self.hanoi(level - 1, column_from, column_to, column_tmp)
            self.move_disk(level, column_from, column_to)
            self.hanoi(level - 1, column_tmp, column_from, column_to)

    def move_disk(self,level, column_from, column_to):
        """执行具体的盘子移动操作，更新视图并记录步数
        Args:
            level (int): 盘子大小（层级）
            column_from (str): 移动起始柱子
            column_to (str): 移动目标柱子
        """
        if self.auto_move:
            time.sleep(self.auto_move_wait_time)
        else:
            input("按任意键(如 enter 键)进行下一步")
        self.clear_console()
        self.steps += 1
        print(f"第 {self.steps}/{self.total_steps} 步：从柱子 {column_from} 移动盘子 [  {self.fill_zero(level)}   ] 到 {column_to}")
        self.show_hanoi_view(column_from, column_to)

    def show_hanoi_view(self,column_from, column_to):
        """可视化显示汉诺塔当前状态
        Args:
            column_from (str): 移动起始柱子名称
            column_to (str): 移动目标柱子名称
        """
        lines = {
            self.line_from_name: self.line_from,
            self.line_tmp_name: self.line_tmp,
            self.line_to_name: self.line_to
        }
        
        if column_from is not None and column_to is not None:
            lf = lines[column_from]
            lt = lines[column_to]
            lt.append(lf.pop())
        
        line_from_strs = []
        line_tmp_strs = []
        line_to_strs = []
        
        from_diffs = self.total_level - len(self.line_from)
        tmp_diffs = self.total_level - len(self.line_tmp)
        to_diffs = self.total_level - len(self.line_to)
        if from_diffs > 0:
            line_from_strs.extend(['[     ]'] * from_diffs)
        if tmp_diffs > 0:
            line_tmp_strs.extend(['[     ]'] * tmp_diffs)
        if to_diffs > 0:
            line_to_strs.extend(['[     ]'] * to_diffs)
        
        line_from_disk_strs = [f'[ {self.fill_zero(i)}  ]' for i in reversed(self.line_from)]
        line_tmp_disk_strs = [f'[ {self.fill_zero(i)}  ]' for i in reversed(self.line_tmp)]
        line_to_disk_strs = [f'[ {self.fill_zero(i)}  ]' for i in reversed(self.line_to)]
        
        line_from_strs.extend(line_from_disk_strs)
        line_tmp_strs.extend(line_tmp_disk_strs)
        line_to_strs.extend(line_to_disk_strs)
        
        line_from_strs.extend(['-------', f'[  {self.line_from_name}  ]'])
        line_tmp_strs.extend(['-------', f'[  {self.line_tmp_name}  ]'])
        line_to_strs.extend(['-------', f'[  {self.line_to_name}  ]'])
        
        view = ''
        for i in range(len(line_from_strs)):
            view += f"{line_from_strs[i]}|{line_tmp_strs[i]}|{line_to_strs[i]}\n"
        print(view) 
        
    def start(self):
        """开始游戏"""
        try:
            try:
                total_level_str = input("请输入汉诺塔的层数(默认为3)：")
                self.total_level = int(total_level_str)
            except Exception:
                pass
            
            auto_move_str = input("是否自动移动？(y/n, 默认y)：")
            if auto_move_str.lower() == 'n':
                self.auto_move = False

            if self.auto_move is True:
                try:
                    auto_move_wait_time_str = input("请输入每次移动之间的等待时间(秒，默认为3.0)：")
                    self.auto_move_wait_time = float(auto_move_wait_time_str)
                except Exception:
                    pass

            self.clear_console()
            self.line_from = [i for i in range(self.total_level,0, -1)]
            self.total_steps = 2 ** self.total_level - 1
            print(f"当前汉诺塔为 {self.total_level} 层，需要移动 {self.total_steps} 步, 汉诺塔初始状态：")
            self.show_hanoi_view(self.line_from_name,None)
            self.hanoi(self.total_level, self.line_from_name, self.line_tmp_name, self.line_to_name)
        except KeyboardInterrupt:
            print("\n\n停止汉诺塔运行，拜拜~")

if __name__ == '__main__': 
    game = HanoiTower()
    game.start()
    