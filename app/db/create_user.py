import sqlite3

def create_user(data: dict) -> dict:
    
    result = {"status" : False, "message" : ""}
    
    conn = sqlite3.connect('app/db/users.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    try:
        # Create a new user based on the front-end data.
        requete = """INSERT INTO user (username, password, email, role) VALUES (?, ?, ?, ?);""" # Requête SQL à executer

        cursor.execute(requete, (data["username"], data["password"], data["email"], data["role"])) # exécution de la requête avec les valeurs à insérer
        
        requete = """INSERT INTO athlete (user_id, sex, first_name, last_name, age, height, weight, VO2_max, FTP) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""" # Requête SQL à executer

        cursor.execute(requete, (cursor.lastrowid, 0, "John/Jane", "Doe,", 18, 160, 60, 0, 0)) # exécution de la requête avec les valeurs à insérer

        conn.commit() # Valide la transaction : utile pour les INSERT, UPDATE, DELETE
        conn.close() # Fermeture de la connexion
        
        result["status"] = True
        result["message"] = f"User {data["username"]} successfully created!"
        
    except ValueError as e:
        result["message"] = "Error during the creation of new user :\n" + str(e)
    
    return result

if __name__ == "__main__":
    # data = {"username": "",
    #         "password": "",
    #         "email": "",
    #         "role": 0}
    
    data = {"username": "Destructor",
            "password": "supersecretpassword",
            "email": "mail@mail.fr",
            "role": 0}
    
    print(create_user(data)["message"])