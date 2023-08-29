#client che simula il centro vaccinale

import socket

def clientA_program():
    #poiché sia server che client sono sullo stesso pc
    host = socket.gethostname()
    #si assegna alla porta lo stesso numero di quello assegnato al server
    port = 5000

    #inizializzazione
    clientA_socket = socket.socket()
    #connessione al server
    clientA_socket.connect((host, port))
    print("      --------------------")
    print("Connessione al server effettuata.")
    print("      --------------------")


    #per inserire dati 
    print("Se si desidera terminare la connessione scrivere fine, \naltrimenti scrivere continua")
    message = input(" -> ")

    if message.lower() != "fine":
        card_id = input("Inserisci il codice tessera sanitaria: ")
        status = input("Inserisci 'valido' per lo stato: ")
    
        data = f"{card_id},{status}"
        mess1 = f"{message}"
    
        #invia i dati al server
        clientA_socket.send(mess1.encode())
        clientA_socket.send(data.encode())
        

        print("Scegliere prossima azione:")
        message2 = input(" -> ")
        mess2 = f"{message2}"
        clientA_socket.send(mess2.encode())


    if message.lower() == "fine":
        #chiudere la connessione
        clientA_socket.send("fine".encode())
        print("      --------------------")
        print("Chiusura della connessione avviata.")
    
    print("      --------------------")
    print("La connessione verrà chiusa.")
    clientA_socket.close()


if __name__ == '__main__':
    clientA_program()