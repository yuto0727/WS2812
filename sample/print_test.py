import time
i=1
while True:
    print("\r"+"@"*i+" "*(110-i) ,end="")
    i+=1

    if i == 111:
        i = 0

    time.sleep(0.001)