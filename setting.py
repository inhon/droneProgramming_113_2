import numpy as np
BASE_HEIGHT=25.0
ROVER_HEIGHT=15.0
ACCEPTED_DELAY = 1 #可接受的通訊延遲 sec
BASE_SPEED=600  #base 在guided mode 下的移動速度cm/sec
ROVER_SPEED_LIMIT=8  #m/sec
SEND_INTERVAL = 0.5# base 發送座標間隔 sec
SLEEP_LENGTH = 0.5 # rover接收座標並進行飛行控制間隔
FORMATION=0 #設定隊形
SPEED_THRESHOLD=2 # 判定base 是否靜止
KP=1
KD=-0.1
K1 = np.array([[0.5, 0], [0, 0.5]])  # Acts on the position error (Proportional Gain)
damping = 0.05  # Damping factor to control high frequency velocity changes (overshoot and oscillations)
max_velocity=10
"""
隊形(formation)包括:
    0. Line: 1台rover 跟在 base 飛行方向的後方
    1. Wedge: 倒 V 型，base 帶領2台rover, 
    2. Square: base在中間，4台rover在方形的四個角上
"""