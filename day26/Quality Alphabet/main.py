import pandas

data = pandas.read_csv(r"udemy\day26\Quality_alphabet\qualities_alphabet.csv")
quality_dict = {row.letter:row.code for (index, row) in data.iterrows()}

def generate_quality():
  word = input("Enter a word: ").upper()
  try:
    output_list = [quality_dict[letter] for letter in word]
  except KeyError:
    print("Sorry, only letters in the alphabet please.")
    generate_quality()
  else:
    print(output_list)
generate_quality()
