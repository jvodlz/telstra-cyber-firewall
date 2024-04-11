# Firewall Server Handler

from http.server import BaseHTTPRequestHandler, HTTPServer

host = "localhost"
port = 8000


#########
# Handle the response here 
def has_bad_header(self):
    bad_header = {"suffix":"%>//",
                "c1":"Runtime",
                "c2":"<%",
                "DNT":"1",
                "Content-Type":"application/x-www-form-urlencoded"
    }

    for k,v in bad_header:
        if self.headers.get(k) != v:
            return True
    return False


def block_request(self):
    print("Blocking request")
    self.close_connection = True
    self.send_error(
        403, "Request blocked by firewall"
    )


def handle_request(self):
    filename = 'tomcatwar.jsp'
    if filename in self.path or self.has_bad_header(): 
        block_request(self)
    else:
        self.send_response(200)
    self.send_header("content-type", "application/json")
    self.end_headers()


#########



class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        handle_request(self)


    def do_POST(self):
        handle_request(self)


if __name__ == "__main__":        
    server = HTTPServer((host, port), ServerHandler)
    print("[+] Firewall Server")
    print("[+] HTTP Web Server running on: %s:%s" % (host, port))


    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


    server.server_close()
    print("[+] Server terminated. Exiting...")
    exit(0)