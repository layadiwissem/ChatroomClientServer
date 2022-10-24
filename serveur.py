# Etudiants : Layadi
# ---------Serveur prend en charge plusieurs clients en même temps----------
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

# Prend en charge le clients entrants
def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s est connecté" % client_address)
        client.send(bytes("Bienvenue dans le chatroom! Tapez votre nom et cliquez Envoyer", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

  # S'occupe d'une seule connexion client
def handle_client(client):  # Prend la socket client en argument
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Bienvenue %s! Si vous voulez quitter, tapez {q} pour sortir.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s a rejoin le chat!" % name
    Discussion(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            Discussion(msg, name + " : ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            Discussion(bytes("%s a quitté le chat." % name, "utf8"))
            break

 # Discussion pour envoyer un message à tous les clients
def Discussion(msg, prefix=""):  # prefix pour identifier le nom
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)

# -------------------------Partie sockets-------------------------
clients = {}
addresses = {}

HOST = ''
PORT = 9001
BUFSIZ = 1024


SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind((HOST , PORT))

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
