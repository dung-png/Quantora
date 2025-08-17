import os
import sqlite3
import json
import configparser
from normalization import normalization

class User_DATA():
    def __init__(self):
        #tao folder
        os.makedirs("database",exist_ok=True)

        #country code
        with open(r'code\countrycode.json','r') as file:
            self.countrycode = json.load(file)

        #connect database
        self.user_db = sqlite3.connect(r"database\users.db")
        self.user_list = []
        self.cursor = self.user_db.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,business_name TEXT NOT NULL UNIQUE,username TEXT NOT NULL UNIQUE,email TEXT NOT NULL UNIQUE,password TEXT NOT NULL,phonenumber TEXT NOT NULL UNIQUE,countrycode TEXT NOT NULL)")
        self.user_db.commit()
        self.read()

    def checkkeeplogin(self):
        if os.path.exists(r'database\config.ini'):
            config = configparser.ConfigParser()
            config.read(r'database\config.ini')
            if config.has_section("Keeplogin"):
                email = config.get("Keeplogin", "email")
                username = config.get("Keeplogin", "username")
                business_name = config.get("Keeplogin", "business_name")
                password = config.get("Keeplogin", "password")
                phonenumber = config.get("Keeplogin", "phonenumber")
                countrycode = config.get("Keeplogin", "countrycode")
                current_user = self.get_user_by_email(email_input=email)
                if current_user:
                    if username == current_user.username and business_name == current_user.business_name and password == current_user.password and phonenumber == current_user.phonenumber and countrycode == current_user.countrycode:
                        return current_user
                return False
            
    def read(self):
        self.cursor.execute("SELECT * FROM users")
        self.user_data = self.cursor.fetchall()
        for t in self.user_data:
            print(t)
            new_user = User(t[0],t[1],t[2],t[3],t[4],t[5],t[6])
            self.user_list.append(new_user)
    
    def insert(self,user_tuple):
        self.cursor.execute("INSERT INTO users (business_name,username,email,password,phonenumber,countrycode) VALUES (?,?,?,?,?,?)",user_tuple)
        self.user_db.commit()
    
    def is_valid_email(self, email_input:str):
        email_input = email_input.strip()
        if "@" in email_input and '.' in email_input:
            return True
        return False
    
    def is_valid_password(self, password_input):
        if len(password_input) >= 8 and len(password_input) <= 20:
            return True
        return False
    
    def is_valid_business_name(self,business_name_input):
        len_business_name = len(normalization(business_name_input))
        if len_business_name >= 3 and len_business_name <= 20:
            for user in self.user_list:
                if normalization(user.business_name) == normalization(business_name_input):
                    return False
            return True
        return False
    
    def is_valid_username(self,username_input):
        len_username = len(normalization(username_input))
        if len_username >= 3 and len_username <= 20:
            for user in self.user_list:
                if normalization(user.username) == normalization(username_input):
                    return False
            return True
        return False

    def is_valid_phonenumber(self, countrycode_input, phonenumber_input):
        list_ = self.countrycode[countrycode_input].split('.')
        if len(phonenumber_input) >= int(list_[0]) and len(phonenumber_input) <= int(list_[1]):
            for user in self.user_list:
                if user.phonenumber == "0"+phonenumber_input:
                    return False
                elif user.phonenumber == phonenumber_input:
                    return False
            if len(phonenumber_input) < int(list_[1]):
                return 1
            else:
                return True
        return False
    
    def get_user_by_email(self,email_input):
        email_input = email_input.strip()
        for user in self.user_list:
            if user.email.strip() == email_input:
                return user
        return False
    
    def signup(self,user_tuple):
        phonenumber_check = self.is_valid_phonenumber(user_tuple[5], user_tuple[4])
        if not self.is_valid_business_name(user_tuple[0]): #khong trung business name
            return 4
        if not self.is_valid_username(user_tuple[1]): #khong trung username
            return 5
        if not self.is_valid_email(user_tuple[2]):
            return 2
        if not self.is_valid_password(user_tuple[3]):
            return 1
        if not phonenumber_check == True: #khong trung
            return 3
        elif phonenumber_check == 1:
            user_tuple = (user_tuple[0],user_tuple[1],user_tuple[2],user_tuple[3],'0'+user_tuple[4],user_tuple[5])
        if self.get_user_by_email(user_tuple[2]): #khong trung V
            return 6
        self.insert(user_tuple)
        user_id = self.cursor.lastrowid
        new_user = User(id = user_id,business_name=user_tuple[0],username=user_tuple[1],email=user_tuple[2],password=user_tuple[3],phonenumber=user_tuple[4],countrycode=user_tuple[5])
        self.user_list.append(new_user)
        return new_user
    
    def checkphonenumber(self, input_number, stored_number):
        input_number = str(input_number).strip()
        stored_number = str(stored_number).strip()

        if input_number == stored_number:
            return True
        elif input_number == "0" + stored_number:
            return True
        elif stored_number == "0" + input_number:
            return True
        return False

    def signin(self, user_tuple):
        user = self.get_user_by_email(user_tuple[0].strip())
        if user and str(user.password).strip() == str(user_tuple[1]).strip() and self.checkphonenumber(user_tuple[2],user.phonenumber):
            if user_tuple[3]:
                config = configparser.ConfigParser()
                config["Keeplogin"] = {
                    "email": user.email,
                    "username" : user.username,
                    "business_name" : user.business_name,
                    "password": user.password,
                    "phonenumber" : user.phonenumber,
                    "countrycode" : user.countrycode
                    }
                with open(r"database\config.ini", 'w') as configfile:
                    config.write(configfile)
            return user
        return False

