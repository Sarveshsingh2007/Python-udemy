import random

# Print Hangman title art
print(r'''
 _                                             
| |                                            
| |__   __ _ _ __   __ _ _ __ ___   __ _ _ __  
| '_ \ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
| | | | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                    __/ |                      
                   |___/                       
''')

# List of hangman stages to visually represent lives left
stages = [r'''
     +---+
     |   |   
     O   |
    /|\  |
    / \  |
         |
    ========
''', r'''
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    ========
''', r'''
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    ========
''', r'''
     +---+
     |   |
     O   |
    /|   |
         |
         |
    ========
''', r'''
     +---+
     |   |
     O   |
     |   |
         |
         |
    ========
''', r'''
     +---+
     |   |
     O   |
         |
         |
         |
    ========
''', r'''
     +---+
     |   |
         |
         |
         |
         |
    ========
''']

# List of possible words to guess in the game
word_list = [
    "kawasaki", "sarvesh", "adhikari", "python", "variable",
    "function", "hangman", "looping", "developer", "keyboard",
    "internet", "compiler", "language", "software", "machine",
    "learning", "boolean", "integer", "recursion", "database"
]

lives = 6  # Number of incorrect guesses allowed

# Randomly choose a word from the list
chosen_word = random.choice(word_list)
print(chosen_word)  # DEBUG: Print the chosen word (you can remove this later)

# Create a placeholder string with underscores for each letter in the chosen word
placeholder = ""
word_length = len(chosen_word)
for position in range(word_length):
    placeholder += "_"
print(placeholder)  # Show the initial blank word

game_over = False  # Flag to control the game loop
correct_letter = []  # List to store letters guessed correctly so far

while not game_over:
    # Show lives left to the player (fixing the string format here)
    print(f"********************{lives}/6 LIVES LEFT**********************")
    
    guess = input("Guess a letter: ").lower()  # Get player's guess and convert to lowercase

    # Check if letter was already guessed
    if guess in correct_letter:
        print(f"You've already guessed {guess}")

    display = ""  # Will hold the current state of the word with guessed letters and underscores

    # Build the display string by checking each letter in the chosen word
    for letter in chosen_word:
        if letter == guess:
            display += letter
            # Add guessed letter to correct_letter list if not already added
            if guess not in correct_letter:
                correct_letter.append(guess)
        elif letter in correct_letter:
            display += letter
        else:
            display += "_"

    print("Word to guess: " + display)  # Show the player progress on the word

    # If the guessed letter is not in the word, reduce a life
    if guess not in chosen_word:
        lives -= 1
        print(f"You guessed {guess}, that's not in the word. You lose a life.")
        # If no lives left, game is over and player loses
        if lives == 0:
            game_over = True
            print(f"********************IT WAS {chosen_word.upper()}! YOU LOSE***********************")

    # If no underscores left in display, player has guessed all letters and wins
    if "_" not in display:
        game_over = True
        print("*******************YOU WIN************************")

    # Show current hangman stage based on remaining lives
    print(stages[lives])
