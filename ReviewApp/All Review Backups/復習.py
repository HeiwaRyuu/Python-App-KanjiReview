import psycopg2

# Connecting to the DB
try:
    con = psycopg2.connect(
        host = "localhost",
        database = "review",
        user = "postgres",
        password = "35c4p3fromh3ll",
        port = 5432
    )
except:
    print("Cannot connect to the database")

# Cursor
cur = con.cursor()

# Creating the table if it does not already exists
create_table = "CREATE TABLE IF NOT EXISTS reviewkanji (id SERIAL PRIMARY KEY, keyword VARCHAR(50), kanji VARCHAR(30))"
cur.execute(create_table)

# Inserting some random data for test into the table
insert_into_table = "INSERT INTO reviewkanji (keyword, kanji) VALUES ('I(as perceiving subject)', '吾'), ('Stone', '石')"
cur.execute(insert_into_table)

# Grabing all data inside the table 
select_from_table = "SELECT keyword, kanji from reviewkanji"
cur.execute(select_from_table)

con.commit()

rows = cur.fetchall()

for r in rows:
    print(r)

# Closing cursor
cur.close()

# Closing the connection
con.close()
