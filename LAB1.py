print(f"Welcome to the age calculator!!")
answer = input(f"Would you like to know how old you will be in a particular year? (y/n)")
while not (answer == 'y' or answer == 'n'):
    print(f"Wrong answer use 'y' or 'n' ")
    answer = input(f"Would you like to know how old you will be in a particular year? (y/n)")

if answer == 'n':
    print(f"Thanks anyway!!")
elif answer == 'y':
    
    year = (input(f"In what year you were born? Please enter a 4 digit number"))   
    while not (year.isdigit()  == True and (len(year) == 4)):
        print(f"You made a mistake. Please enter your year of born correctly!!")
        year = (input(f"In what year you were born? Please enter a 4 digit number"))
        
    future = (input(f"In what year you want to know your age"))
    while not (future.isdigit() == True and (len(future) == 4) and (int(future) > int(year))):
        print(f"You made a mistake. Please enter the year you want to know your age correctly!!")
        future = (input(f"In what year you want to know your age"))
        
    age = int(future) - int(year)
    print(f"In the year {future}, you will have {age} years old.")
    print(f"Goodbye!!")

