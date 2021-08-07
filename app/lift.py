import logging
import time
from typing import List
from .person import Person
from .constant import Direction

class Lift:
    """
    电梯对象
    :param id: int 电梯序号
    :param floor_num: int 总层数
    :param floor: int 电梯所在楼层
    """
    def __init__(self, id: int, floor_num: int,floor: int = 0):
        # 序号
        self.id = id
        self.floor_num = floor_num
        # 当前乘客
        self.carried_persons: List[Person] = []
        # 请求的乘客
        self.request_persons: List[Person] = []
        # 当前楼层
        self.current_floor = floor
        # 目标楼层
        self.target_floor = None
        self.direction = Direction.NONE
        self.total_time = 0 # 运输乘客总耗时(从乘客请求到乘客到达的总时间)
        self.total_person_count = 0 # 运输乘客总数
        self.logger = logging.getLogger(__name__)

    def add_request_person(self, person: Person):
        self.request_persons.append(person)

    def move_one_step(self):
        """
        电梯移动一步
        向上 +1，向下 -1
        """
        self.current_floor = self.current_floor + self.direction.value

    def hasPerson(self) -> bool:
        """
        是否有乘客
        :return bool
        """
        return len(self.carried_persons) > 0 or len(self.request_persons) > 0

    def run(self):
        if self.target_floor == self.current_floor:
            self.arrive()
        else:
            self.move_one_step()

    def arrive(self):
        """
        电梯到达楼层的逻辑处理

        1. 先检查内外部乘客
        2. 修改电梯目标楼层
        3. 判断电梯要不要调整方向
        """
        self.logger.debug(f"{self.id}号电梯达到目标楼层{self.target_floor}")
        # 先检查内外部乘客
        self.handle_person()
        # 修改电梯目标楼层
        self.set_target_floor()
        # 判断电梯要不要调整方向
        self.set_direction()


    def handle_person(self):
        """
        处理内外部乘客
        """
        self.logger.debug(f'{self.id}号电梯内部乘客：{self.carried_persons}')
        for p in self.carried_persons:
            if p.dest_floor == self.current_floor:
                self.logger.debug(f'{p.id}乘客下{self.id}号电梯')
                p.arrive_time = time.time()
                self.total_time = self.total_time + p.arrive_time - p.request_time
                self.total_person_count += 1
                self.carried_persons.remove(p)

        self.logger.debug(f'{self.id}号电梯外部乘客：{self.request_persons}')
        for p in self.request_persons:
            if p.current_floor == self.current_floor:
                if self.direction != Direction.NONE:
                    if p.direction == self.direction or not self.carried_persons:
                        self.logger.debug(f'{p.id}号乘客上{self.id}号电梯')
                        self.request_persons.remove(p)
                        self.carried_persons.append(p)
                else:
                    self.logger.debug(f'{p.id}号乘客上{self.id}号电梯')
                    self.request_persons.remove(p)
                    self.carried_persons.append(p)

    def set_target_floor(self):
        """
        设定目标楼层
        1. 先检查电梯外部请求
        2. 简单电梯内部乘客的请求
        """
        self.logger.debug(f'{self.id}号电梯当前方向:{self.direction}')
        min_request_floor = None # 外部乘客最小的请求楼层
        min_dest_floor = None # 内部乘客最小的目标楼层

        req_distance_list = [] # 请求距离列表
        req_queue_select = [] # 请求队列
        arrive_distance_list = [] # 到达距离列表
        # 检查电梯外部请求
        for p in self.request_persons:
            if p.current_floor == self.current_floor and self.carried_persons:
                continue
            else:
                req_queue_select.append(p.current_floor)
                req_distance_list.append(self.calculate_cost(p.current_floor, p.direction))
            min_request_floor = min(req_distance_list)
        # 检查电梯内部请求
        if self.carried_persons:
            arrive_distance_list = [self.get_distance(p.dest_floor) for p in self.carried_persons]
            min_dest_floor = min(arrive_distance_list)

        # 获取最近
        if min_dest_floor is not None and min_request_floor is not None:
            if min_dest_floor < min_request_floor:
                self.target_floor = self.carried_persons[arrive_distance_list.index(min_dest_floor)].dest_floor
                self.logger.debug(f'{self.id}号电梯目标楼层：{self.target_floor}')
            else:
                self.target_floor = req_queue_select[req_distance_list.index(min_request_floor)]
                self.logger.debug(f'{self.id}号电梯目标楼层：{self.target_floor}')
        elif min_dest_floor is not None:
            self.target_floor = self.carried_persons[arrive_distance_list.index(min_dest_floor)].dest_floor
            self.logger.debug(f'{self.id}号电梯目标楼层：{self.target_floor}')
        elif min_request_floor is not None:
            self.target_floor = req_queue_select[req_distance_list.index(min_request_floor)]
            self.logger.debug(f'{self.id}号电梯目标楼层：{self.target_floor}')


    def get_distance(self, dest_floor: int) -> int:
        """
        计算目标楼层和当前楼层的距离
        :param dest_floor int 目标楼层
        :return int 距离
        """
        if self.direction == Direction.UP:
            if self.current_floor > dest_floor:
                return self.floor_num - self.current_floor + self.floor_num - dest_floor
            return dest_floor - self.current_floor
        elif self.direction == Direction.DOWN:
            if self.current_floor > dest_floor:
                return self.current_floor - dest_floor
            return self.current_floor - 1 + dest_floor - 1
        return abs(self.current_floor - dest_floor)

    def set_direction(self):
        old_direction = self.direction
        if self.target_floor:
            if self.target_floor > self.current_floor:
                self.direction = Direction.UP
            elif self.target_floor < self.current_floor:
                self.direction = Direction.DOWN
        else:
            self.direction = Direction.NONE
        if self.direction != old_direction:
            self.logger.debug(f'{self.id}号电梯方向改变：{self.id}号电梯')

    # 计算调度成本
    def calculate_cost(self, request_floor, direction):
        if self.direction == Direction.UP:
            if self.current_floor > request_floor or direction == Direction.DOWN:
                return self.floor_num - self.current_floor + self.floor_num - request_floor
            return request_floor - self.current_floor
        elif self.direction == Direction.DOWN:
            if self.current_floor < request_floor or direction == Direction.UP:
                return self.current_floor - 1 + request_floor - 1
            return self.current_floor - request_floor
        return abs(self.current_floor - request_floor)

