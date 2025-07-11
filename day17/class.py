class User:     # PascalCase
    def __init__(self, user_id, username):
        # print("new user being created...")
        self.id = user_id
        self.username = username
        self.followers = 0


# user_1 = User()    
# user_1.id = "001"  # attribute is a variable that associated with object
# user_1.username = "sarvesh" 
# print(user_1.id)


user_1 = User("001", "sarvesh")
user_2 = User("002", "adhikari")

# print(user_1.id)
# print(user_2.username)
print(user_1.followers)
