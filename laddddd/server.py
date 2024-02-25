import socket
from threading import Thread
import time

SERVER=None
PORT=None
ip_address=(None)

clients={}
playerNames=[]

def handleClient(player_socket,player_name):
    global clients, playerNames

    playerType=clients[player_name]['player_type']
    if(playerType == 'player1'):
        clients[player_name]['turn']=True
        player_socket.send(str({'player_type': clients[player_name]['player_type'],
                                'turn': clients[player_name]['turn']}).encode('utf-8'))
        
    else:
        clients[player_name]['turn']=True
        player_socket.send(str({'player_type': clients[player_name]['player_type'],
                                'turn': clients[player_name]['turn']}).encode('utf-8'))
        
    playerNames.append({"name":player_name,"type":clients[player_name]["player_type"]})
    time.sleep(2)

    if(len(playerNames)>0 and len(playerNames)<=2):
        for cName in clients:
            cSocket=clients[cName]["player_socket"]
            cSocket.send(str({"player_name":playerNames}).encode('utf-8'))

    while True:
        try:
            message=player_socket.recv(4096)
            if message:
                for cName in clients:
                    cSocket=clients[cName]["player_socket"]
                    cSocket.send(message)
        except:
            pass

def acceptConnections():
    global clients,SERVER

    while True:
        # player_socket = client (ip_address and information)
        player_socket,addr=SERVER.accept()
        player_name=player_socket.recv(4096).decode('utf-8')

        if(len(clients.keys())==0):
           clients[player_name]={'player_type':'player_1'}
        else:
            clients[player_name]={'player_type':'player_2'}

        clients[player_name]['player_socket']=player_socket
        clients[player_name]['address']=addr
        clients[player_name]['player_name']=player_name
        clients[player_name]['turn']=False

        print(f"Connection build with {player_name}:{addr}")
        print("clients data:",clients)
        thread= Thread(target=handleClient,args=(player_socket,player_name))
        thread.start()
        
def setup():
    global SERVER,PORT,ip_address
    ip_address='127.0.0.1'
    port=8000
    SERVER= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.bind((ip_address,port))

    SERVER.listen(10)
    print("server is waiting for incoming clients")
    print("\n")
    acceptConnections()

setup()