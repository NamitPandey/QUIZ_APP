import string
import random

def generate_random_password():

    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    ## length of password from the user
    length = 18

    ## shuffling the characters
    random.shuffle(characters)

    ## picking random characters from the list
    password = []
    for i in range(length):
        password.append(random.choice(characters))

    ## shuffling the resultant password
    random.shuffle(password)

    ## converting the list to string
    ## printing the list
    return "".join(password)
