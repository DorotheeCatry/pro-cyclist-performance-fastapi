from app.db.db_utils import get_db_connection

def get_athlete_sessions(athlete_id: int):
    
    conn = get_db_connection()
    cursor = conn.cursor() # Création d'un curseur
    
    requete = "SELECT * FROM test_session WHERE athlete_id = ?"
    cursor.execute(requete, (athlete_id, ))
    
    results = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return results

def get_athlete_by_id(athlete_id: int):
    
    conn = get_db_connection()
    cursor = conn.cursor() # Création d'un curseur
    
    requete = "SELECT * FROM athlete WHERE user_id = ?"
    cursor.execute(requete, (athlete_id, ))
    
    results = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return results




if __name__ == "__main__":
    print(get_athlete_sessions(1))