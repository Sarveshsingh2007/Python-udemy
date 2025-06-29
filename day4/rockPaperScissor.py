import random

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''   
     _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

game_images = [rock, paper, scissors]

while True:
    user_input = input("What do you choose? Type 0 for Rock, 1 for Paper, 2 for Scissors or 'q' to quit: ")

    if user_input.lower() == 'q':
        print("Thanks for playing! Goodbye.")
        break

    if user_input not in ['0', '1', '2']:
        print("Invalid input. Please enter 0, 1, 2 or 'q'.\n")
        continue

    user_choice = int(user_input)
    computer_choice = random.randint(0, 2)

    print("\nYou chose:")
    print(game_images[user_choice])

    print("Computer chose:")
    print(game_images[computer_choice])

    if user_choice == computer_choice:
        print("It's a draw!\n")
    elif (user_choice == 0 and computer_choice == 2) or \
         (user_choice == 1 and computer_choice == 0) or \
         (user_choice == 2 and computer_choice == 1):
        print("You win!\n")
    else:
        print("You lose!\n")
