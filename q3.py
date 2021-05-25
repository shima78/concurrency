from threading import Thread, Semaphore, Lock

from time import sleep

# True hungry
# flase eating
fork = []
N = 5
for j in range(N):
    fork.append(Semaphore(1))
s = []
for j in range(N):
    s.append(Semaphore(0))

room = Semaphore(N-1)
mutex = Lock()


def take_fork(i):
    mutex.acquire()
    # critical
    state[i] = 'Hungry'
    print("philosopher", f"{i} is hungry \n")
    test(i)
    mutex.release()


def test(i):
    if 0 < i < 4:
        if state[i] == 'Hungry' and state[i - 1] != 'Eating' and state[i + 1] != 'Eating':
            state[i] = 'Eating'
            s[i].release()
    elif i == 0:
        if state[0] == 'Hungry' and state[4] != 'Eating' and state[1] != 'Eating':
            state[i] = 'Eating'
            s[i].release()
    elif i == 4:
        if state[4] == 'Hungry' and state[0] != 'Eating' and state[3] != 'Eating':
            state[i] = 'Eating'
            s[i].release()


def drop_fork(i):
    mutex.acquire()
    state[i] = 'Thinking'
    print("philosopher", f"{i} is {state[i]} \n")
    if 0 < i < N-1:
        test(i - 1)
        test(i + 1)
    elif i == 0:
        test(N-1)
        test(1)
    elif i == N-1:
        test(0)
        test(i-1)
    mutex.release()


def philosopher(i):
    while True:
        take_fork(i)
        sleep(0.5)
        print("philosopher", f"{i} is eating \n")
        drop_fork(i)
        #         thinking
        print("philosopher ", f"{i} is thinking \n")
        sleep(0.5)


if __name__ == "__main__":
    philosophers = []
    state = []
    for i in range(N):
        state.append('Thinking')
    for i in range(N):
        philosophers.append(Thread(target=philosopher, args=[i]))

        philosophers[-1].start()

    for thread in philosophers:
        thread.join()
