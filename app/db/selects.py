from app.db.db_utils import get_db_connection

def get_athlete_sessions(athlete_id: int):
    
    conn = get_db_connection()
    cursor = conn.cursor() # Création d'un curseur
    
    query = "SELECT * FROM test_session WHERE athlete_id = ?"
    cursor.execute(query, (athlete_id, ))
    
    results = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return results

if __name__ == "__main__":
    print(get_athlete_sessions(1))