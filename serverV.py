# server che si occupa di verificare la validità, quindi lo stato, di un green pass
# a seguito di una richiesta da un clientS e inoltre di modificarne lo stato 
# a seguito di notifica da un clientT 

import socket
import sqlite3

# funzione principale del serverV
def serverV_program():
    # per ottenere il nome dell'host
    host = socket.gethostname()
    # inizializzare la porta ad un numero superiore a 1024 (le precedenti sono riservate)
    port = 5050

    # per ottenere un istanza
    serverV_socket = socket.socket()
    # per legare l'indirizzo dell'host alla porta
    serverV_socket.bind((host, port))

    # configurare il numero di client che il server può ascoltare simultaneamente
    serverV_socket.listen(2)
    print("      --------------------")
    print("Server controllo validità green pass in ascolto.")

    # variabile per verificare lo stato del server
    running = True 
    # per poter gestire le connessioni in modo corretto in base al tipo di client 
    while running:
        # per accettare una nuova connessione dal client (ancora generico)
        client_socket, address = serverV_socket.accept()
        print("Connessione da parte di: " + str(address))
        print("      --------------------")

        # per gestire il tipo di client (specifico)
        client = client_socket.recv(1024).decode()
        if client.lower() == "clients":
            #gestire la connessionedel clientB
            print("La connessione è stata effettuata da un clientB.\n")
            running = handle_clientS(client_socket)
        else: 
            if client.lower() == "clientt":
                #gestire la connessione da parte dei client B2
                print("La connessione è stata effettuata da un clientB2.\n")
                running = handle_clientT(client_socket)
            else:
                print("Tipo do client sconosciuto, la connessione verrà chiusa. \n")
                client_socket.close()
                continue

    # a seguito della fine delle operazioni da parte del client 
    print("Il programma client è stato chiuso.\n")
    client_socket.close()

    #termina il programma chiudendo la socket del server
    print("Il server verrà chiuso.")
    print("      --------------------")
    serverV_socket.close()


# funzione per gestire i clientS, che richiedono il controllo della validità di un green pass
def handle_clientS(clientS_socket):
    # per essere sicuri che si stia utilizzando il corretto handle
    print("Si sta utilizando la funzione per la gestione del clientS che ha richiesto la verifica di validità. \n")
    # ricevi le informazioni (pacchetti più grandi di 1024 bytes non verranno accettati)
    message = clientS_socket.recv(1024).decode()
    mess1 = message
    
    # controllo sul messaggio ricevuto
    if mess1.lower() == "continua":
        # ricevi dati dal client
        data = clientS_socket.recv(1024).decode()
        tessera_sanitaria = data
        print("Dati ricevuti: \n-> codice tessera {}".format(tessera_sanitaria))
        
        # richiama il controllo su quella tessera sanitaria
        stato = check_greenpass(tessera_sanitaria)
        # invia la risposta al client che ha effettuato la richiesta
        clientS_socket.send(stato.encode())

        # per sapere come proseguire
        message2 = clientS_socket.recv(1024).decode()
        mess2 = message2
    else: 
        print("Non è stato ricevuto un messaggio corretto.\n")
        return False 

    #per uscire dal ciclo di gestione dei client
    if mess1.lower() == "fine" or mess2.lower() == "fine":
        print("      --------------------")
        print("Chiusura della connessione richiesta dal client.")
        clientS_socket.close()
        return False
        
    return False


# funzione per gestire i clientT, che inviano una notifica per modificare lo stato del green pass
def handle_clientT(clientT_socket):
    # per essere ricuri dell'handle che si utilizza
    print("Si sta utilizando la funzione per la gestione dei clientT, che ha inviato una modifica allo stato del green pass. \n")
    #ricevi le informazioni (pacchetti più grandi di 1024 bytes non verranno accettati)
    message = clientT_socket.recv(1024).decode()
    mess1 = message
    
    # controllo sul messaggio ricevuto 
    if mess1.lower() == "continua":
        # ricevi dati dal client
        data = clientT_socket.recv(1024).decode()
        tessera_sanitaria, modifica = data.split(',')
        print("Dati ricevuti: \n-> codice tessera {}, \n-> modifica {}".format(tessera_sanitaria, modifica)) 
        # per capire il tipo di modifica da effettuare
        if modifica.lower() == "contagio" or modifica.lower() == "guarigione":
            modify_greenpass(tessera_sanitaria, modifica)
        else:
           # ulteriore controllo
           if modifica.lower() != "contagio" and modifica.lower() != "guarigione":
                print("Le uniche parole accettabili per lo stato sono 'contagio' oppure 'guarigione'. \n")

        # per sapere come proseguire
        message2 = clientT_socket.recv(1024).decode()
        mess2 = message2
    else: 
        print("Non è stato consegnato un messaggio coerente.\n") 
        return False   

    # per uscire dal ciclo di gestione dei client
    if mess1.lower() == "fine" or mess2.lower() == "fine":
        print("      --------------------")
        print("Chiusura della connessione richiesta dal client.")
        clientT_socket.close()
        return False
    
    return False
    

# funzione per verificare la validità del green pass
def check_greenpass(tessera_sanitaria):
    # per creare o connettersi al database
    conn = sqlite3.connect('database.db') 
    cursor = conn.cursor()

    # per verificare se il green pass è presente nel database
    tessera = tessera_sanitaria
    print("Si verificherà la validità del green pass appartenente alla tessera sanitaria {}\n".format(tessera))
    cursor.execute("SELECT stato FROM greenpass WHERE tessera_sanitaria=?", (tessera,))
    result = cursor.fetchone()
    # per mandare il risultato al client
    if result:
        return result[0]
    else:
        return "Non presente nel database"
    
    # per chiudere la connessione al database
    conn.close()


# funzione per modificare lo stato di validità di un green pass
def modify_greenpass(tessera_sanitaria, modifica):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    tessera = tessera_sanitaria

    # per scegliere l'azione in base alla modifica richiesta 
    if modifica.lower() == "contagio":
        nuovo_stato = "non valido"
        cursor.execute("UPDATE greenpass SET stato = ? WHERE tessera_sanitaria = ?", (nuovo_stato, tessera,))
        conn.commit()
    else:
        if modifica.lower() == "guarigione":
            nuovo_stato = "valido"
            cursor.execute("UPDATE greenpass SET stato = ? WHERE tessera_sanitaria = ?", (nuovo_stato, tessera,))
            conn.commit()
        else: 
            if modifica.lower() != "contagio" and modifica.lower() != "guarigione":
                print("Non è stata inserita una modifica di stato accettabile. \n")

    # per chiudere la connessione
    conn.close()


# funzione per mostrare il contenuto del database
def display_database_contents():
    # connessione al database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # selezionare tutto il contenuto
    cursor.execute('SELECT * FROM greenpass')
    rows = cursor.fetchall()
    # stampare il contenuto
    print("\n******************************")
    print("Contenuto del database:")
    for row in rows:
        print("ID: ", row[0])
        print("Codice tessera: ", row[1])
        print("Tempo validità greenpass: ", row[2])
        print("Stato del greenpass: ", row[3])
        print("----------------------------")

    # chiudere la connessione al database
    conn.close()
    


# per specificare il metodo di esecuzione
if __name__ == '__main__':
    # prima viene eseguito il programma principale del server
    serverV_program()
    # alla fine del programma principale viene mostrato il contenuto del database
    display_database_contents()