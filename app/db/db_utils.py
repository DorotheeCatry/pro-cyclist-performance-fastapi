import sqlite3

def create_db():    

    conn = sqlite3.connect('app/db/users.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    requetes = ["""CREATE TABLE IF NOT EXISTS user 
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    email TEXT UNIQUE,
    subscription_date DATE DEFAULT (DATE('now')),
    role INTEGER
    );""", 
    """CREATE TABLE IF NOT EXISTS athlete 
    (user_id INTEGER,    
    sex INTEGER CHECK(sex IN (0, 1)),
    first_name TEXT,
    last_name TEXT,
    age INTEGER,
    height INTEGER,
    weight REAL,
    VO2_max INT,
    FTP INT,    
    FOREIGN KEY(user_id) REFERENCES user(id)
    );""", 
    """CREATE TABLE IF NOT EXISTS test_session
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    athlete_id INTEGER,
    date DATE DEFAULT (DATE('now')),
    cadence REAL,
    power_output REAL,
    heart_rate REAL,
    respiratory_frequence REAL
    VO2 REAL,
    condition_rating INT CHECK(condition_rating BETWEEN 1 AND 5),
    FOREIGN KEY(athlete_id) REFERENCES athlete(user_id)
    );"""] # Requête SQL à executer

    for requete in requetes:
        cursor.execute(requete) # exécution de la requête avec les valeurs à insérer

    conn.commit() # Valide la transaction : utile pour les INSERT, UPDATE, DELETE
    conn.close() # Fermeture de la connexionCRETAE TABLE IF NO EXISTS
    
if __name__ == "__main__":
    create_db()