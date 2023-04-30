import socket
import requests
import json

IP = socket.gethostbyname(socket.gethostname())
PORT = 14000
ADDRESS = (IP, PORT)
SERVER = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

page = 1
total_pages = float('inf')
data = {'page': None, 'total': 0, 'items': []} # creating a dictionary to hold the data from the api
print("[STARTING BROADCAST...]")
while page <= total_pages: #infinite loop
    print(f"[INITIALIZING DATA FOR PAGE {page}]")
    #adds paging params to the get call
    response = requests.get('https://api.fbi.gov/wanted/v1/list', params={
        'page': page,
        'per_page': 10  # request 10 items per page
    })
    #deserializes the data and stores it in the result variable
    result = json.loads(response.content)
    #extracts the properties from the obj and stores it in the data variable
    data['page'] = result['page']
    data['total'] = result['total']
    #appends the data to the list instead of overwriting it
    data['items'].extend(result['items'])
    #error handling
    try:
        total_pages = result['total_pages']
    except KeyError:
        total_pages = float('inf')
    #prints items until the loop breaks
    if len(result['items']) > 0:
        for item in result['items']:
            print(f"Title: {item['title']}")
    else:
        print("No items on this page.")
        print("[ENDING BROADCAST...]")
        break
        #serializes the data into a jsonstring with utf encoding
    payload = json.dumps(data).encode('utf-8')
    chunk_size = 1024  # set the size of each chunk
    #creates a list using comprehension that iterates over the payload bytes object in chunks of chunk_size bytes using the range
    #method
    chunks = [payload[i:i+chunk_size] for i in range(0, len(payload), chunk_size)]
    #looping over the chunks in the list
    for chunk in chunks:
        SERVER.sendto(chunk, ADDRESS)

    page += 1
