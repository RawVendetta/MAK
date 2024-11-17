def translate_keystrokes(input_file):
    # Define a mapping for special keys, including left and right variations
    key_mapping = {
        "Key.space": " ",  # Replace with a space
        "Key.up": " [Up] ",
        "Key.down": " [Down] ",
        "Key.left": " [Left] ",
        "Key.right": " [Right] ",
        "Key.ctrl": " [Ctrl] ",
        "Key.alt": " [Alt] ",
        "Key.alt_l": " [Alt] ",  # Map left Alt
        "Key.alt_r": " [Alt] ",  # Map right Alt
        "Key.shift": " [Shift] ",
        "Key.shift_l": " [Shift] ",  # Map left Shift
        "Key.shift_r": " [Shift] ",  # Map right Shift
        "Key.enter": "\n",  # Newline for Enter key
        "Key.cmd": " [Cmd] ",  # Command key
        "Key.cmd_l": " [Cmd] ",  # Left Command key
        "Key.cmd_r": " [Cmd] ",  # Right Command key
        "Key.tab": " [Tab] ",  # Tab key
    }

    result = []

    # Read the input file
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading and trailing spaces
            if line in key_mapping:
                # Replace using mapping for special keys
                result.append(key_mapping[line])
            elif line:
                # Add regular characters directly, without quotes
                result.append(line.strip())  # Ensure no leading/trailing spaces

    # Join the list into a single string without any additional characters
    readable_string = ''.join(result).replace("'", "").replace('"', "").strip()  # Combine all parts into a single string and trim any extra spaces

    return readable_string

def main():
    input_file = "received_data.log"  # Defined file where keystrokes are logged
    
    translated_string = translate_keystrokes(input_file)  # Use defined function to parse log file
    print(f"\nTranslated String:\n{translated_string}\n")  # Print translated log file

if __name__ == "__main__":
    main()