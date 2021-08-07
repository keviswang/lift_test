import logging
from .lift import Lift
from .person import Person


class Controller:
  def __init__(self, num: int, floor_num: int):
    ''' 初始化调度器

    :param num: 电梯数量
    :param floor_num: 楼层数量
    '''
    self.lifts = [Lift(i, floor_num, 1) for i in range(num)]
    self.logger = logging.getLogger(__name__)

  # 判断电梯里面是否还有人,用于demo里面结束调度线程
  def hasPersonInLift(self) -> bool:
    for i in self.lifts:
      if i.hasPerson():
        return True
    return False

  # 找到距离最近(根据方向和楼层)的电梯
  def dispatch(self, person: Person) -> Lift:
    cost_list = [l.calculate_cost(person.dest_floor, person.direction) for l in self.lifts]
    self.logger.debug(f'响应用户{person}请求，调度成本为: {cost_list}')
    selected_lift = self.lifts[cost_list.index(min(cost_list))]
    self.logger.info(f'调度结果：{person.current_floor}楼用户(ID: {person.id})请求使用{selected_lift.id}号电梯(目前在{selected_lift.current_floor},在去{selected_lift.target_floor}路上)到达{person.dest_floor}楼')
    return selected_lift

