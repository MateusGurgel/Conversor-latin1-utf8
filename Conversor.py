import pymysql

db = pymysql.connect(host='200.139.21.67', port=3306, user='divsist', password='d1v1S1st', db='ojsbd2470prod')

cursor = db.cursor()
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
index = 0;
offset = 50;

for table in tables:

    index += 1

    if index < offset:
        continue 

    table_name = table[0]
    
    print(f"Table {table_name} started")
    print(f"Table index {index}")

    cursor.execute(f"DESCRIBE {table_name}")
    columns = cursor.fetchall()

    error = 0
    success = 0
    keys_searched = 0

    for column in columns:
        if column[0] == "setting_value":
            cursor.execute(f"SELECT {column[0]} FROM {table_name}")
            rows = cursor.fetchall()

            for row in rows:
                string = row[0]
                keys_searched += 1

                if not isinstance(string, str):
                    continue

                try:
                    utf8_str = string.encode('iso-8859-1').decode('utf-8')
                    query = f"UPDATE {table_name} SET {column[0]}='{utf8_str}' WHERE {column[0]}='{string}';"
                    cursor.execute(query)
                    db.commit()
                    success += 1
                except:
                    error += 1

    print(f"Table {table_name} finished")
    print(f"Keys searched: {keys_searched}")
    print(f"Successful updates: {success}")
    print(f"Errors: {error}")
db.close()
