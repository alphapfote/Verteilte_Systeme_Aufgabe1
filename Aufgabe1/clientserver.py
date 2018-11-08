import logging
import socket
import json
import constCS
import lab_logging

lab_logging.setup()  # init loging channels for the lab

# TCP-Server ---------------------------------------------------------------------------------------
class Server:
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Server")

    # Telefonbuch-Liste
    tel = {'natalia': '1234', 'alice': '8765', 'jana': '2921', 'hendrik': '1801'}

    # Socket initialisieren
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Gibt den Socket nach dem Schließen der Verbindung wieder frei, verhindert "addresses in use"-Errors:
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
        self.sock.bind((constCS.HOST, constCS.PORT))
        self.logger.info("Server bound to socket " + str(self.sock))

    # Auf Nachricht warten (listen) und dann die Anfrage bearbeiten
    def serve(self):
        self.sock.listen(1)
        self.logger.info("Server is listening for client")

        (connection, address) = self.sock.accept()  # Gibt den neuen Socket und Adresse des Clients zurück 
        
        while True:  # für immer
            data = connection.recv(1024).decode('ascii')  # Erhalte Daten vom Client

            # print ("Erhaltener command:" + data.decode('ascii'))
            if not data:
                # TCP-Verbindung verloren 
                self.logger.info("Server didn´t get data")
                break

            self.logger.info("Server got some data: " + data)            
            # Sende komplettes Telefonbuch
            if data == 'getAll':
                teljson = json.dumps(self.tel)
                #for key, value in self.tel.items():
                print(teljson)
                connection.send(teljson.encode('ascii'))
                self.logger.info("Server sent data: " + teljson)
                break

            # Sende einzelnen Eintrag aus dem Telefonbuch 
            elif data in self.tel:   
                connection.send((data + ' - ' + self.tel[data]).encode('ascii'))
                self.logger.info("Server sent data: " + self.tel[data])
                break

            # Zu sendende Daten im Telefonbuch nicht gefunden 
            else:
                connection.send(('No data found for ' + data).encode('ascii'))
                break
            
        connection.close()  # Schließe die Verbindung
        self.sock.close()
        self.logger.info("Server closed connection.")

        
# TCP-Client ---------------------------------------------------------------------------------------
class Client:
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    # Socket initialisieren
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((constCS.HOST, constCS.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

    def call(self, msg_in="Hello, world"):
        self.sock.send(msg_in.encode('ascii'))  # send encoded string as data
        
        data = self.sock.recv(1024)  # Erhalte die Antwort vom Server
        
        msg_out = data.decode('ascii')
        print(msg_out)  # print the result
        self.sock.close()  # Schließe die Verbindung
        self.logger.info("Client down.")
        return msg_out

    # Einzelner Eintrag aus dem Telefonbuch anfragen
    def get(self, name):
        self.sock.send(name.encode('ascii')) # Sende Command als String
        self.logger.info("Client sent name: " + name)

        data = self.sock.recv(1024)  # Erhalte die Antwort vom Server
        self.logger.info("Client got response: " + data.decode('ascii'))

        number = data.decode('ascii')
        self.sock.close()  # Schließe die Verbindung
        self.logger.info("Client closed connection.")
        return number

    # Komplettes Telefonbuch anfragen
    def getAll(self):
        self.sock.send('getAll'.encode('ascii')) # Sende Command als String
        self.logger.info("Client sent getAll")

        data = self.sock.recv(1024)  # Erhalte die Antwort vom Server
        output = data.decode('ascii')
        self.logger.info("Client got response: " + output)

        dataToArray = json.loads(data)
        for key, value in dataToArray.items():
           print(key + ' ' + value + ';')
        self.sock.close()  # Schließe die Verbindung
        self.logger.info("Client closed connection.")
        return dataToArray
