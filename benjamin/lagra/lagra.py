import json,os,time

def display_menu_no_logon():
    print("\nVälkommen till Lagra™!\n")
    print("Vad vill du göra?")
    print("1. Logga in")
    print("2. Registrera användare")
    print("3. Avsluta\n")

def display_menu_logged_on(logged_in_user):
    print("\nVälkommen till Lagra™, " + logged_in_user + "!\n")
    print("1. Se lagrade objekt")
    print("2. Lägg till objekt")
    print("3. Logga ut\n")

def get_number_input(min, max, message):
    valid_input = False

    while valid_input == False:
        try:
            user_input = input(message)
            
            user_input_converted = int(user_input)

            if(user_input_converted >= min and user_input_converted <= max):
                valid_input = True
        except:
            print("Invalid input")

    return user_input_converted

def load_users():
    try:
        users_file = open("C:\\Users\\benja\\OneDrive\\Dokument\\Skola\\M5\\skoluppgifter\\benjamin\\lagra\\users.json", "r")
        users_data = users_file.read()
        users_file.close()

        if users_data.strip() == "":
            users = []
        else:
            users = json.loads(users_data)
            if(type(users) is not list):
                users = [users]
    except:
        users = []

    return users

def register_user(current_users, stored_items):
    print("\n=== Registrera användare ===\n")

    username_exists = True

    while username_exists:
        username = input("Användarnamn: ")
        username_exists = False
        
        for user in current_users:
            if user['username'] == username:
                print("\nAnvändarnamnet är upptaget.")
                username_exists = True
                break

    password = input("Lösenord: ")

    user = {
        'username': username,
        'password': password
    }

    current_users.append(user)
    users_json = json.dumps(current_users, indent=4)
    
    users_file = open("C:\\Users\\benja\\OneDrive\\Dokument\\Skola\\M5\\skoluppgifter\\benjamin\\lagra\\users.json", "w")
    users_file.write(users_json)
    users_file.close()

    stored_items.append({
        "username": username,
        "items": []
    })
    items_json = json.dumps(stored_items, indent=4)
    items_file = open("C:\\Users\\benja\\OneDrive\\Dokument\\Skola\\M5\\skoluppgifter\\benjamin\\lagra\\items.json", "w")
    items_file.write(items_json)
    items_file.close()

    print("\nAnvändare registrerad!")

    time.sleep(1.5)

def login(users):
    stop = False

    while(stop == False):
        print("\n=== Logga in ===\n")
        username = input("Användarnamn: ")
        password = input("Lösenord: ")

        for user in users:
            if(user["username"] == username and user["password"] == password):
                print("\nInloggad som " + username + "!")
                time.sleep(1.5)

                return username

        print("\nFel användarnamn eller lösenord.\n")
        print("1. Försök igen")
        print("2. Gå tillbaka\n")

        choice = get_number_input(1,2, "Val: ")

        if(choice == 2):
            stop = True

    return None

def load_stored_items():
    try:
        items_file = open("C:\\Users\\benja\\OneDrive\\Dokument\\Skola\\M5\\skoluppgifter\\benjamin\\lagra\\items.json", "r")
        items_data = items_file.read()
        items_file.close()

        if items_data.strip() == "":
            items = []
        else:
            items = json.loads(items_data)
            if(type(items) is not list):
                items = [items]
    except:
        items = []

    return items

def add_stored_item(stored_items, logged_on_user):
    object_names = input("Vad ska lagras?: ")
    object_list = [obj.strip() for obj in object_names.split(',')]

    for items in stored_items:
        if items["username"] == logged_on_user:
            user_items = items["items"]
            break
    else:
        user_items = []
        stored_items.append({
            "username": logged_on_user,
            "items": user_items
        })

    user_items.extend(object_list)

    items_file = open("C:\\Users\\benja\\OneDrive\\Dokument\\Skola\\M5\\skoluppgifter\\benjamin\\lagra\\items.json", "w")
    stored_items_json = json.dumps(stored_items, indent=4)
    items_file.write(stored_items_json)
    items_file.close()

def view_stored_items(stored_items, logged_on_user):
    for items in stored_items:
        if items["username"] == logged_on_user:
            user_items = items["items"]
            break
    else:
        user_items = []

    if user_items:
        print("\nDina lagrade objekt:")
        for item in user_items:
            print("- " + item)
    else:
        print("\nInga objekt lagrade.")
    input("\nTryck på Enter för att fortsätta...")

def main():
    users = load_users()
    logged_in_user = None
    stored_items = load_stored_items()

    quit = False
    
    while(quit == False):
        os.system('cls')

        if logged_in_user:
            display_menu_logged_on(logged_in_user)

            choice = get_number_input(1,3, "Val: ")

            if(choice == 1):
                view_stored_items(stored_items, logged_in_user)

            if(choice == 2):
                add_stored_item(stored_items, logged_in_user)

            if(choice == 3):
                logged_in_user = None
    
        else:
            display_menu_no_logon()
            choice = get_number_input(1,3, "Val: ")

            if(choice == 1):
                logged_in_user = login(users)

            if(choice == 2):
                register_user(users, stored_items)
            
            elif(choice == 3):
                quit = True

main()
