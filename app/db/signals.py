import random
from faker import Faker
from db_utils import get_db_connection

# Initialize Faker
fake = Faker()

# Connect to the database
conn = get_db_connection()
cursor = conn.cursor()

def is_db_empty():
    """Check if the user table is empty"""
    cursor.execute("SELECT COUNT(*) FROM user")
    return cursor.fetchone()[0] == 0

def generate_user(role):
    """Generate a user with a defined role (0 = coach, 1 = cyclist)"""
    return (
        fake.user_name(),
        "Password123",
        fake.unique.email(),
        role
    )

def insert_users():
    """Insert 50 cyclists and 2 coaches into the database"""
    users = [generate_user(0) for _ in range(2)]  # 2 coaches
    users += [generate_user(1) for _ in range(50)]  # 50 cyclists
    
    cursor.executemany("""
        INSERT INTO user (username, password, email, role) 
        VALUES (?, ?, ?, ?)
    """, users)
    conn.commit()
    print("50 cyclists and 2 coaches inserted into the user table.")

def generate_realistic_cyclist(user_id):
    """Generate an athlete with realistic physiological data"""

    sex = random.choice([0, 1])
    
    if sex == 1:
        first_name = fake.first_name_male()
    else:
        first_name = fake.first_name_female()

    last_name = fake.last_name()
    
    age = random.randint(22, 35)
    
    if sex == 1:  # Homme
        height = random.randint(170, 190)
        weight = round(random.uniform(60, 80), 1)
        vo2_max = random.randint(65, 85)
        if weight <= 68:
            FTP = random.randint(320, 400)
        else:  
            FTP = random.randint(400, 500)
    else:  # Femme
        height = random.randint(160, 175)
        weight = round(random.uniform(50, 65), 1)
        vo2_max = random.randint(55, 75)
        if weight <= 58:
            FTP = random.randint(250, 330)
        else:
            FTP = random.randint(330, 380)
    
    return (user_id, sex, first_name, last_name, age, height, weight, vo2_max, FTP)

def insert_athletes():
    """Insert athletes corresponding to the cyclists"""
    cursor.execute("SELECT id FROM user WHERE role = 1")
    cyclists = cursor.fetchall()
    
    athletes = [generate_realistic_cyclist(user_id) for (user_id,) in cyclists]
    
    cursor.executemany("""
        INSERT INTO athlete (user_id, sex, first_name, last_name, age, height, weight, VO2_max, FTP) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, athletes)
    conn.commit()
    print("Information of 50 athletes inserted into the athlete table.")

def generate_realistic_test(athlete_id, sex):
    """Generate a realistic test session for a given athlete"""
    cadence = round(random.uniform(85, 110), 1) if sex == 1 else round(random.uniform(85, 105), 1)
    power_output = round(random.uniform(300, 500), 1) if sex == 1 else round(random.uniform(250, 400), 1)
    heart_rate = round(random.uniform(150, 200), 1) if sex == 1 else round(random.uniform(140, 190), 1)
    respiratory_frequency = round(random.uniform(30, 60), 1)
    vo2_measured = round(random.uniform(40, 90), 1)
    condition_rating = random.randint(1, 5)
    
    return (athlete_id, fake.date_this_decade(), cadence, power_output, heart_rate, respiratory_frequency, vo2_measured, condition_rating)

def insert_test_sessions():
    """Insert 5 tests per athlete into the database"""
    cursor.execute("SELECT user_id, sex FROM athlete")
    athletes = cursor.fetchall()
    
    test_sessions = [
        generate_realistic_test(user_id, sex)
        for (user_id, sex) in athletes
        for _ in range(5)
    ]
    
    cursor.executemany("""
        INSERT INTO test_session (athlete_id, date, cadence, power_output, heart_rate, respiratory_frequency, VO2, condition_rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, test_sessions)
    conn.commit()
    print("Each athlete has 5 tests recorded in the test_session table.")

if __name__ == "__main__":
    if is_db_empty():
        insert_users()
        insert_athletes()
        insert_test_sessions()
    else:
        print("The database already contains data. No insertion performed.")
    
    conn.close()
