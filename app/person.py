import logging
import time
from .constant import Direction

# 电梯乘客
class Person:
    def __init__(self, id: int, dest_floor: int, current_floor: int):
        self.logger = logging.getLogger(__name__)
        # 序号
        self.id = id
        # 要去的楼层
        self.dest_floor = dest_floor
        # 目前所在楼层
        self.current_floor = current_floor
        # 请求时间
        self.request_time = time.time()
        # 到达时间
        self.arrive_time = None
        self.direction = Direction.UP if self.current_floor < self.dest_floor else Direction.DOWN

    def __repr__(self) -> str:
        return f'[{self.id}号用户当前在{self.current_floor}层,要去{self.dest_floor}层]'

