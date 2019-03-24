import sys
import socket
import httpRequest
import time 
import httpResponse
import threading

connStr = ''

#Handle each complete request
def clientThreadRequest(conn, doc_root, firstRequest):
    #Process the input request
    toParse = httpRequest.HttpRequest()
    toParse.parseRequest(firstRequest)

    #Process the output response
    responseObj = httpResponse.HttpResponse()
    responseObj.serverResponse(toParse, doc_root)
    print(responseObj.response)
    tn = threading.currentThread().getName()
    print(tn)

    #Send the response to client
    conn.sendall(responseObj.response)
    global connStr 

    #Check the connection state
    connStr = responseObj.connection

#Handle requests from one client
def clientThread(conn, doc_root):
        # send a thank you message to the client.
        #conn.sendall(b'Thank you for connecting')
        #time.sleep(5)
        buffer = ''
        while True:
            if buffer == '':
                try:
                    data =  conn.recv(1024)
                except socket.timeout:
                    print('too long')
                    conn.close()
                    return
            elif '\r\n\r\n' not in buffer: 
                try:
                    data =  conn.recv(1024)
                except socket.timeout:
                    print('too longs')
                    conn.sendall(b'HTTP/1.1 400 Client Error')
                    conn.close()
                    return
            buffer += data.decode('UTF-8')
            while "\r\n\r\n" in buffer:
                index = buffer.index("\r\n\r\n")
                firstRequest = buffer[0:index]
                tn = threading.currentThread().getName()
                print(tn)
                t = threading.Thread(target = clientThreadRequest, args= (conn, doc_root, firstRequest))
                t.start()
                buffer = buffer[index+4::]
                t.join()
                if connStr == 'close':
                    state = 1
                    conn.close()
                    return

class MyServer:
    def __init__(self, port, doc_root):
        self.port = port
        self.doc_root = doc_root
        self.host = "localhost"

    """
    Add your server and handlers here.       
    """
    
    def startServer(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        print('Socket successfully created')

        try:
            serverSocket.bind((self.host, self.port))
        except:
            print('Port used')
            sys.exit()

        serverSocket.listen(5)

        print('Server is running!')
        while True: 
            # Establish connection with client.
            conn, addr = serverSocket.accept()      
            print('Got connection from '+ str(addr))
            conn.settimeout(5)

            t = threading.Thread(target = clientThread, args= (conn, self.doc_root))
            t.start()


if __name__ == '__main__':
    input_port = int(sys.argv[1])
    input_doc_root = sys.argv[2]
    server = MyServer(input_port, input_doc_root)
    # Add code to start your server here
    server.startServer()
