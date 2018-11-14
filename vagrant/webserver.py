from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi #common gatway interface

class WebServerHandler(BaseHTTPRequestHandler): #tells what code to excute based on the http request
# extends BaseHTTPRequestHandler
	def do_GET(self):
		try:
			if self.path.endswith("/hello"): #path refers to the url sent by the client
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<h1>Hello!</h1>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
			
			if self.path.endswith("/hola"): #path refers to the url sent by the client
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>&#161Hola! <a href= '/hello' > Back to hello"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(output) #sent to client
				print output
				return
				
		except IOError :
			self.send_error(404, 'File Not Found: %s' % self.path)
			
	def do_POST(self):
		try:
			self.send_response(301) #sucessful post
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			ctype, pdict = cgi.parse_header(
				self.headers.getheader('content-type')) #harses the html header
			if ctype == 'multipart/form-data': #is it form data
				fields = cgi.parse_multipart(self.rfile, pdict) 
				messagecontent = fields.get('message') #pulls feild called message
			output = ""
			output += "<html><body>"
			output += " <h2> Okay, how about this: </h2>"
			output += "<h1> %s </h1>" % messagecontent[0]
			output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
			output += "</body></html>"
			self.wfile.write(output)
			print output
		except:
			pass

def main(): #instanciate server and specify port
	try:
		port = 8080
		server = HTTPServer(('', port), WebServerHandler) #host empty string? WebServerHandler-server instance
		print "Web Server running on port %s" % port
		server.serve_forever() #constantly listening
	except KeyboardInterrupt:
		print " ^C entered, stopping web server...."
		server.socket.close()

if __name__ == '__main__':
	main()