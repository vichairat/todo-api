import sqlite3

conn = sqlite3.connect('todo.db')
print "Opened database successfully";

conn.execute('''CREATE TABLE items
       (id	INTEGER	PRIMARY KEY	AUTOINCREMENT,
       subject	CHAR(255)	NOT NULL,
       detail	TEXT,
       done	BOOLEAN	NOT NULL);''')
print "Table created successfully";

conn.execute('''INSERT INTO items (subject, detail, done) 
	VALUES ('sample subject', 'sample detail', 0 )''');

conn.commit()
print "Records created successfully";

conn.close()