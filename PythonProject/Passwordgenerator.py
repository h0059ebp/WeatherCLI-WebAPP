import random, string

passwordlentgth = int(input("Enter the length of the password: "))
random_string = ''.join(random.choice(string.ascii_letters) for _ in range(passwordlentgth))
print(random_string)  # e.g. 'aKdLmNpQrT'

print("Hello World")
print(23+22)