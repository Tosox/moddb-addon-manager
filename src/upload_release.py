import os
import moddb

def set_output(name, value):
    with open(os.getenv("GITHUB_OUTPUT"), 'a') as f:
        print(f"{name}={value}", file=f)

def main():
    username = os.getenv("MODDB_USERNAME")
    password = os.getenv("MODDB_PASSWORD")

    try:
        moddb.login(username, password)
    except ValueError as e:
        print(e)
        exit(1)

    print(f"Successfully logged-in as {username}")

if __name__ == '__main__':
    main()
