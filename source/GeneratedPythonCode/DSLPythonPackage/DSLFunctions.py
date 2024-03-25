import socket

def sendData(receiverDevice, data):
    receiverDevice.messageQueueReceive.put(data)

def receiveData(transmitterDevice = None):
    data = transmitterDevice.messageQueueSend.get()
    return data

def sendTCP(ipAddress, port, role, data):
    if role == "client":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ipAddress, port))
        s.sendall(data)
        s.close()
    if role == "server":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ipAddress, port))
        s.listen(1)
        conn, addr = s.accept()
        conn.sendall(data)
        conn.close()

def receiveTCP(ipAddress, port, role):
    if role == "client":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ipAddress, port))
        data = s.recv(1024)
        s.close()
        return data
    elif role == "server":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ipAddress, port))
        s.listen(1)
        conn, addr = s.accept()
        data = s.recv(1024)
        conn.close()
        return data

def writeFile(filename, data):
    with open(filename, 'a') as savefile:
        savefile.write(str(data))

def readFile(filename):
    with open(filename, 'r') as savefile:
        data = savefile.read()
        return data

def trigger(device):
    device.event()