import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# Retrieve the top 10 scores in descending order
cursor.execute('SELECT name, score FROM high_scores ORDER BY score DESC LIMIT 10')
top_scores = cursor.fetchall()

# Display the top scores with names
for rank, (name, score) in enumerate(top_scores, start=1):
    print(f"Rank {rank}: Name: {name}, Score: {score}")

# Close the database connection
conn.close()
