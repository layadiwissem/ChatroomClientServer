# Etudiant : Layadi 

# --------Script pour Tkinter GUI chat client----------
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

    #S'occupe de la reception des messages.
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # client peut avoir quitté le chat
            break

    # S'occupe de l'envoie des messages.
def send(event=None):  # event est passé par bind
    msg = my_msg.get()
    my_msg.set("")  # Effacer input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{q}":
        client_socket.close()
        top.quit()

    # Cette fonction est appellée quand la fenetre est fermée
def on_closing(event=None):
    my_msg.set("{q}")
    send()

top = tkinter.Tk()
top.title("Chatroom multi-clients ")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # Pour le message à envoyer.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame) 
# Pour le container des messages (interface)
msg_list = tkinter.Listbox(messages_frame, height=30, width=90, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()
entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Envoyer", command=send)
send_button.pack()
top.protocol("WM_DELETE_WINDOW", on_closing)

#            -----------Partie sockets----------
HOST = "127.0.0.1" 
PORT = 9001
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Commencer  l'execution du GUI
