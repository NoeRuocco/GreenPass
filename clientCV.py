# client che rappresenta il centro vaccinale, che invierà al server vaccinale (serverV)
# le informazioni relative a tessera sanitaria, tempo di validità del green pass e 
# stato del green pass delle persone vaccinate 

import socket
import re

def clientCV_program():
    # poiché sia server che client sono sullo stesso pc
    host = socket.gethostname()
    # si assegna alla porta lo stesso numero di quello assegnato al serverV 
    port = 5000

    # inizializzazione della socket clientCV
    clientCV_socket = socket.socket()
    # connessione al serverV
    clientCV_socket.connect((host, port))
    print("      --------------------")
    print("Connessione al server effettuata.")
    print("      --------------------")

    # per poter effettuare operazioni 
    print("Se si desidera terminare la connessione scrivere fine,\naltrimenti scrivere continua")
    message = input(" -> ")

    # se il messaggio iniziale è "continua", verrà richiesto l'inserimento
    # dei dati del green pass
    if message.lower() == "continua":
        tessera_sanitaria = input("Inserisci il codice tessera sanitaria: ")
        tempo_val = input("Inserisci il tempo di validità del green pass: ")
        stato = input("Inserisci lo stato: ")
        
        # controllo iniziale sul formato della tessera sanitaria (ultime 8 cifre)
        if verify_code(tessera_sanitaria):
            # controllo poiché l'unico stato ammissibile post vaccinazione è "valido"
            if stato.lower() == "valido":
                #inviare i dati inseriti al serverV
                data = f"{tessera_sanitaria},{tempo_val},{stato}"
                mess1 = f"{message}"
                clientCV_socket.send(mess1.encode())
                clientCV_socket.send(data.encode())
            else: 
                print("Non è stato inserito uno stato valido. \n")
        else: 
            print("Il formato inserito non è corretto. Inserire gli ultimi 8 numeri della tessera. \n")
        
        
        # per scegliere come proseguire 
        print("      --------------------")
        print("Scegliere prossima azione:")
        message2 = input(" -> ")
        mess2 = f"{message2}"
        clientCV_socket.send(mess2.encode())

    # se il messaggio iniziale è "fine", la connessione viene subito chiusa
    if message.lower() == "fine":
        #chiudere la connessione
        clientCV_socket.send("fine".encode())
        print("      --------------------")
        print("Chiusura della connessione avviata.")

    # ulteriore controllo sul messaggio iniziale
    if message.lower() != "continua" and message.lower() != "fine":
        print("Non è stato inserito un messaggio ammissibile per compiere operazioni.\n")
    

    # per chiudere la connessione col serverV alla fine delle operazioni
    print("      --------------------")
    print("La connessione verrà chiusa.")
    clientCV_socket.close()


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
    clientCV_program()