import pandas

data = pandas.read_csv(r"udemy\day26\Quality_alphabet\qualities_alphabet.csv")
quality_dict = {row.letter:row.code for (index, row) in data.iterrows()}

word = input("Enter a word: ").upper()
output_list = [quality_dict[letter] for letter in word]
print(output_list)
