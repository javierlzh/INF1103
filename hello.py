print("=======================")
print("Welcome here")
print("My first post!")
print("=======================")

username = input("Enter your username: ")
age = int(input("Enter your age: "))
category = input("Enter Content Category: ")

print("\nInstagram Profile")
print("=======================")
print("Username: ", username)
print("Age: ", age)
print("Category: ", category)

if age>40 and category == 'fun':
    print("You are old what is fun for you?")