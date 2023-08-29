#server che simula il server vaccini

import socket
import sqlite3


#programma principale
def serverA_program():
    #per ottenere il nome dell'host
    host = socket.gethostname()
    #inizializzare la porta ad un numero superiore a 1024 poiché le precedenti sono riservate ad altro
    port = 5000

    #per ottenere un istanza 
    serverA_socket = socket.socket()
    #per legare l'indirizzo dell'host alla porta
    serverA_socket.bind((host, port))

    #configurare il numero di client che il server può ascoltare simultaneamente
    serverA_socket.listen(2)
    print("      --------------------")
    print("Server vaccinazioni in ascolto.")

    #variabile per il controllo dello stato del server
    running = True
    while running:
        #per accettare una nuova connessione
        clientA_socket, address = serverA_socket.accept()
        print("Connessione da parte di: " + str(address))
        print("      --------------------")
        #per gestire la connessione
        running = handle_client(clientA_socket)

    #per chiudere le connessioni
    clientA_socket.close() 
    
    print("Il server verrà chiuso.")
    print("      --------------------")
    serverA_socket.close()
        

#programma per gestire il client che si connette al server
def handle_client(clientA_socket): 
    #ricevi le informazioni (pacchetti più grandi di 1024 bytes non verranno accettati)
    message = clientA_socket.recv(1024).decode()
    mess1 = message
    
    if mess1.lower() != "fine":
        data = clientA_socket.recv(1024).decode()
        card_id, status = data.split(',')
        #salvare i dati neldatabase
        print("Dati ricevuti: \n-> codice tessera {}, \n-> stato {}".format(card_id, status))
        save_to_database(card_id, status)
        message2 = clientA_socket.recv(1024).decode()
        mess2 = message2

    #per uscire dal ciclo di gestione dei client
    if mess1.lower() == "fine" or mess2.lower() == "fine":
        print("      --------------------")
        print("Chiusura della connessione richiesta dal client.")
        clientA_socket.close()
        return False

    return True


#funzione per salvare i dati nel database delle persone vaccinate
def save_to_database(card_id, status):
    #per creare o connettersi al database
    conn = sqlite3.connect('database.db') 
    cursor = conn.cursor()

    #per creare la tabella nel caso non esista
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS card_data (
                   id INTEGER PRIMARY KEY, 
                   card_id TEXT, 
                   status TEXT)
                   ''')

    #per inserire i dati nella tabella 
    cursor.execute('''
                   INSERT INTO card_data (card_id, status) 
                   VALUES (?, ?)''', 
                   (card_id, status))

    #per salvare le modifiche
    conn.commit()
    conn.close()
    print("I dati sono stati inseriti correttamente nel database.")


#funzione per visualizzare il contenuto del database
def display_database_contents():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM card_data')
    rows = cursor.fetchall()

    print("\n******************************")
    print("Contenuto del database:")
    for row in rows:
        print("ID: ", row[0])
        print("Codice tessera: ", row[1])
        print("Stato green pass: ", row[2])
        print("----------------------------")

    conn.close()
    

if __name__ == '__main__':
    serverA_program()
    #alla chiusura del server verrà mostrato il contenuto del suo database 
    display_database_contents()