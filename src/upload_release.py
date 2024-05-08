import os
import moddb

def set_output(name, value):
    with open(os.getenv("GITHUB_OUTPUT"), 'a') as f:
        print(f"{name}={value}", file=f)

def assert_required(var, msg):
    if not var:
        with open(os.getenv("GITHUB_OUTPUT"), 'a') as f:
            print(f"::error title=Error::{msg}", file=f)
        exit(1)

def main():
    username = os.getenv("MODDB_USERNAME")
    assert_required(username, "Missing required input 'MODDB_USERNAME'")

    password = os.getenv("MODDB_PASSWORD")

    try:
        moddb.login(username, password)
    except ValueError as e:
        print(f"Login failed for user {username}")
        exit(1)

    print(f"Successfully logged-in as {username}")

if __name__ == '__main__':
    main()
