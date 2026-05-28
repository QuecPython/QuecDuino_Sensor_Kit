from machine import Pin
import utime

# 引脚定义（根据实际接线修改）
TRIG_PIN = Pin.GPIO30  # 触发脚
ECHO_PIN = Pin.GPIO31  # 回声脚

TRIG = Pin(TRIG_PIN, Pin.OUT, Pin.PULL_DISABLE, 0)
ECHO = Pin(ECHO_PIN, Pin.IN, Pin.PULL_DISABLE, 0)

# 简单滑动滤波，取多次测量的平均值
dist_list = []
FILTER_SIZE = 5  # 滤波窗口大小

def rcwl_9610a_get_dist():
    TRIG.off()
    utime.sleep_us(2)
    TRIG.on()
    utime.sleep_us(10)
    TRIG.off()

    # 优化超时时间，避免误判
    t_out = 0
    while ECHO.value() == 0 and t_out < 30000:
        t_out += 1
    if t_out >= 30000:
        return None

    start = utime.ticks_us()

    t_out = 0
    while ECHO.value() == 1 and t_out < 500000:  # 最大量程8m，对应约480000us
        t_out += 1
    if t_out >= 500000:
        return None

    end = utime.ticks_us()
    dura = end - start
    dist = dura / 58.0
    return round(dist, 2)

while True:
    raw_dist = rcwl_9610a_get_dist()
    
    if raw_dist is not None and 2 <= raw_dist <= 800:
        # 滑动滤波
        dist_list.append(raw_dist)
        if len(dist_list) > FILTER_SIZE:
            dist_list.pop(0)
        avg_dist = round(sum(dist_list) / len(dist_list), 2)
        print("当前距离：", avg_dist, "cm")
    else:
        print("超出范围或信号异常")

    utime.sleep(0.2)





