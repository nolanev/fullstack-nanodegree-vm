from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi #common gatway interface

from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()




class WebServerHandler(BaseHTTPRequestHandler): #tells what code to excute based on the http request
# extends BaseHTTPRequestHandler
	def do_GET(self):
		try:
			if self.path.endswith('/restaurants'):
				restaurants = session.query(Restaurant).all()
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = "<html><body>"				
				for restaurant in restaurants:
					output+=restaurant.name
					output += "<a href ='restaurants/%s/edit' >Edit </a>" %restaurant.id
					output+= "<a href= 'restaurants/%s/delete' > Delete </a>"	 %restaurant.id
					output+="<br><br>"
				output+="<a href= 'restaurants/new' >New Restaurant </a>"
				output+="</html></body>"
				self.wfile.write(output)
				print(output)
				return
			if self.path.endswith("edit"): 
				restaurantId=self.path.split("/")[2]
				myRestaurant=session.query(Restaurant).filter_by(id=restaurantId).one()
				if myRestaurant:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = "<body><html>"	
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'> " %restaurantId
					output += "<h2>Enter new name</h2><input name='newRestaurantName' type='text' placeholder='%s' >" %myRestaurant.name
					output += "<input type='submit' value='Rename'> </form>"
					output += "</body></html>"
					self.wfile.write(output)
					
					
			if self.path.endswith("/delete"): 
				restaurantId=self.path.split("/")[2]
				myRestaurant=session.query(Restaurant).filter_by(id=restaurantId).one()
				if myRestaurant:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = ""
					output += "<html><body>"
					output += "<h1>Are you sure you want to delete %s?" % myRestaurant.name
					output += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" % restaurantId
					output += "<input type = 'submit' value = 'Delete'>"
					output += "</form>"
					output += "</body></html>"
					self.wfile.write(output)
					
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Make a New Restaurant</h1>"
				output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
				output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
				output += "<input type='submit' value='Create'>"
				output += "</form></html></body>"
				self.wfile.write(output)
			
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
			if self.path.endswith("/restaurants"): #path refers to the url sent by the client
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
			
			
				
		except IOError :
			self.send_error(404, 'File Not Found: %s' % self.path)
			
	def do_POST(self):
		try:
			if self.path.endswith("/delete"): 
				restaurantId=self.path.split("/")[2]
				myRestaurant=session.query(Restaurant).filter_by(id=restaurantId).one()
				if myRestaurant:
					session.delete(myRestaurant)
					session.commit()
					self.send_response(301) #sucessful post
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()
					
			if self.path.endswith("edit"): 
				restaurantId=self.path.split("/")[2]
				myRestaurant=session.query(Restaurant).filter_by(id=restaurantId).one()
				ctype, pdict = cgi.parse_header(
				self.headers.getheader('content-type')) 
				if ctype == 'multipart/form-data': 
					fields = cgi.parse_multipart(self.rfile, pdict) 
					messagecontent = fields.get('newRestaurantName') 
				
				if myRestaurant  != []:
					myRestaurant.name=messagecontent[0]
					session.add(myRestaurant)
					session.commit()
					self.send_response(301) #sucessful post
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()
			
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(
				self.headers.getheader('content-type')) 
				if ctype == 'multipart/form-data': 
					fields = cgi.parse_multipart(self.rfile, pdict) 
					messageContent = fields.get('newRestaurantName') 
				restaurant1 = Restaurant(name=messageContent[0])
				session.add(restaurant1)
				session.commit()
				self.send_response(301) #sucessful post
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()
				
			
			
			
			if self.path.endswith("/hola"):
				self.send_response(301) #sucessful post
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type')) #parses the html header
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