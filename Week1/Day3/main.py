from api import fetch_user

def main():
    user = fetch_user(1)

    if user:
        print("User fetched from API:")
        print(f"Name : {user['name']}")
        print(f"Email: {user['email']}")
        print(f"City : {user['address']['city']}")
    else:
        print("Failed to fetch user data")

if __name__ == "__main__":
    main()