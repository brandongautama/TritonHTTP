class HttpRequest:

    CRLF = '\r\n'

    def __init__(self):
        self.method = ''
        self.url = ''
        self.version = 0

        # key pair
        self.host = ''
        self.agent = ''
        self.connection = ''

        # valid or not
        self.invalid = None

    def parseRequest(self, request):
        # Check First line
        pos1 = request.find(HttpRequest.CRLF)
        firstLine = request[0:pos1]
        # Handle the leading & tailing space
        if len(firstLine.strip()) != len(firstLine):
            self.invalid = True
            print('Extra space in the first line of request')
            return

        # Extract first Line
        firstLinePart = firstLine.split(' ')
        if len(firstLinePart) != 3:
            self.invalid = True
            print('Wrong Format in the first line of request')
            return 

        if firstLinePart[0] == 'GET':
            self.method = firstLinePart[0]
        else:
            self.invalid = True
            print('Method not supported')
            return 

        if firstLinePart[1] == '/':
            self.url = '/index.html'
        else:
            self.url = firstLinePart[1]

        self.version = firstLinePart[2]
        

        # Check Key-Value Part
        ExtractLines = request.split(HttpRequest.CRLF)
        RestLines = ExtractLines[1:]
        for r in RestLines:
            if r:
                rp = r.split(': ')
                if len(rp) != 2:
                    self.invalid = True
                    print('Wrong Format in the key-value pair')
                    return
                else:
                    key = rp[0]
                    value = rp[1]
                    if key == 'Host':
                        self.host = value
                    if key == 'User-Agent':
                        self.agent = value
                    if key == 'Connection':
                        self.connection = value
        if not self.host:
            self.invalid = True
            print('Missing host in the key-value')
            return 

        return         
