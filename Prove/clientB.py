#client che simula uno il client che chiede la verifica del green pass

import socket 

def clientB_program():
    #poiché sia server che client sono sullo stesso pc
    host = socket.gethostname()
    #si assegna alla porta lo stesso numero di quello assegnato al server
    port = 5050

    #inizializzazione
    clientB_socket = socket.socket()
    #connessione al server
    clientB_socket.connect((host, port))
    print("      --------------------")
    print("Connessione al server effettuata.")
    print("      --------------------")

    #per richiedere la verifica delgreen pass
    print("Per terminare la connessione scrivere fine, \naltrimenti scrivere continua.")
    message = input(" -> ")

    if message.lower() != "fine": 
        card_id = input("Inserisci il codice tessera sanitaria: ")
        data = f"{card_id}"
        mess1 = f"{message}"

        #invia i dati al server
        clientB_socket.send(mess1.encode())
        clientB_socket.send(data.encode())

        print("Scegliere prossima azione:")
        message2 = input(" -> ")
        mess2 = f"{message2}"
        clientB_socket.send(mess2.encode())

    if message.lower() == "fine":
        #chiudere la connessione
        clientB_socket.send("fine".encode())
        print("      --------------------")
        print("Chiusura della connessione avviata.")
        clientB_socket.close()


if __name__ == '__main__':
    clientB_program()
