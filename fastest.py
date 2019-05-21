try:
    f = open('www')
except FileNotFoundError:
    print("file does not exist")