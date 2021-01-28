import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname((socket.gethostname()))
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT' # Close the conn and DC client form server
ACTIVE_CONNECTIONS = f'[ACTIVE CONNECTIONS]: {threading.activeCount() - 1}'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f'[NEW CONNECTION]: {addr} connected.')

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) 

        if msg_length: # 1st time you connect no msg sent, and you will run into an issue, so use if statement here
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(ACTIVE_CONNECTIONS)

            print(f'[{addr}]: {msg}')

            #If we want to sent msg to every client connected to the server
            conn.send('--- Msg received on server ---\n'.encode(FORMAT))

    conn.close()

def start():
    server.listen()
    print(f'[LISTENING]: Server is listening on {SERVER}')
    while True:
        try:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(ACTIVE_CONNECTIONS) # -1 because the starting threading always spawn first for listen conns, but is not an active client-server conn
        except KeyboardInterrupt:
            print('Server stopped by System Administrator.')

print('[STARTING] Server is starting...')

try:
    start()
except ConnectionError as error:
    print(error + '\n' + 'Something went wrong. Try in a moment again.')