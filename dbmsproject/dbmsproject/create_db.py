import mysql.connector

connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="dbms",
  auth_plugin='mysql_native_password'
)

cursor= connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS User (
username varchar(200) PRIMARY KEY,
password TEXT NOT NULL
);""")

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Doctor (
#   name VARCHAR(255),
#   age INT,
#   speciality VARCHAR(255),
#   patients INT,
#   FOREIGN KEY (patients) REFERENCES patients(name),
#   PRIMARY KEY (name)
# );""")

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Patients (
#   ID int,
#   name VARCHAR(255),
#   age INT,
#   sickness VARCHAR(255),
#   PRIMARY KEY (ID)
# );""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Doctor (
  name VARCHAR(255) PRIMARY KEY,
  age INT,
  speciality VARCHAR(255),
  patients INT,
  FOREIGN KEY (Patients) REFERENCES Patients(ID)
    ON UPDATE CASCADE
    ON DELETE SET NULL
);""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Patients (
  ID INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255),
  age INT,
  sickness VARCHAR(255)
);""")
