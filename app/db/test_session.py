from app.db.db_utils import get_db_connection

def create_session(athlete_id: int, data: dict) -> dict:
    
    result = {"status" : False, "message" : ""}
    
    conn = get_db_connection()
    cursor = conn.cursor() # Création d'un curseur

    try:
        # Create a new user based on the front-end data.
        requete = """INSERT INTO test_session (athlete_id, cadence, power_output, heart_rate, respiratory_frequency, VO2, condition_rating)
        VALUES (?, ?, ?, ?, ?, ?, ?);""" # Requête SQL à executer

        cursor.execute(requete, (athlete_id, data["cadence"], data["power_output"], data["heart_rate"], data["respiratory_frequency"], \
            data["VO2"], data["condition_rating"])) # exécution de la requête avec les valeurs à insérer
        
        conn.commit() # Valide la transaction : utile pour les INSERT, UPDATE, DELETE
        new_id = cursor.lastrowid
        conn.close() # Fermeture de la connexion
        
        result["status"] = True
        result["message"] = f"Session #{new_id} successfully created!"
        
    except ValueError as e:
        result["message"] = "Error during the creation of new session : " + str(e)
    except Exception as e:
        result["message"] = "Error during the creation of new session : " + str(e)
        
    return result

if __name__ == "__main__":
    
    # data = {"cadence": 0.0,
    #         "power_output": 0.0,
    #         "heart_rate": 0.0,
    #         "respiratory_frequency": 0.0,
    #         "VO2": 0.0,
    #         "condition_rating": 0}
    
    data = {"cadence": 1.2,
        "power_output": 1.6,
        "heart_rate": 0.7,
        "respiratory_frequency": 1.45,
        "VO2": 1.99,
        "condition_rating": 3}
    
    print(create_session(1, data)["message"])