# 📡 Morse Code Converter - Text Based Program

# Step 1: Morse Code Dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.',
    ' ': '/'  # Use / for space between words
}

# Step 2: Ask user for input
text = input("Enter a message to convert into Morse Code: ")

# Step 3: Convert text to Morse Code
morse_code = ""
for char in text.upper():      # Make input uppercase to match dict keys
    if char in MORSE_CODE_DICT:
        morse_code += MORSE_CODE_DICT[char] + " "
    else:
        morse_code += "? "  # unknown character placeholder

# Step 4: Display the result
print("\n📡 Morse Code Output:")
print(morse_code)
