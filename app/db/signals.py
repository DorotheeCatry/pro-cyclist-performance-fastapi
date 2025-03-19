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
    
    if sex == 1:
        first_name = fake.first_name_male()
    else:
        first_name = fake.first_name_female()

    last_name = fake.last_name()
    
    age = random.randint(22, 35)  # Age range more realistic for competitive cyclists
    
    # Height and weight based on specific data for men and women
    if sex == 1:  # Male
        height = random.randint(170, 190)
        weight = round(random.uniform(60, 85), 1)
        vo2_max = random.randint(65, 85)  # VO2 max for men
        if weight <= 65:  # Climber
            FTP = random.randint(320, 400)
        elif weight <= 75:  # All-rounder
            FTP = random.randint(370, 460)
        else:  # Sprinter
            FTP = random.randint(440, 500)
    else:  # Female
        height = random.randint(160, 175)
        weight = round(random.uniform(50, 70), 1)
        vo2_max = random.randint(55, 75)  # VO2 max for women
        if weight <= 55:  # Climber
            FTP = random.randint(250, 320)
        elif weight <= 65:  # All-rounder
            FTP = random.randint(290, 360)
        else:  # Sprinter
            FTP = random.randint(330, 380)

    # Adjust FTP based on age, younger athletes will have a higher FTP
    # Older athletes (around 35 years old) may see their FTP slightly decrease.
    if age > 30:
        FTP -= random.randint(10, 30)  # FTP penalty for older athletes
    
    # Adding some other factors like VO2 max and height
    FTP += (vo2_max - 60) * 2  # Adjust based on VO2 max (higher = better performance)
    if height > 180:
        FTP += 10  # A taller cyclist may have better muscle development

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

def generate_realistic_test(athlete_id, sex, FTP):
    """Generate a realistic test session for a given athlete"""
    cadence = round(random.uniform(85, 110), 1) if sex == 1 else round(random.uniform(85, 105), 1)
    power_output = round(FTP * random.uniform(0.8, 1.2), 1)  # Use a percentage of FTP for power
    heart_rate = round(random.uniform(150, 200), 1) if sex == 1 else round(random.uniform(140, 190), 1)
    respiratory_frequency = round(random.uniform(30, 60), 1)
    vo2_measured = round(random.uniform(40, 90), 1)
    condition_rating = random.randint(1, 5)

    return (athlete_id, fake.date_this_month(), cadence, power_output, heart_rate, respiratory_frequency, vo2_measured, condition_rating)

def insert_test_sessions():
    """Insert 5 tests per athlete into the database"""
    cursor.execute("SELECT user_id, sex, FTP FROM athlete")
    athletes = cursor.fetchall()
    
    test_sessions = [
        generate_realistic_test(user_id, sex, FTP)
        for (user_id, sex, FTP) in athletes
        for _ in range(10)
    ]
    
    cursor.executemany("""
        INSERT INTO test_session (athlete_id, date, cadence, power_output, heart_rate, respiratory_frequency, VO2, condition_rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, test_sessions)
    conn.commit()
    print("Each athlete has 10 tests recorded in the test_session table.")

def update_users_with_athlete_info():
    """Update the user table with first name, last name, and email from the athlete table"""
    
    # Retrieve athlete information (first name, last name, and user_id) from the `athlete` table
    cursor.execute("""
        SELECT athlete.user_id, athlete.first_name, athlete.last_name
        FROM athlete
        JOIN user ON athlete.user_id = user.id
    """)
    athletes = cursor.fetchall()

    # Create an array with updated information for the `user` table
    updated_users = []
    for user_id, first_name, last_name in athletes:
        username = f"{first_name.capitalize()}{last_name.capitalize()}"
        email = f"{first_name.lower()}.{last_name.lower()}@gmail.com"
        
        # Use `user_id` instead of `id`
        updated_users.append((username, email, user_id))
    
    # Update the `user` table with this information
    cursor.executemany("""
        UPDATE user
        SET username = ? , email = ?
        WHERE id = ?
    """, updated_users)
    
    # Apply the changes
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
