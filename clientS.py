#client che rappresenta una qualsiasi persona che vuole verificare la validità di un green pass
#come ad esempio un negoziante, e invierà la richiesta al server di controllo serverC

import socket 
import re

def clientS_program():
    #poiché sia server che client sono sullo stesso pc
    host = socket.gethostname()
    #si assegna alla porta lo stesso numero di quello assegnato al serverC
    port = 5050

    #inizializzazione
    clientS_socket = socket.socket()
    #connessione al serverC
    clientS_socket.connect((host, port))
    #per poter specificare al server il tipo di client che si sta connettendo
    client = "clients"
    clientS_socket.send(client.encode())
    print("      --------------------")
    print("Connessione al server effettuata.")
    print("      --------------------")

    #per poter effettuare operazioni
    print("Per terminare la connessione scrivere fine, \naltrimenti scrivere continua.")
    message = input(" -> ")

    #se il primo messaggio inserito è "continua" si prosegue con la richiesta di validità
    if message.lower() == "continua": 
        tessera_sanitaria = input("Inserisci il codice tessera sanitaria: ")
        # controllo sul corretto inserimento del codice della tessera sanitaria (ultime 8 cifre)
        if verify_code(tessera_sanitaria):
            # per poter inviare i dati al serverC
            data = f"{tessera_sanitaria}"
            mess1 = f"{message}"

            clientS_socket.send(mess1.encode())
            clientS_socket.send(data.encode())

            # per ottenere risposta dal serverC
            print("      --------------------")
            server_response = clientS_socket.recv(1024).decode()
            print("Risposta a seguito del controllo:", server_response)

            # per scegliere come proseguire 
            print("      --------------------")
            print("Scegliere prossima azione:")
            message2 = input(" -> ")
            mess2 = f"{message2}"
            clientS_socket.send(mess2.encode())
        else: 
            print("Il formato inserito per la tessera sanitaria non è corretto. Inserire le utlime 8 cifre del codice. \n")

    # se il messaggio iniziale è "fine" la connessione al serverC verrà chiusa 
    if message.lower() == "fine":
        #chiudere la connessione
        clientS_socket.send("fine".encode())
        print("      --------------------")
        print("Chiusura della connessione avviata.")
        clientS_socket.close()

    # ulteriore controllo sul messaggio iniziale
    if message.lower() != "continua" and message.lower() != "fine":
        print("Non è stato inserito un messaggio ammissibile per compiere operazioni.\n")
        

    # per chiudere la connessione col serverC alla fine delle operazioni
    print("      --------------------")
    print("Chiusura della connessione avviata.")
    clientS_socket.close()


# funzione per verificare il corretto formato della tessera sanitaria 
def verify_code(tessera_sanitaria): 
    # definizione del pattern regex per una tessera sanitaria 
    # (contando le ultime 8 cifre)
    pattern = r'^\d{8}$'
    
    # si effettua la verifica usando il pattern regex
    if re.match(pattern, tessera_sanitaria):
        return True
    else:
        return False


# per specificare il metodo di esecuzione
if __name__ == '__main__':
    clientS_program()