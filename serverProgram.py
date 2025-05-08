import socket
import psycopg2
import time

MAX_BYTES_TO_RECEIVE = 10000
MAX_BACKLOG = 5

# NeonDB config (replace with your real info)
NEON_DB_DSN = "postgresql://neondb_owner:npg_0srythD3oBMH@ep-sparkling-hat-a5078nm2-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"


# SQL Queries
QUERIES = {
    "1": """
        SELECT avg(value::FLOAT) AS total_moisture
        FROM public."NeonDBTable_virtual",
            jsonb_each_text(payload::jsonb) AS kv(key, value)
        WHERE key ~* 'Moisture Meter'
           AND time >= NOW() - INTERVAL '3 hours'
                 AND payload->>'board_name' IN ('Fridge Board', 'Fridge 2 Board')
    """,
    "2": """
        SELECT AVG((payload->>'YF-S201 - Water Flow Sensor Dishwasher 1')::FLOAT * 0.26)
        FROM public."NeonDBTable_virtual"
        WHERE time >= NOW() - INTERVAL '3 hours'
          AND payload->>'board_name' = 'DishWasher Board';
    """,
    "3": """
        SELECT payload->>'board_name' AS device, SUM(ABS(value::FLOAT)) AS total_current
        FROM public."NeonDBTable_virtual",
            jsonb_each_text(payload::jsonb) AS kv(key, value)
        WHERE time >= NOW() - INTERVAL '3 hours'
            AND key ~* 'ACS712'
        GROUP BY payload->>'board_name'
        ORDER BY payload->>'board_name'
        LIMIT 1
    """
}

def get_query_result(choice):
    try:
        with psycopg2.connect(dsn=NEON_DB_DSN) as conn:
            with conn.cursor() as cur:
                cur.execute(QUERIES[choice])
                result = cur.fetchone()
                if result is None:
                    return "No data found."
                if choice == "3":
                    device, board = result[0].split(' Board') 
                    return f"{device} consumed {result[1]:.2f} total amps in the last 3 hours"
                return f"{float(result[0]):.2f}"
    except Exception as e:
        return f"Database error: {e}"


# --- Original TCP Setup Below ---

TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketEstablished = False

while not socketEstablished:
    validInput = False
    try:
        enteredPortNumber = input('Enter server port number: ')
        portNumber = int(enteredPortNumber)
        if portNumber < 0:
            raise ValueError
        validInput = True
    except ValueError:
        print(f"Port number must be a non-negative integer. Entered value: {enteredPortNumber}")

    if validInput:
        try:
            TCPSocket.bind(('', portNumber))
            socketEstablished = True
        except socket.error as e:
            print(f"Error establishing socket: {e}")

TCPSocket.listen(MAX_BACKLOG)
incomingSocket, incomingAddress = TCPSocket.accept()

print("Connection established. Awaiting message from client")

receivingMessages = True
while receivingMessages:
    #incomingSocket.send(b"Choose query: 1 (Fridge moisture), 2 (Dishwasher water), 3 (Highest energy user)\n")
    incomingMessage = incomingSocket.recv(MAX_BYTES_TO_RECEIVE).decode().strip()
    print(f"Incoming message: {incomingMessage}")

    if incomingMessage == 'exit()':
        receivingMessages = False
        break

    if incomingMessage in {"1", "2", "3"}:
        response = get_query_result(incomingMessage)
    else:
        response = "Invalid input. Enter 1, 2, or 3"

    incomingSocket.send(bytearray(response + "\n", encoding="utf-8"))

incomingSocket.close()
TCPSocket.close()
