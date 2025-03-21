from app.db.db_utils import get_db_connection
from app.schemas.schemas import ResponseData

def create_athlete(user_id: int) -> ResponseData:
    """
    Create a blank/default athlete.
    This function should never be called on its own. It is called automatically when a new user is created in the DB.
    """
    
    result = {"status" : False, "message" : ""}
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
                
        query = """INSERT INTO athlete (user_id, sex, first_name, last_name, age, height, weight, VO2_max, FTP) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""

        cursor.execute(query, (user_id, 0, "John/Jane", "Doe", 18, 160, 60, 0, 0))
        
        conn.commit()
        
        result["status"] = True
        result["message"] = f"Athlete n°{user_id} successfully created!"
        
    except ValueError as e:
        result["message"] = "Error during the creation of new athlete : " + str(e)
    except Exception as e:
        result["message"] = "Error during the creation of new athlete : " + str(e)
    finally:
        conn.close()
        
    return result

def modify_athlete(id: int, data: dict) -> dict:
    
    """
    Modify an athlete's entry in the database.
    id : the user_id or athlete_id of selected athlete.
    data : should contains every info of the athlete, even those that won't be modified.
    """
    
    result = {"status" : False, "message" : ""}
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:        
        query = """UPDATE athlete SET
        sex = ?, 
        first_name = ?,
        last_name = ?, 
        age = ?, 
        height = ?, 
        weight = ?, 
        VO2_max = ? 
        WHERE user_id = ?;"""

        cursor.execute(query, (data["sex"], data["first_name"], data["last_name"], data["age"], data["height"],data["weight"],\
            data["VO2_max"], id))

        query = """SELECT username FROM user WHERE id = ?"""
        cursor.execute(query, (id, ))
        username = cursor.fetchone()["username"]
        
        conn.commit() 
        
        result["status"] = True
        result["message"] = f"User {username} successfully updated!"
        
    except ValueError as e:
        result["message"] = "Value error during the modification of user infos : " + str(e)
    except Exception as e:
        result["message"] = "Exception error during the modification of user infos : " + str(e)
    finally:
        conn.close() 
    
    return result

# if __name__ == "__main__":
#     # data = {"username": "",
#     #         "password": "",
#     #         "email": "",
#     #         "role": 0}
    
#     data = {"username": "Destructor",
#             "password": "supersecretpassword",
#             "email": "mail@mail.fr",
#             "role": 0}
    
#     print(create_athlete(data)["message"])
    
#         # data = {"sex": 0,
#     #         "first_name": "",
#     #         "last_name": "",
#     #         "age": 0,
#     #         "height": 0,
#     #         "weight": 0.0,
#     #         "VO2_max": 0,
#     #         "FTP": 0}
    
#     data = {"sex": 1,
#         "first_name": "Samuel",
#         "last_name": "Thorez",
#         "age": 31,
#         "height": 185,
#         "weight": 80.6,
#         "VO2_max": 4000,
#         "FTP": 100}
    
#     print(modify_athlete(1, data)["message"])