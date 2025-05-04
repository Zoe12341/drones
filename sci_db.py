from scidbpy import connect
    
try:
    connection = connect(host="localhost", port=8080, username="drone", password="Buzzing0verhead")
    print("Successfully connected to SciDB!")
except Exception as e:
    print(f"Error connecting to SciDB: {e}")
