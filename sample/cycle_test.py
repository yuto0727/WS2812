from datetime import datetime
from time import time, sleep
from threading import Thread

debug_prev_time = 0

interval_sec = 0.02


def callable_task():
    global debug_prev_time
    prev = debug_prev_time
    debug_prev_time = time()
    print(interval_sec-round(time()-prev, 5))



def main():
    base_timing = time()

    while True:
        Thread(target=callable_task).start()

        current_timing = time()
        elapsed_sec = (current_timing - base_timing)
        sleep_sec = interval_sec - (elapsed_sec % interval_sec)

        sleep(max(sleep_sec, 0))


if __name__ == '__main__':
    main()
