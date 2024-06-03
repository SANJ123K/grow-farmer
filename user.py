from database import mydb

cursor = mydb.cursor()

query = """
            create table grow_farmer.user(
            name varchar(20),
            email varchar(40) PRIMARY KEY,
            password varchar(20),
            mobile varchar(10),
            city varchar(20),
            state varchar(15))
         """
cursor.execute(query)
cursor.close()
mydb.commit()
