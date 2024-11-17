import os

# Create the CapturedImages/Converted directory if it doesn't exist
converted_dir = 'CapturedImages/Converted'
if not os.path.exists(converted_dir):
	os.makedirs(converted_dir)  # Make the directory if it's not already there

def list_screenshot_files():
	# Get a list of all .txt files in the CapturedImages directory that contain "screenshot" in their name
	files = [f for f in os.listdir('CapturedImages') if f.endswith('.txt') and 'screenshot' in f]
	return files  # Return the list of screenshot files

def read_image_from_file(input_file, output_image_file):
	# Read the raw binary data from the specified text file
	with open(input_file, 'rb') as file:
		img_data = file.read()  # Read the binary data

	# Save the binary data to a new PNG file
	with open(output_image_file, 'wb') as img_file:
		img_file.write(img_data)  # Write the binary data to the new file

	print(f'Image saved as {output_image_file}')  # Confirm the image has been saved

def convert_all_files(screenshot_files):
	# Convert each screenshot file to a PNG format
	for filename in screenshot_files:
		output_file = os.path.join(converted_dir, f'CONVERTED_{filename[:-4]}.png')  # Prepare the output file name
		input_file = os.path.join('CapturedImages', filename)  # Get the full input file path
		if os.path.exists(output_file):
			print(f'{output_file} already exists. Skipping conversion.')  # Skip if the file already exists
		else:
			read_image_from_file(input_file, output_file)  # Convert the file

def main():
	# Main loop to handle user interaction
	while True:
		screenshot_files = list_screenshot_files()  # Get the list of screenshot files
		
		if not screenshot_files:
			print('No screenshot files found.')  # Inform the user if no files are available
			return

		# Display the list of files and their conversion status
		print('\nSelect a screenshot file to convert (or \'a\' to convert all, or \'0\' to exit):')
		for index, filename in enumerate(screenshot_files, start=1):
			output_file = os.path.join(converted_dir, f'CONVERTED_{filename[:-4]}.png')  # Prepare output filename
			converted_status = '[CONVERTED]' if os.path.exists(output_file) else '[UNCONVERTED]'  # Check conversion status
			print(f'{index}. {filename} {converted_status}')  # Display each file with its status

		# Get user input for file selection
		choice = input('Enter the number of the file you want to convert (or \'a\' to convert all, or \'0\' to exit): ').strip()
		
		if choice.lower() == '0':
			print('Exiting the program.')  # Exit the program if user chooses 0
			break
		elif choice.lower() == 'a':
			convert_all_files(screenshot_files)  # Convert all files if user chooses 'a'
		else:
			try:
				choice = int(choice)  # Try converting user input to an integer
				if choice < 1 or choice > len(screenshot_files):
					raise ValueError('Invalid choice.')  # Validate the user choice
				
				selected_file = screenshot_files[choice - 1]  # Get the selected file
				output_file = os.path.join(converted_dir, f'CONVERTED_{selected_file[:-4]}.png')  # Prepare output path
				input_file = os.path.join('CapturedImages', selected_file)  # Complete input file path

				if os.path.exists(output_file):
					print(f'{output_file} already exists. Skipping conversion.')  # Skip if already converted
				else:
					read_image_from_file(input_file, output_file)  # Convert the selected file

			except ValueError as e:
				print(f'Error: {e}. Please enter a valid number.')  # Handle invalid input

if __name__ == '__main__':
	main()  # Run the main function