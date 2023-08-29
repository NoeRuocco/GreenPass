#client che simula il client che manda variazioni del green pass al server di controllo

import socket 

def clientB2_program():
    #poiché sia server che client sono sullo stesso pc
    host = socket.gethostname()
    #si assegna alla porta lo stesso numero di quello assegnato al server
    port = 5050

    #inizializzazione
    clientB2_socket = socket.socket()
    #connessione al server
    clientB2_socket.connect((host, port))

    #per prendere l'input
    message = input(" (Se si desidera terminare la connessione scrivere fine) -> ")

    if message.lower().strip() != 'fine': 
        #invia il messaggio 
        clientB2_socket.send(message.encode())
        #riceve la risposta
        data = clientB2_socket.recv(1024).decode()

        #per mostrarlo nel terminale
        print("Da parte del server: " + data)

        #per prendere di nuovo l'input
        message = input(" -> ")

    #chiudere la connessione
    clientB2_socket.close()


if __name__ == '__main__':
    clientB2_program()
