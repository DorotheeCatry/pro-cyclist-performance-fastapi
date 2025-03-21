from app.db.db_utils import get_db_connection

def create_session(athlete_id: int, data: dict):
    """
    Create a new training session.
    athlete_id : id of the athlete associated with the session.
    data : should contains every necessary informations from session.
    """
    
    
    result = {"status" : False, "message" : ""}
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """INSERT INTO test_session (athlete_id, cadence, power_output, heart_rate, respiratory_frequency, VO2, FTP, condition_rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""

        cursor.execute(query, (athlete_id, data["cadence"], data["power_output"], data["heart_rate"], data["respiratory_frequency"], \
            data["VO2"], data["FTP"], data["condition_rating"]))
        
        conn.commit() 
        new_id = cursor.lastrowid
        
        result["status"] = True
        result["message"] = f"Session #{new_id} successfully created!"
        
    except ValueError as e:
        result["message"] = "Error during the creation of new session : " + str(e)
    except Exception as e:
        result["message"] = "Error during the creation of new session : " + str(e)
    finally:
        conn.close()
    
    return result

# if __name__ == "__main__":
    
#     # data = {"cadence": 0.0,
#     #         "power_output": 0.0,
#     #         "heart_rate": 0.0,
#     #         "respiratory_frequency": 0.0,
#     #         "VO2": 0.0,
#     #         "condition_rating": 0}
    
#     data = {"cadence": 1.2,
#         "power_output": 1.6,
#         "heart_rate": 0.7,
#         "respiratory_frequency": 1.45,
#         "VO2": 1.99,
#         "condition_rating": 3}
    
#     print(create_session(1, data)["message"])