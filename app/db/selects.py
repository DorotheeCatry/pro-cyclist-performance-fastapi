from app.db.db_utils import get_db_connection

def get_athlete_sessions(athlete_id: int):
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM test_session WHERE athlete_id = ?"
    cursor.execute(query, (athlete_id, ))
    
    results = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return results


def get_athlete_by_id(athlete_id: int):
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    request = "SELECT * FROM athlete WHERE user_id = ?"
    cursor.execute(request, (athlete_id, ))
    results = dict(cursor.fetchone())
    
    conn.close()
    
    return results

def get_athlete_list():
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    request = """SELECT user_id, first_name, last_name 
    FROM user
    LEFT JOIN athlete
    ON id = user_id
    WHERE role = 1"""
    cursor.execute(request)
    results = cursor.fetchall()
    print(results)
    
    conn.close()
    
    return results




if __name__ == "__main__":
    print(get_athlete_sessions(1))