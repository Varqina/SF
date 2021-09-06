import threading

def printing(i):
    while True:
        print(f'{i}\n')


for i in range(2):
    t = threading.Thread(target=printing, args=(i,))
    t.start()