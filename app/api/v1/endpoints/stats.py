from app.db.db_utils import get_db_connection
from fastapi import APIRouter

router = APIRouter()

# Endpoint to get the most powerful athlete based on average power output
@router.get("/get_most_powerful")
def get_most_powerful():
    """
    Retrieve the most powerful athlete based on average power output.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            ts.athlete_id, 
            a.first_name, 
            a.last_name, 
            a.sex, 
            a.age, 
            a.height, 
            a.weight, 
            a.VO2_max, 
            a.FTP, 
            AVG(ts.power_output) AS AVG_POWER
        FROM test_session ts
        INNER JOIN athlete a ON a.user_id = ts.athlete_id
        GROUP BY athlete_id
        ORDER BY AVG_POWER DESC
        LIMIT 1;
    """
    cursor.execute(query)
    result = cursor.fetchone()    
    
    conn.close()
    
    if result:
        return {
            "athlete_id": result["athlete_id"],
            "first_name": result["first_name"],
            "last_name": result["last_name"],
            "sex": result["sex"],
            "age": result["age"],
            "height": result["height"],
            "weight": result["weight"],
            "VO2_max": result["VO2_max"],
            "FTP": result["FTP"],
            "AVG_POWER": result["AVG_POWER"]
        }
    return None

# Endpoint to get the athlete with the best VO2 max
@router.get("/get_best_VO2max")
def get_best_VO2max():
    """
    Retrieve the athlete with the highest VO2 max.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT *
        FROM athlete
        ORDER BY VO2_max DESC
        LIMIT 1;
    """
    cursor.execute(query)
    result = cursor.fetchone()    
    
    conn.close()
    
    if result:
        return {
            "user_id": result["user_id"],
            "first_name": result["first_name"],
            "last_name": result["last_name"],
            "sex": result["sex"],
            "age": result["age"],
            "height": result["height"],
            "weight": result["weight"],
            "FTP": result["FTP"],
            "VO2_max": result["VO2_max"],
        }
    return None

# Endpoint to get the athlete with the best power-to-weight ratio
@router.get("/get_best_power_to_weight")
def get_best_power_to_weight():
    """
    Retrieve the athlete with the best power-to-weight ratio.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            ts.athlete_id, 
            a.first_name, 
            a.last_name, 
            a.sex, 
            a.age, 
            a.height, 
            a.weight, 
            a.VO2_max, 
            a.FTP, 
            AVG(ts.power_output) AS avg_power
        FROM test_session ts
        INNER JOIN athlete a ON a.user_id = ts.athlete_id
        GROUP BY athlete_id
        ORDER BY avg_power DESC
        LIMIT 1;
    """
    cursor.execute(query)
    result = cursor.fetchone()    
    
    conn.close()
    
    if result:
        
        avg_power = result["avg_power"]
        weight = result["weight"]
        
        power_to_weight = (avg_power / weight) if weight > 0 else None
        
        return {
            "athlete_id": result["athlete_id"],
            "first_name": result["first_name"],
            "last_name": result["last_name"],
            "sex": result["sex"],
            "age": result["age"],
            "height": result["height"],
            "weight": result["weight"],
            "VO2_max": result["VO2_max"],
            "FTP": result["FTP"],
            "avg_power": result["avg_power"],
            "POWER_TO_WEIGHT": power_to_weight
        }
    return None
