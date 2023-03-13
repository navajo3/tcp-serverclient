import socket
import time
from requests.exceptions import ConnectionError

activity = 0

def get_constants(prefix):
    return {
        getattr(socket, n): n
        for n in dir(socket)
        if n.startswith(prefix)
    }


families = get_constants('AF_')
types = get_constants('SOCK_')
protocols = get_constants('IPPROTO_')

# TCP/IP socket 
try:
    sock = socket.create_connection(('', 10000)) 
except socket.error:
    print('Server is not responding')
    time.sleep(10)
    exit(1)

print('Family  :', families[sock.family])
print('Type    :', types[sock.type])
print('Protocol:', protocols[sock.proto])
print()

try:

    message = b'This is the message.  It will be repeated.'
    print('sending {!r}'.format(message))
    sock.sendall(message)

    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('received {!r}'.format(data))
        activity = 1

finally:
    if activity == 0:
        print('Server is not responding')
        time.sleep(10)
    elif activity == 1:
        print('closing socket')
        sock.close()
        time.sleep(10)
