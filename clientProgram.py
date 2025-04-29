import socket

#Variables
MAXBYTES = 120
mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
valid = False

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
while not valid:
    selection = int(input("Please choose from the flowing options:\n" \
    "1. What is the average moisture inside my kitchen fridge in the past three hours?\n"\
    "2. What is the average water consumption per cycle in my smart dishwasher?\n"\
    "3. Which device consumed more electricity among my three IoT devices "\
    "(two refrigerators and a dishwasher)?\n"))#Gets the users message
    if selection > 3 or selection < 1:
        print('Sorry, this query cannot be processed.' )
        continue
    mainSocket.send(bytearray(selection, encoding='utf-8'))
    response = mainSocket.recv(MAXBYTES).decode()
    print(f'Server response: {response}')
    valid = True
mainSocket.close()


    


