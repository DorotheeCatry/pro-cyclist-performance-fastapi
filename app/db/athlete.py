from app.db.db_utils import get_db_connection

def create_athlete(user_id: int) -> dict:
    
    result = {"status" : False, "message" : ""}
    
    conn = get_db_connection()
    cursor = conn.cursor() # Création d'un curseur

    try:
                
        requete = """INSERT INTO athlete (user_id, sex, first_name, last_name, age, height, weight, VO2_max, FTP) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""" # Requête SQL à executer

        cursor.execute(requete, (user_id, 0, "John/Jane", "Doe", 18, 160, 60, 0, 0)) # exécution de la requête avec les valeurs à insérer
        
        conn.commit() # Valide la transaction : utile pour les INSERT, UPDATE, DELETE
        
        result["status"] = True
        result["message"] = f"Athlete n°{user_id} successfully created!"
        
    except ValueError as e:
        result["message"] = "Error during the creation of new athlete : " + str(e)
    except Exception as e:
        result["message"] = "Error during the creation of new athlete : " + str(e)
    finally:
        conn.close() # Fermeture de la connexion
        
    return result

def modify_athlete(id: int, data: dict) -> dict:
    
    result = {"status" : False, "message" : ""}
    
    conn = get_db_connection()
    cursor = conn.cursor() # Création d'un curseur

    try:        
        requete = """UPDATE athlete SET
        sex = ?, 
        first_name = ?,
        last_name = ?, 
        age = ?, 
        height = ?, 
        weight = ?, 
        VO2_max = ?, 
        FTP = ?
        WHERE user_id = ?;""" # Requête SQL à executer

        cursor.execute(requete, (data["sex"], data["first_name"], data["last_name"], data["age"], data["height"],data["weight"],\
            data["VO2_max"], data["FTP"], id)) # exécution de la requête avec les valeurs à insérer

        requete = """SELECT username FROM user WHERE id = ?"""
        cursor.execute(requete, (id, ))
        username = cursor.fetchone()["username"]
        
        conn.commit() # Valide la transaction : utile pour les INSERT, UPDATE, DELETE
        
        result["status"] = True
        result["message"] = f"User {username} successfully updated!"
        
    except ValueError as e:
        result["message"] = "Error during the creation of new user : " + str(e)
    except Exception as e:
        result["message"] = "Error during the creation of new user : " + str(e)
    finally:
        conn.close() # Fermeture de la connexion
    
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
    
    print(create_athlete(data)["message"])
    
        # data = {"sex": 0,
    #         "first_name": "",
    #         "last_name": "",
    #         "age": 0,
    #         "height": 0,
    #         "weight": 0.0,
    #         "VO2_max": 0,
    #         "FTP": 0}
    
    data = {"sex": 1,
        "first_name": "Samuel",
        "last_name": "Thorez",
        "age": 31,
        "height": 185,
        "weight": 80.6,
        "VO2_max": 4000,
        "FTP": 100}
    
    print(modify_athlete(1, data)["message"])