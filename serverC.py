# server centro vaccinale che si occupa di ricevere tutte le informazioni 
# sui nuovi green pass validi inviati dal centro vaccinale (clientCV)

import socket
import sqlite3

# funzione principale per l'esecuzione del serverV
def serverC_program():
    # per ottenere il nome dell'host
    host = socket.gethostname()
    # inizializzare la porta ad un numero superiore a 1024 poiché le precedenti sono riservate ad altro
    port = 5000

    # per ottenere un istanza
    serverC_socket = socket.socket()
    # per legare l'indirizzo dell'host alla porta
    serverC_socket.bind((host, port))

    # configurare il numero di client che il server può ascoltare simultaneamente
    serverC_socket.listen(2)
    print("      --------------------")
    print("Server centro vaccinazioni in ascolto.")

    # variabile per il controllo dello stato del server
    running = True
    while running:
        # per accettare una nuova connessione
        clientCV_socket, address = serverC_socket.accept()
        print("Connessione da parte di: " + str(address))
        print("      --------------------")
        # per gestire la connessione da parte dei client 
        running = handle_client(clientCV_socket)

    #per chiudere le connessioni
    print("Il programma client è stato chiuso.\n")
    clientCV_socket.close() 
    
    # per chiudere il server alla fine delle operazioni
    print("Il server verrà chiuso.")
    print("      --------------------")
    serverC_socket.close()


# funzione per gestire i client che si connettono al server
def handle_client(clientCV_socket): 
    # ricevi le informazioni (pacchetti più grandi di 1024 bytes non verranno accettati)
    message = clientCV_socket.recv(1024).decode()
    mess1 = message
    
    # se il client ha inviato come messaggio iniziale "continua", 
    # allora si posso salvare nel database i dati inviati 
    if mess1.lower() == "continua":
        # recuperare i dati dal client 
        data = clientCV_socket.recv(1024).decode()
        tessera_sanitaria, tempo_val, stato = data.split(',')
        # salvare i dati nel database
        print("Dati ricevuti: \n-> codice tessera {}, \n-> tempo validità {}, \n-> stato {}".format(tessera_sanitaria, tempo_val, stato))
        save_to_database(tessera_sanitaria, tempo_val, stato)
        # per sapere come proseguire dopo il primo invio di dati
        message2 = clientCV_socket.recv(1024).decode()
        mess2 = message2
    else:
        print("Non è stato ricevuto un messaggio coerente.\n")
        return False

    # per uscire dal ciclo di gestione dei client e finire l'operazione
    if mess1.lower() == "fine" or mess2.lower() == "fine":
        print("      --------------------")
        print("Chiusura della connessione richiesta dal client.")
        clientCV_socket.close()
        return False

    return True


# funzione per poter salvare i dati nel database 
def save_to_database(tessera_sanitaria, tempo_val, stato):
    # per creare o connettersi al database
    conn = sqlite3.connect('database.db') 
    cursor = conn.cursor()

    # per creare la tabella nel caso non esista
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS greenpass (
                   id INTEGER PRIMARY KEY, 
                   tessera_sanitaria TEXT, 
                   tempo_val TEXT,
                   stato TEXT)
                   ''')

    # per inserire i dati nella tabella 
    cursor.execute('''
                   INSERT INTO greenpass (tessera_sanitaria, tempo_val, stato) 
                   VALUES (?, ?, ?)''', 
                   (tessera_sanitaria, tempo_val, stato,))

    # per salvare le modifiche
    conn.commit()
    # per chiudere la connessione al database
    conn.close()
    print("I dati sono stati inseriti correttamente nel database.")


# funzione per visualizzare il contenuto del database
def display_database_contents():
    # per connettersi o creare il database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # per selezionare tutto il contenuto del database
    cursor.execute('SELECT * FROM greenpass')
    rows = cursor.fetchall()
    # per stampare a video il contenuto
    print("\n******************************")
    print("Contenuto del database:")
    for row in rows:
        print("ID: ", row[0])
        print("Codice tessera: ", row[1])
        print("Tempo validità del green pass: ", row[2])
        print("Stato green pass: ", row[3])
        print("----------------------------")

    # per chiudere la connessione al database
    conn.close()

   
# per specificare il metodo di esecuzione
if __name__ == '__main__':
    # prima viene eseguito il programma relativo al server
    serverC_program()
    # quando il server viene chiuso, viene visualizzato il contenuto del database
    display_database_contents()