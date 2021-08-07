import logging
import threading
import random
import time
from typing import List
from app.controller import Controller
from app.person import Person

logging.basicConfig(
    format='%(levelname)s: %(message)s', level=logging.INFO)

floor_num = 10 # 总楼层10
lift_num = 4 # 电梯数量
logger = logging.getLogger(__name__)

# 模拟用户请求电梯
def mock_lift_request(id: int, controller: Controller):
    current_floor = random.randint(1, floor_num)
    dest_floor = random.randint(1, floor_num)
    while current_floor == dest_floor:
        # 当如果请求到达楼层和当前所在楼层相同时，重新产生乘客请求
        dest_floor = random.randint(1, floor_num)
    p = Person(id, dest_floor, current_floor)
    selected_lift = controller.dispatch(p)
    selected_lift.add_request_person(p)
    selected_lift.set_target_floor()
    selected_lift.set_direction()

class ControllerThread(threading.Thread):
    def __init__(self, controller: Controller):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.controller = controller

    def stop(self):
        self._stop_event.set()

    def run(self):
        while True:
            if self._stop_event.isSet():
                break
            for l in self.controller.lifts:
                logger.debug(f"{l.id}电梯当前在{l.current_floor}层")
                if l.target_floor is not None:
                    l.run()
            time.sleep(0.5)


if __name__ == '__main__':
    controller = Controller(lift_num, floor_num)
    controller_thread = ControllerThread(controller)
    controller_thread.start()
    for i in range(1, 31):
        time.sleep(1)
        mock_lift_request(i, controller)

    while controller.hasPersonInLift():
        time.sleep(0.5)
    controller_thread.stop()
    for l in controller.lifts:
        if l.total_person_count > 0:
            logging.info(f"{l.id}号电梯成功运载{l.total_person_count}人, 平均周转时间: {round(l.total_time/l.total_person_count, 10)}")