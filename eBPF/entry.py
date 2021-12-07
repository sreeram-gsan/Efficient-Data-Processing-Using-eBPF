import sys
import os
import subprocess
import multiprocessing
import signal

process_id = None
process_obj = None

def startBPF():
    global process_obj
    global process_id
    process_obj = multiprocessing.Process(target=targetF ,args=())
    process_obj.start()
    process_id = process_obj.pid

def killProcess():
    global process_obj
    global process_id
    if(process_obj):
        os.kill(process_id, signal.SIGINT)
        print("Killed eBPF container")
    else:
        print("Dummy")
        
def targetF():
    process_id = os.getpid()
    print(process_id)
    try:
        exec(open("main.py").read())
    except KeyboardInterrupt:
        print("Exiting Bye Bye")

if __name__=='__main__':
    for line in sys.stdin:
        if 'q' == line.rstrip():
            break
        if 'k' == line.rstrip():
            killProcess()
        if 's' == line.rstrip():
            startBPF()
        print(f'Input : {line}')
    print("Exit")

        