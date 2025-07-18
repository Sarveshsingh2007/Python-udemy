# with open("my_file.txt") as file:
#     content = file.read()
#     print(content)


with open("my_file.txt", mode="w") as file: # in write mode if file doesn't exit the file will be created automatically.
    file.write("New txt.")

    # list.append("\n New txt.")
