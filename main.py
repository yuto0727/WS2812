from time import time, sleep
from threading import Thread

"""
本番設定値（予定）
サイドテープ 110x2
座席下テープ 20x4
"""

# --- 定数定義 ---
MAIN_CTRL_PERIOD = 0.02

LED_MAX_COUNT = 110 # 必ず偶数にすること
LED_MIN_COUNT = 3

LED_MAX_BRIGHT = 50 # 必ず偶数にすること
LED_MIN_BRIGHT = 5

FADEOUT_RATIO = 1/2
FADE_BRIGHT_STEP = 100 # 明るさの差がステップ数以上の場合にこのステップで減衰

LED_FLOW_COUNT = 15 # 流れるパターンの個数

# --- グローバル変数定義 ---
do_threading = True

bpm = 110

led_status = {}
led_status["colorA"] = 0#RGB 0~255
led_status["colorB"] = 100 #RGB 0~255
led_status["brightness"] = 0 # 0~255
led_status["count"] = 0 # 0~LED_MAX_COUNT


"""led_status["mode"]
LEDの点灯パターンのモード

#0 先頭からレベルメーター
#1 中央からレベルメーター（減衰）
#2 中央からレベルメーター（増幅）
#3 全灯で明るさを変化
#4 全灯で点滅
#5 先頭から流れるパターン
#6 中央から流れるパターン
"""
led_status["mode"] = 0


# --- メイン関数 ---
def main():
    Thread(target=bpm_loop).start()
    Thread(target=control_led).start()
    while True:
        led_status["mode"] = int(input())

# --- 関数定義 ---
"""bpm_loop()
global変数"bpm"の値によって定周期で実行
ビートのタイミングでLED制御変数の変更関数を実行
"""
def bpm_loop():
    base_timing = time()
    while do_threading:
        # BPMから実行周期を算出
        interval_sec = round(60/bpm, 6)

        # スレッド発行
        Thread(target=change_led_status, args=(bpm,)).start()

        # 次実行周期を計算し待機
        current_timing = time()
        elapsed_sec = (current_timing - base_timing)
        sleep_sec = interval_sec - (elapsed_sec % interval_sec)
        sleep(max(sleep_sec, 0))


"""change_led_status()
global変数"led_status"の値を変化する
"""
def change_led_status(bpm):
    global led_status

    # bpmから減衰時間を算出
    # ビート間隔×FADEOUT_RATIOで減衰
    interval_sec = round(60/bpm, 6)
    fade_sec = interval_sec*FADEOUT_RATIO

    # 先頭からレベルメーター
    if led_status["mode"] == 0:
        led_status["brightness"] = LED_MAX_BRIGHT

        fadeout_count = LED_MAX_COUNT-LED_MIN_COUNT
        led_status["count"] = LED_MAX_COUNT
        for i in range(fadeout_count):
            led_status["count"] -= 1  if led_status["count"] > LED_MIN_COUNT else led_status["count"]
            sleep(fade_sec/fadeout_count)

    # 中央からレベルメーター（減衰）
    elif led_status["mode"] == 1:
        led_status["brightness"] = LED_MAX_BRIGHT

        fadeout_count = (LED_MAX_COUNT//2)-LED_MIN_COUNT
        led_status["count"] = LED_MAX_COUNT//2
        for i in range(fadeout_count):
            led_status["count"] -= 1 if led_status["count"] > LED_MIN_COUNT else led_status["count"]
            sleep(fade_sec/fadeout_count)

    # 中央からレベルメーター（増幅）
    elif led_status["mode"] == 2 or led_status["count"] == 6:
        led_status["brightness"] = LED_MAX_BRIGHT

        fadein_count = (LED_MAX_COUNT//2)-LED_MIN_COUNT
        led_status["count"] = LED_MIN_COUNT
        for i in range(fadein_count):
            led_status["count"] += 1 if led_status["count"] < LED_MAX_COUNT//2 else led_status["count"]
            sleep(fade_sec/fadein_count)

    # 全灯で明るさ変化
    elif led_status["mode"] == 3:
        led_status["count"] = LED_MAX_COUNT

        fadeout_count = min(LED_MAX_BRIGHT-LED_MIN_BRIGHT, FADE_BRIGHT_STEP)
        led_status["brightness"] = LED_MAX_BRIGHT

        if fadeout_count == FADE_BRIGHT_STEP:
            fadeout_count = (LED_MAX_BRIGHT-LED_MIN_BRIGHT)//fadeout_count

        for i in range(fadeout_count):
            led_status["brightness"] -= 1 if led_status["brightness"] > LED_MIN_BRIGHT else led_status["brightness"]
            sleep(fade_sec/fadeout_count)

    # 全灯で点滅
    elif led_status["mode"] == 4:
        led_status["count"] = LED_MAX_COUNT

        led_status["brightness"] = LED_MAX_BRIGHT
        sleep(0.05)
        led_status["brightness"] = LED_MIN_BRIGHT

    # 先頭から流れるパターン
    if led_status["mode"] == 5:
        led_status["brightness"] = LED_MAX_BRIGHT

        led_status["count"] = 0
        for i in range(LED_MAX_COUNT):
            led_status["count"] += 1  if led_status["count"] <= LED_MAX_COUNT else led_status["count"]
            sleep(fade_sec/LED_MAX_COUNT)




"""make_led_pattern_list()
global変数"led_status"の値からLEDの点灯パターンのリストを作成
"""
def make_led_pattern_list():
    led_pattern = [[0, 0] for i in range(LED_MAX_COUNT)]
    mode = led_status["mode"]

    if mode == 0:
        for i in range(LED_MAX_COUNT):
            led_pattern[i][0] = LED_MAX_BRIGHT if led_status["count"] >= i else 0

    elif mode == 1 or mode == 2:
        center = LED_MAX_COUNT//2
        start_point = center - led_status["count"]
        end_point = center + led_status["count"] - 1
        for i in range(LED_MAX_COUNT):
            led_pattern[i] = LED_MAX_BRIGHT if start_point <= i <= end_point else 0

    if mode == 3 or mode == 4:
        for i in range(LED_MAX_COUNT):
            led_pattern[i] = led_status["brightness"]

    if mode == 5:
        start_point = led_status["count"] - LED_FLOW_COUNT if led_status["count"] - LED_FLOW_COUNT >= 0 else 0
        end_point = led_status["count"]
        for i in range(LED_MAX_COUNT):
            led_pattern[i] = LED_MAX_BRIGHT if start_point <= i <= end_point else 0

    return led_pattern


"""control_led()
global変数"led_status"の値に基づいてLEDを制御
"""
def control_led():
    while do_threading:
        led_pattern = make_led_pattern_list()
        debug_print(led_pattern)







"""
以下、デバッグ用
"""
def debug_print(led_pattern):
    text = [" ", "▁", "▂", "▃", "▅", "▆", "▇"]

    p = ""

    for i in led_pattern:
        bright = map_range(i, 0, LED_MAX_BRIGHT, 0, 6)
        p += text[bright]

    print("\r"+p+str(led_status["count"])+"  " ,end="")

def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min





if __name__ == "__main__":
    main()

