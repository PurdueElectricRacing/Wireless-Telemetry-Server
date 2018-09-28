import asyncio
import websockets
import time
import datetime
import json

# Contains list of all connected users
USERS = set()

def get_server(ip, port):
    return websockets.serve(on_client_connect, ip, port)

# Main server entry point
async def on_client_connect(websocket, path):
    
    connection_addr = f'{websocket.remote_address[0]}:{websocket.remote_address[1]}'
    print(f'Connected to client at {connection_addr} on {datetime.datetime.now()}.')

    await websocket.send(json.dumps({'type':'connected','payload':'true', 'timestamp':time.time()}))
    
    global USERS
    try:
        # Track all connected users to broadcast new data whenever available
        USERS.add(websocket)
        # Recieve handler is used to monitor messages from the clients.
        await recieve_data_loop(websocket)
        # Client disconnects whenever this handler returns.
        USERS.remove(websocket)
    finally:
        print("Client disconnected.")
            
        
#Broadcast data to all users connected on the socket
async def send_data(data):
    global USERS
    if USERS:
        payload = json.dumps({'type':'data','payload':data, 'timestamp':time.time()})
        await asyncio.wait([user.send(payload) for user in USERS])
  

# This function runs in its own loop to handle recieving any messages
async def recieve_data_loop(websocket):
    while websocket.open:
        try:
            message = await websocket.recv()
            print(f'Message from client: {message}')
        except:
            return

if __name__ == "__main__":
    ip = '127.0.0.1'
    port = 5000
    asyncio.get_event_loop().run_until_complete(get_server(ip. port))
    print(f'Serving websocket server on {ip}:{port} ...')
    asyncio.get_event_loop().run_forever()
