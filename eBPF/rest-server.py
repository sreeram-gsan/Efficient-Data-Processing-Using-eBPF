from flask import Flask, jsonify, request
import sys
import os
import subprocess
import multiprocessing
import signal
import fileinput
  
# creating a Flask app
app = Flask(__name__)
process_id = None
process_obj = None
eBPF_source_code = "eBPF/stringContainsFilter.c"

# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/end', methods = ['GET', 'POST'])
def end():
    if(request.method == 'GET'):
        return jsonify({'data': killProcess()})

@app.route('/start//<filter>', methods = ['GET', 'POST'])
def start(filter):
    if(request.method == 'GET'):
        data = startBPF(filter)
        if(data):
            return jsonify({'data': data})

def startBPF(filter):
    global process_obj
    global process_id

    filedata = ""

    with open(eBPF_source_code, 'r') as file :
        for line in file:
            if ('char pattern[] = "' in line):
                filedata = filedata + 'char pattern[] = "'+ filter +'";' + "\n"
            else:
                filedata = filedata + line

    # Write the file out again
    with open(eBPF_source_code, 'w') as file:
        file.write(filedata)

    try :
        process_obj = multiprocessing.Process(target=targetF ,args=())
        process_obj.start()
        process_id = process_obj.pid
        return "Sucessfully started the eBPF process"
    except:
        return "Failed to start the eBPF process"

def killProcess():
    global process_obj
    global process_id
    if(process_obj):
        os.kill(process_id, signal.SIGINT)
        return "Killed eBPF process"
    else:
        return "No active eBPF process"

def targetF():
    process_id = os.getpid()
    print(process_id)
    try:
        exec(open("eBPF/main.py").read())
    except KeyboardInterrupt:
        print("Exiting Bye Bye")
  
# driver function
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)