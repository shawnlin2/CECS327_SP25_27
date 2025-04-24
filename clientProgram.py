import socket

#Variables
MAXBYTES = 120
mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Grab and check the users input
while True:
    try:
        port = int(input('Enter the server port: '))
        if port < 0:
            print("Port number can not be less than zero")
            continue
        IPAddress = input("Enter the IP address: ")

    except ValueError as error:
        print("Port number can not be a none number")
        

    #Tries to establish a socket connection based on the input
    try:
        socket.inet_aton(IPAddress)
        mainSocket.connect((IPAddress, port))
        break
    except socket.error as e:
        print("Socket could not be binded to the given port and address. \n"
        "Double check that you entered the port and IP Address correctly")
        

#Message Sending 
while True:
    message = input("Enter a message to send(exit() to quit): ")#Gets the users message
    mainSocket.send(bytearray(message, encoding='utf-8'))
    if message == 'exit()':#Checks for if the message is exit() and stops the program if that is the case
        mainSocket.close()
        break
    response = mainSocket.recv(MAXBYTES).decode()
    print(f'Server response: {response}')



    


