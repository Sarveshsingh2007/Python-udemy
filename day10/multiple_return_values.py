def format_name(f_name, l_name):
    if f_name == "" or l_name == "":
        return
    
    formated_f_name = f_name.title()
    formated_l_name = l_name.title()

    return f"Result: {formated_f_name} {formated_l_name}"
    # print("sarveshsingh9381@gmail.com") this will not print because return is the last statement of program

print(format_name(input("What is your first name?: "), input("What is your last name?: ")))