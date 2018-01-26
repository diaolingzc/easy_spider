# coding:utf-8

import time
import os
import sched

# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
schedule = sched.scheduler(time.time, time.sleep)


def execute_command(cmd, inc):
    print('cmd', cmd)
    schedule.enter(inc, 0, execute_command, (cmd + 1, inc))


def main(cmd, inc=60):
    schedule.enter(0, 0, execute_command, (cmd, inc))
    schedule.run()

if __name__ == '__main__':
    main(0, 0.0001)