class User():
    def __init__(self,id,business_name,username,email,password,phonenumber,countrycode):
        self.id = id
        self.business_name = business_name.strip()
        self.username = username.strip()
        self.email = email.strip()
        self.password = password.strip()
        self.phonenumber = phonenumber.strip()
        self.countrycode = countrycode

class Product_DATA():
    def __init__(self, user_id , type):
        self.product_db = sqlite3.connect(r'database\products.db')
        self.cursor = self.product_db.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL , image_path TEXT , name TEXT NOT NULL , available INTEGER NOT NULL , cost INTEGER NOT NULL)")
        self.product_db.commit()
        self.product_list = []
        self.Read_data(user_id)
        self.product_list = self._Sort_(self.product_list,type)

    def Read_data(self , user_id):
        self.cursor.execute("SELECT * FROM products")
        self.products_data = self.cursor.fetchall()
        for t in self.products_data:
            if int(t[1]) == int(user_id):
                print("t",t)
                print("product list",self.product_list)
                new_product = Product(t[0],t[1],t[2],t[3],t[4],t[5])
                self.product_list.append(new_product)
        
    def Insert_(self,tuple__):
        print("Inserting product:",tuple__)
        self.cursor.execute("INSERT INTO products (user_id,image_path,name,available,cost) VALUES (?,?,?,?,?)",tuple__)
        self.product_db.commit()
        _product_id = self.cursor.lastrowid
        new_product = Product(_product_id,tuple__[0],tuple__[1],tuple__[2],tuple__[3],tuple__[4])
        self.product_list.append(new_product)

    def Remove_(self,object):
        self.cursor.execute("DELETE FROM products WHERE id = ? AND user_id = ?",(object.id,object.user_id))
        self.product_db.commit()
        self.product_list.remove(object)

    def Edit_(self,tuple__):
        self.cursor.execute("UPDATE products SET image_path = ? , name = ? , available = ? , cost = ? WHERE id = ? AND user_id = ?",tuple__)
        self.product_db.commit()

    def _Sort_(self,input_list,type):
        if type.lower().strip() == "A-Z".lower().strip():
            for origin in range(len(input_list)):
                for index in range(origin+1,len(input_list)):
                    if input_list[origin].name > input_list[index].name:
                        input_list[origin] ,input_list[index] = input_list[index], input_list[origin]
            return input_list
        elif type.lower().strip() == "Z-A".lower().strip():
            for origin in range(len(input_list)):
                for index in range(origin+1,len(input_list)):
                    if input_list[origin].name < input_list[index].name:
                        input_list[origin] ,input_list[index] = input_list[index], input_list[origin]
            return input_list
        else:
            for origin in range(len(input_list)):
                for index in range(origin+1,len(input_list)):
                    if input_list[origin].id < input_list[index].id:
                        input_list[origin] ,input_list[index] = input_list[index], input_list[origin]
            return input_list
    
    def Search(self,Input__):
        result = []
        for product in self.product_list:
            if normalization(Input__) in normalization(product.name):
                result.append(product)
        return result
    
class Product():
    def __init__(self,id,user_id,image,name,available,cost):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.available = available
        self.cost = cost
        if image.lower().strip() == "browse".lower().strip():
            self.image = r"D:/Quantora/ui/src/noneimg.png"
            print("path",self.image)
        else:
            self.image = image.strip()
        print("Product image:", self.image)

    def update_(self,tuple__):
        self.image = tuple__[0]
        self.name = tuple__[1]
        self.available = tuple__[2]
        self.cost = tuple__[3]