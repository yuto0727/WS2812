from time import time, sleep

CTRL_PERIOD = 1

def main():
    debug_interval_time = []
    base_time, prev_time, next_time = time(), 0, 0

    print("Main loop start.")
    print(f"Base time: {base_time}")

    for i in range(10):
        debug_interval_time.append([time()-prev_time, next_time])
        prev_time = time()


        next_time = ((base_time - time()) % CTRL_PERIOD) or CTRL_PERIOD
        sleep(next_time)

    for i in range(10):
        print(f"No.{i}: {debug_interval_time[i]}")



if __name__ == "__main__":
    main()