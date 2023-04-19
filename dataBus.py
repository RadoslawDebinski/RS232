import socket
import threading

# list of actually connected clients
clients = []


def client_communication(client, address):
    # variables to process special data

    clients.append(client)  # adding client to list

    while True:
        try:
            messData = client.recv(1024)
            # Sending other messages
            if messData:
                print(f"[{address}] {messData.decode()}")

                for c in clients:
                    if c != client:
                        c.send(messData)
            else:
                clients.remove(client)
                print(f"[Client {address[0]} : {str(address[1])} disconnected: Not valid data]")
        # Message if user disconnected by X
        except ConnectionResetError:
            clients.remove(client)
            print(f"[Client {address[0]} : {str(address[1])} disconnected by closing window]")
            break


def server_program(serverSideSocket):
    serverSideSocket.listen()

    print('Bus is active...')

    while True:
        client, address = serverSideSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        # Starting client thread
        clientThread = threading.Thread(target=client_communication, args=(client, address))
        clientThread.start()
        print(f"There is {threading.active_count() - 1} active connections now.")


if __name__ == '__main__':
    server_program()
