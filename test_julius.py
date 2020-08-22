import time

from JuliusManager import JuliusManager

julius = JuliusManager("localhost", 10500)
julius.wake_words = {"水ください": 1}

while True:
    for spoken_id in julius.update():
        print(f"ID:{spoken_id} was spoken")
        if spoken_id == 1:
            print("call some function")
    time.sleep(1)
