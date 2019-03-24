import os.path, time
import os
import datetime

class HttpResponse:

    CRLF = '\r\n'

    def __init__(self):
        self.version = ''
        self.statusCode = 0
        self.msgCode = ''

        self.lastMod = ''
        self.contentType = ''
        self.contentLen = ''
        self.contents = ''
        self.connection = ''
        self.response = ''

        self.close = None
    
    #Process the Last-Modified time in correct format 
    def processTime(self, path):
        strs = time.strftime('%a, %d %b %y %H:%M:%S', time.gmtime(os.path.getmtime(path)))
        print(time.gmtime(os.path.getmtime(path)))
        pacific_now = datetime.datetime.now(datetime.timezone.utc).astimezone()
        pacific_now = (str)(pacific_now)
        pacific_now = pacific_now[-6::]
        self.lastMod = strs + ' ' + pacific_now


    def serverResponse(self, request, doc_root):

        # parse doc_root
        if doc_root.strip()[-1] == '/':
            doc_root = doc_root[:-1]

        path = doc_root +  request.url

        stack = []
        items = path.split('/')
        for item in items:
            if item == '.':
                continue
            elif item == '..':
                stack.pop(-1)
            else:
                stack.append(item)

        simplifiedPath = '/'.join(stack)
        simplifiedPath = '/' + simplifiedPath

        #400
        if request.version != 'HTTP/1.1' or request.url[0] != '/' or request.invalid:
            self.version = 'HTTP/1.1'
            self.statusCode = 400
            self.msgCode = 'Client Error'
            self.close = True
            self.processError()
            return
        elif not os.path.isfile(path) or doc_root not in simplifiedPath:
        # 404 Not Found: The requested content wasn’t there
            self.version = 'HTTP/1.1'
            self.statusCode = 404
            self.msgCode = 'Not Found'
            self.close = True
            self.processError();
            return
        else:
        # 200
            self.version = "HTTP/1.1"
            self.statusCode = 200
            self.msgCode = "OK"
            self.processResponseFile(path)

            self.processTime(path)

            self.contentLen = os.stat(path).st_size
            self.close = False


            if request.connection == 'close':
                self.connection = request.connection
            else:
                self.connection = 'open'

            if request.url[-4:] == "html":
                self.contentType = 'text/html'
                self.processResponseFormatText()
            elif request.url[-3:] == "jpg":
                self.contentType = 'image/jpeg'
                self.processResponseFormatImage()
            elif request.url[-3:] == "png":
                self.contentType = 'image/png'
                self.processResponseFormatImage()


    def processResponseFile(self, path):
        file = open(path, 'rb')
        self.contents = file.read()
        file.close()

    def processResponseFormatText(self):
        self.response = self.version + ' ' + (str)(self.statusCode) + ' ' + self.msgCode + HttpResponse.CRLF
        self.response += 'Server: Myserver 1.0' +  HttpResponse.CRLF
        self.response += 'Last-Modified: ' + self.lastMod + HttpResponse.CRLF
        self.response += 'Content-Type: ' + self.contentType + HttpResponse.CRLF
        self.response += 'Content-Length: ' + (str)(self.contentLen) + HttpResponse.CRLF
        self.response += 'Connection: ' + self.connection + HttpResponse.CRLF + HttpResponse.CRLF
        self.response += self.contents.decode('UTF-8')
        self.response = self.response.encode('UTF-8')

    def processResponseFormatImage(self):
        self.response = self.version + ' ' + (str)(self.statusCode) + ' ' + self.msgCode + HttpResponse.CRLF
        self.response += 'Server: Myserver 1.0' +  HttpResponse.CRLF
        self.response += 'Last-Modified: ' + self.lastMod + HttpResponse.CRLF
        self.response += 'Content-Type: ' + self.contentType + HttpResponse.CRLF
        self.response += 'Content-Length: ' + (str)(self.contentLen) + HttpResponse.CRLF
        self.response += 'Connection: ' + self.connection + HttpResponse.CRLF + HttpResponse.CRLF
        self.response = self.response.encode('UTF-8')
        self.response += self.contents

    def processError(self):
        self.response = self.version + ' ' + (str)(self.statusCode) + ' ' + self.msgCode + HttpResponse.CRLF
        self.response += 'Server: Myserver 1.0' +  HttpResponse.CRLF
        self.response += HttpResponse.CRLF
        self.response += HttpResponse.CRLF
        self.response = self.response.encode('UTF-8')


