import mysql.connector


class SqlHelper():
    # create a database instance 
    def initDbInstance(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678"
        )
        self.__checkDB(self)
        return self.mydb

    # check database status, if not exists create one!
    def __checkDB(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("""SELECT SCHEMA_NAME
                            FROM INFORMATION_SCHEMA.SCHEMATA
                            WHERE SCHEMA_NAME = 'share'""")
        dbExists = False
        if len(mycursor.fetchall()) > 0:
            print("DB exists!")
            dbExists = True
            
        if not dbExists:
            print("Create DB share!")
            # create database and tables
            results = mycursor.execute("""
            CREATE DATABASE share;
            USE share;
            CREATE TABLE `share_user` (
                `userId` int NOT NULL AUTO_INCREMENT,
                `userName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                `password` varchar(100) DEFAULT NULL,
                `sex` varchar(6) DEFAULT NULL,
                `age` int DEFAULT NULL,
                PRIMARY KEY (`userId`)
            ) 
            ENGINE=InnoDB 
            AUTO_INCREMENT=1;

            CREATE TABLE `share_grouplist` (
                groupId INT auto_increment NOT NULL,
                groupName varchar(100) NULL,
                PRIMARY KEY (`groupId`)
            )
            ENGINE=InnoDB
            DEFAULT CHARSET=utf8mb4
            COLLATE=utf8mb4_0900_ai_ci
            AUTO_INCREMENT=1;
            
            CREATE TABLE `share_articles` (
                articleId INT auto_increment NOT NULL,
                content varchar(100) NULL,
                title varchar(100) NULL,
                groupId INT NOT NULL,
                PRIMARY KEY (`articleId`),
                FOREIGN KEY (groupId) REFERENCES share_grouplist (groupId)
            )
            ENGINE=InnoDB
            AUTO_INCREMENT=1;

            """, multi=True)

            for cur in results:
                print('cursor:', cur)
                if cur.with_rows:
                    print('result:', cur.fetchall())

        else:
            mycursor.execute("USE share;")

        self.mydb.commit()
        mycursor.close()

    def __init__(self):
        self.mydb = None
