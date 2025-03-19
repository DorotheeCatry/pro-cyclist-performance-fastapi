from app.db.db_utils import get_db_connection, create_db
from app.core.security import get_password_hash
from faker import Faker
import random
import os

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
        get_password_hash("Password123"),
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
    sex = random.choice([0, 1])  # 0 = female, 1 = male
    
    first_name = fake.first_name_male() if sex == 1 else fake.first_name_female()
    last_name = fake.last_name()
    age = random.randint(22, 35)  # Age range more realistic for competitive cyclists
    
    # Define cyclist type
    cyclist_type = random.choices(["climber", "rouleur", "sprinter"], weights=[40, 40, 20])[0]
    
    # Height, weight, and VO2 max based on cyclist type and sex
    if cyclist_type == "climber":
        height = random.randint(165, 175) if sex == 1 else random.randint(155, 170)
        weight = round(random.uniform(55, 65), 1) if sex == 1 else round(random.uniform(45, 55), 1)
        vo2_max = random.randint(75, 90) if sex == 1 else random.randint(65, 85)
    elif cyclist_type == "rouleur":
        height = random.randint(175, 185) if sex == 1 else random.randint(165, 175)
        weight = round(random.uniform(70, 80), 1) if sex == 1 else round(random.uniform(55, 65), 1)
        vo2_max = random.randint(65, 80) if sex == 1 else random.randint(55, 75)
    else:  # Sprinter
        height = random.randint(180, 190) if sex == 1 else random.randint(170, 180)
        weight = round(random.uniform(75, 85), 1) if sex == 1 else round(random.uniform(60, 70), 1)
        vo2_max = random.randint(60, 75) if sex == 1 else random.randint(50, 65)
    
    return (user_id, sex, first_name, last_name, age, height, weight, vo2_max, cyclist_type)

def insert_athletes():
    """Insert athletes corresponding to the cyclists"""
    cursor.execute("SELECT id FROM user WHERE role = 1")
    cyclists = cursor.fetchall()
    
    athletes = [generate_realistic_cyclist(user_id) for (user_id,) in cyclists]
    
    cursor.executemany("""
        INSERT INTO athlete (user_id, sex, first_name, last_name, age, height, weight, VO2_max, cyclist_type) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, athletes)
    conn.commit()
    print("Information of 50 athletes inserted into the athlete table.")

def generate_realistic_test(athlete_id, sex, cyclist_type):
    """Generate a realistic test session for a given athlete"""
    cadence_range = {
        "climber": (90, 110),
        "rouleur": (85, 100),
        "sprinter": (80, 95)
    }
    ftp_range = {
        "climber": (250, 350) if sex == 1 else (200, 300),
        "rouleur": (300, 400) if sex == 1 else (250, 350),
        "sprinter": (400, 500) if sex == 1 else (320, 400)
    }
    
    cadence = round(random.uniform(*cadence_range[cyclist_type]), 1)
    ftp = random.randint(*ftp_range[cyclist_type])
    power_output = round(ftp * random.uniform(0.8, 1.2), 1)  # Use a percentage of FTP for power
    heart_rate = round(random.uniform(150, 200), 1) if sex == 1 else round(random.uniform(140, 190), 1)
    respiratory_frequency = round(random.uniform(30, 60), 1)
    vo2_measured = round(random.uniform(40, 90), 1)
    condition_rating = random.randint(1, 5)

    return (athlete_id, fake.date_this_month(), cadence, power_output, heart_rate, respiratory_frequency, vo2_measured, ftp, condition_rating)

def insert_test_sessions():
    """Insert 10 tests per athlete into the database"""
    cursor.execute("SELECT user_id, sex, cyclist_type FROM athlete")
    athletes = cursor.fetchall()
    
    test_sessions = [
        generate_realistic_test(user_id, sex, cyclist_type)
        for (user_id, sex, cyclist_type) in athletes
        for _ in range(10)
    ]
    
    cursor.executemany("""
        INSERT INTO test_session (athlete_id, date, cadence, power_output, heart_rate, respiratory_frequency, VO2, FTP, condition_rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, test_sessions)
    conn.commit()
    print("Each athlete has 10 tests recorded in the test_session table.")

def update_users_with_athlete_info():
    """Update the user table with first name, last name, and email from the athlete table"""
    
    cursor.execute("""
        SELECT athlete.user_id, athlete.first_name, athlete.last_name
        FROM athlete
        JOIN user ON athlete.user_id = user.id
    """)
    athletes = cursor.fetchall()

    updated_users = []
    for user_id, first_name, last_name in athletes:
        username = f"{first_name.capitalize()}{last_name.capitalize()}"
        email = f"{first_name.lower()}.{last_name.lower()}@gmail.com"
        
        updated_users.append((username, email, user_id))
    
    cursor.executemany("""
        UPDATE user
        SET username = ? , email = ?
        WHERE id = ?
    """, updated_users)
    
    conn.commit()
    print("User table has been updated with information from the athlete table.")
    
if __name__ == "__main__":
    if not os.path.exists("users.db"):
        create_db()
    if is_db_empty():
        insert_users()
        insert_athletes()
        insert_test_sessions()
        update_users_with_athlete_info()
    else:
        print("The database already contains data. No insertion performed.")
    
    conn.close()
