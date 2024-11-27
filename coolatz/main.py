from multiprocessing import Queue, Process
from threading import Thread


def collatz_sequence(n):
    if n == 1:  # Caso base
        return [1]
    elif n % 2 == 0:
        return [n] + collatz_sequence(n // 2)
    else:
        return [n] + collatz_sequence(3 * n + 1)


def partcount(start, end, queue_obj):
    for i in range(start, end):
        sequence = collatz_sequence(i)
        queue_obj.put((i, sequence))


if __name__ == '__main__':
    n = Queue()
    # t1 = Process(target=partcount, args=(1, 2500, n))
    # t2 = Process(target=partcount, args=(2500, 5000, n))
    # t3 = Process(target=partcount, args=(5000, 7500, n))
    # t4 = Process(target=partcount, args=(7500, 10000, n))
    t1 = Thread(target=partcount, args=(1, 2500, n))
    t2 = Thread(target=partcount, args=(2500, 5000, n))
    t3 = Thread(target=partcount, args=(5000, 7500, n))
    t4 = Thread(target=partcount, args=(7500, 10000, n))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()

    while not n.empty():
        num, sequence = n.get()
        print(f"Numero: {num}, Sequenza di Collatz: {sequence[:10]}...")
