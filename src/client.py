import socket

HEADER = 64
PORT = 5050
SERVER = '192.168.46.209' # Change this value for whatever IPV4 you found on your ipconfig/ifconfig
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT) # Encode string into a bytes-like-object
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT) # First msg sent, representing 
    send_length += b' ' * (HEADER - len(send_length))
    
    client.send(send_length)
    client.send(message)

    # In order to read server response msgs
    print(client.recv(2048).decode(FORMAT))

print('*** Welcome to Chat APP. Press Ctrl + C to close your session. ***\n')
username = input('Choose your username: ')

while True:
    try:
        user_msg = input('Message: ')
        send(f'*{username}* says: {user_msg}')
    except KeyboardInterrupt:
        print('Ended session in APP. See you next time.')
        send(f'{DISCONNECT_MESSAGE}ED!. Client {username} has leave the server.')
        break
        