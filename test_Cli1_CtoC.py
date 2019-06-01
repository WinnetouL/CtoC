print("something", __name__)

def main():
    print("morjen")
    print(__name__)

if __name__ == "__main__":
    main()
else:
    print("__name__ doesn't equal __main__")