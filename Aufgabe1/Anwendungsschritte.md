# Anwendungsschritte zur Ausführung des Programms

## 1. Server starten
Starten Sie zuerst das Notebook des Servers.

## 2. Client starten
Passen Sie den Client an, abhängig davon, welche Daten Sie gerne erhalten möchten. <br>
Rufen Sie hierzu die GETALL-Methode (mit der Funktion getAll()) oder die GET-Methode (mit der Funktion get(String name))  mit dem gewünschtem Namen auf. <br>
Starten Sie nun das Notebook des Clients.

## 3. Überprüfen Sie, ob die erhaltenen Daten richtig sind.

## Fehlerbehebung 
Wenn der Fehler "Socket already in use" kommt, muss man die Prozesse auf den Port beenden, sodass er wieder freigegeben ist. <br>
Im Terminal in Mac: <br>
  sudo lsof -i tcp: <portnummer> <br>
  sudo kill -9 <PID> <br>
