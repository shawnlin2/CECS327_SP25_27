import socket

#Variables
mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
MAXBYTE = 120

#Getting the users input to set up the port
while True:
    try:
        port = int(input('Enter the server port: '))
        if port < 0:#Check to make sure that the port is a positive nonzero integer
            print("Port number can not be less than zero")
            continue
        mainSocket.bind(('localhost', port))
        break
    
    except ValueError as error:#Grabs the error if the user did not enter a integer for the port
        print("Port number can not be a none number")
    except socket.error as error: #Grabs any error that has to do with the socket
        print(f"Error: {error}")
        print(f"Try Again")

mainSocket.listen(5)
incomingSocket, incomingAddress = mainSocket.accept()

#Simulates the user's action
while True:
    message = incomingSocket.recv(MAXBYTE).decode()#Gets the message and decodes it
    if message != "exit()":#Checks for the message not being exit()
        newMessage = message.upper()
        incomingSocket.send(bytearray(newMessage, encoding="utf-8"))
    else:
        incomingSocket.close()#Closes the incomingSocket
        mainSocket.close() #Closes the mainSocket 
        break
    

