# client che rappresenta un ente (es. ASL) che comunica le variazioni relative 
# ad un green pass al server di controllo serverC

import socket
import re

def clientT_program():
    #poiché sia server che client sono sullo stesso pc
    host = socket.gethostname()
    #si assegna alla porta lo stesso numero di quello assegnato al server
    port = 5050

    #inizializzazione
    clientT_socket = socket.socket()
    #connessione al server
    clientT_socket.connect((host, port))
    # per poter specificare al serverc il tipo di client che si sta connettendo
    client = "clientt"
    clientT_socket.send(client.encode())
    print("      --------------------")
    print("Connessione al server effettuata.")
    print("      --------------------")

    # per poter effettuare operazioni
    print("Per terminare la connessione scrivere fine, \naltrimenti scrivere continua.")
    message = input(" -> ")

    # se il primo messaggio è "continua" verranno richieste le informazioni per 
    # poter apportare la modifica allo stato della validità del green pass
    if message.lower() == "continua":
        tessera_sanitaria = input("Inserisci il codice tessera sanitaria: ")
        modifica = input("Inserisci 'contagio' oppure 'guarigione' per le modifiche allo stato: ")
        
        # primo controllo sul codice della tessera sanitaria (ultime 8 cifre)
        if verify_code(tessera_sanitaria): 
            # controllo sull'inserimento della modifica
            if modifica.lower() == "contagio" or modifica.lower() == "guarigione":
                # invia i dati al server 
                data = f"{tessera_sanitaria},{modifica}"
                mess1 = f"{message}"
    
                clientT_socket.send(mess1.encode())
                clientT_socket.send(data.encode())
            else:
                print("Non è stato inserito un valore corretto per la modifica del green pass.\n")

            # per poter proseguire 
            print("Scegliere prossima azione:")
            message2 = input(" -> ")
            mess2 = f"{message2}"
            clientT_socket.send(mess2.encode())
        else: 
            print("Il formato inserito per la tessera sanitaria non è corretta. Inserire le ultime 8 cifre del codice. \n")

            
    # se il messaggio iniziale è "fine" la connessione al serverC verrà chiusa 
    if message.lower() == "fine":
        #chiudere la connessione
        clientT_socket.send("fine".encode())
        print("      --------------------")
        print("Chiusura della connessione avviata.")
        clientT_socket.close()

    #ulteriore controllo sul messaggio iniziale 
    if message.lower() != "continua" and message.lower() != "fine":
        print("Non è stato inserito un messaggio ammissibile per compiere operazioni.\n")
        

    # per chiudere la connessione alla fine delle operazioni
    print("      --------------------")
    print("Chiusura della connessione avviata.")
    clientT_socket.close()


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
    clientT_program()