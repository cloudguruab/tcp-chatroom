# imports
import threading
import socket

# host and port config
host = '127.0.0.1'  # localhost
port = 5555

# internet socket for unilateral communication between server and client
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind config to localhost at port ...
server.bind((host, port))

# put server in listening mode for new connections
server.listen()

# when we have a new client we add it to the client list.
# This way we can pull nicknames from the client list.
# so Client x has nickname y.
clients = []
nicknames = []

# broadcast message to all clients in server


def broadcast(msg):
    """[broadcast allows us
    to send messages in the chat server]"""

    for client in clients:
        client.send(msg)


# receive message and interact
# with clients on the server
def handle(client):
    """[handle: allows us to 
    interact inside the chat server]"""

    while True:
        try:
            # receive 1024 bytes which is standard size for a message.
            message = msg = client.recv(1024)
            if message.decode('ascii').startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin': 
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('Command was refused'.encode('ascii'))                    
            elif message.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin': 
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    with open('bans.txt', 'a') as f:
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned by the admin.\n')
                else:
                    client.send('Command was refused'.encode('ascii'))
            else:
                broadcast(msg)
        except:
            # find the client in the clients list.
            index = clients.index(client)
            clients.remove(client)  # remove the client
            client.close()  # close the connection to the client
            nickname = nicknames[index]  # find the nickname of the client
            # remove the nickname associated with the client
            nicknames.remove(nickname)
            # we encode our message with ascii
            broadcast(f'{nickname} left the chat'.encode('ascii'))
            # (standard for information interchange for code)
            break


def receive():
    """[receive open invitations]"""

    while True:
        # accepts clients real time
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        # send key word to joining client
        # keyword will make them put in nickname
        # then we append or save them to our list
        client.send('NICK.'.encode('ascii'))
        
        nickname = client.recv(1024).decode('ascii')

        with open('bans.txt', 'r') as f:
            bans = f.readlines()
        
        if nickname+'\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue
            
        if nickname == 'admin':
            client.send('PWD'.encode('ascii'))
            password = client.recv(1024).decode('asci')

            if password != 'adminpass':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)

        # broadcast to all clients, new client joined.
        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        # allows us to accept multiple join request
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You were kicked by the admin'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked by an admin'.encode('asciii'))

print('Server is listening...')
receive()
