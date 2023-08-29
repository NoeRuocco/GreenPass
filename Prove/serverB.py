#server che simula il server di controllo
 
import socket
import sqlite3


#funzione principale
def serverB_program():
    #per ottenere il nome dell'host
    host = socket.gethostname()
    #inizializzare la porta ad un numero superiore a 1024 poiché le precedenti sono riservate ad altro
    port = 5050

    #per ottenere un istanza 
    serverB_socket = socket.socket()
    #per legare l'indirizzo dell'host alla porta
    serverB_socket.bind((host, port))

    #configurare il numero di client che il server può ascoltare simultaneamente
    serverB_socket.listen(2)
    print("      --------------------")
    print("Server controllo green pass in ascolto.")

    #variabile per il controllo dello stato del server
    running = True
    while running:
        #per accettare una nuova connessione
        clientB_socket, address = serverB_socket.accept()
        #clientB2_socket, address = serverB_socket.accept()
        print("Connessione da parte di: " + str(address))
        print("      --------------------")
        #per gestire la connessione
        running = handle_clientB(clientB_socket)
        #running = handle_clientB2(clientB2_socket)

    #per chiudere le connessioni
    clientB_socket.close()  
    #clientB2_socket.close() 
     
    
    print("Il server verrà chiuso.")
    print("      --------------------")
    serverB_socket.close()


#funzione per gestire i client che richiedono il controllo su un green pass
def handle_clientB(clientB_socket):
    #ricevi le informazioni (pacchetti più grandi di 1024 bytes non verranno accettati)
    message = clientB_socket.recv(1024).decode()
    mess1 = message
    
    if mess1.lower() != "fine":
        data = clientB_socket.recv(1024).decode()
        card_id = data

        print("Dati ricevuti: \n-> codice tessera {}".format(card_id))
        #richiama il controllo su quella tessera sanitaria
        check_greenpass(clientB_socket, card_id)

        message2 = clientB_socket.recv(1024).decode()
        mess2 = message2

    #per uscire dal ciclo di gestione dei client
    if mess1.lower() == "fine" or mess2.lower() == "fine":
        print("      --------------------")
        print("Chiusura della connessione richiesta dal client.")
        clientB_socket.close()
        return False

    return True


#funzione per gestire i client che effettuano modifiche ai green pass
def handle_clientB2(clientB2_socket):
    #ricevi le informazioni (pacchetti più grandi di 1024 bytes non verranno accettati)
    message = clientB2_socket.recv(1024).decode()
    mess1 = message
    
    if mess1.lower() != "fine":
        data = clientB2_socket.recv(1024).decode()
        card_id = data

        print("Dati ricevuti: \n-> codice tessera {}".format(card_id))
        #per inserire o eliminare le informazioni dal database 
        
        message2 = clientB2_socket.recv(1024).decode()
        mess2 = message2

    #per uscire dal ciclo di gestione dei client
    if mess1.lower() == "fine" or mess2.lower() == "fine":
        print("      --------------------")
        print("Chiusura della connessione richiesta dal client.")
        clientB2_socket.close()
        return False

    return True


#funzione per verificare la validità del green pass
def check_greenpass(clientB_socket, card_id):
    #per creare o connettersi al database
    conn = sqlite3.connect('database2.db') 
    cursor = conn.cursor()

    #per verificare se il green pass è presente nel proprio database
    codice = card_id
    print("Si verificherà la validità del green pass appartenente alla tessera sanitaria {}".format(codice))
    cursor.execute("SELECT * FROM greenpass_data WHERE card_id=?", (codice,))
    result = cursor.fetchnone()

    if result:
        response = "NON VALIDO."
    else:
        response = "--cercare nell'altro db-- "

    #inviare la risposta al client
    clientB_socket.send(response.encode())


#funzione per salvare informazioni sui green pass non validi nel database
def save_to_database(card_id):
    #per creare o connettersi al database
    conn = sqlite3.connect('database2.db') 
    cursor = conn.cursor()

    #per creare la tabella nel caso non esista
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS greenpass_data (
                   id INTEGER PRIMARY KEY, 
                   card_id TEXT)
                   ''')

    #per inserire i dati nella tabella 
    cursor.execute('''INSERT INTO greenpass_data (card_id) 
                   VALUES (?)''', 
                   (card_id))

    #per salvare le modifiche
    conn.commit()
    conn.close()
    print("Il green pass non è più valido.")


#funzione per eliminare i green pass dal database quando tornano validi 
def delete_from_database(card_id):
    #connessione al database
    conn = sqlite3.connect('database2.db')
    cursor = conn.cursor()

    #elimina quella tessera sanitaria dalla tabella dei green pass non validi
    cursor.execute('DELETE FROM card_data')  
    conn.commit()

    conn.close()
    print("Il green pass è tornato valido.")


#funzione per mostrare il contenuto del database
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
    serverB_program()