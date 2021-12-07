import queue_reader as qr

'''
processor.py

Spawns a thread to listen to the queue - toProcessor; thread on queue_reader
Injects eBPF code snippets based on the filter
'''
if __name__ == "__main__":
    qr.main()
    print("queue reader running...")
    