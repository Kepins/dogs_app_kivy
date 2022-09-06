import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import MySQLConnection, Error

from entities.appointment import Appointment
from entities.breed import Breed
from entities.dog import Dog
from entities.owner import Owner
from entities.service import Service
from entities.size import Size


class Model:
    db: MySQLConnection

    owners: list[Owner]
    sizes: list[Size]
    breeds: list[Breed]
    dogs: list[Dog]
    services: list[Service]
    appointments: list[Appointment]

    def __init__(self):
        # load environment variables from '.env' file
        load_dotenv()
        self.db = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            passwd=os.getenv('MYSQL_PASSWD'),
            database=os.getenv('MYSQL_DATABASE')
        )
        self.__load()

    def __load(self):
        self.__load_owners()
        self.__load_sizes()
        self.__load_breeds()
        self.__load_dogs()
        self.__load_services()
        self.__load_appointments()

    def __load_owners(self):
        self.owners = []
        cursor = self.db.cursor()
        query = '''
            SELECT * FROM Owner
        '''
        cursor.execute(query)
        tuples = cursor.fetchall()
        for t in tuples:
            owner = Owner(id=t[0], phone_number=t[1], phone_name=t[2], first_name=t[3], last_name=t[4], note=t[5], dogs=[])
            self.owners.append(owner)

    def __load_sizes(self):
        self.sizes = []
        cursor = self.db.cursor()
        query = '''
            SELECT * FROM Size
         '''
        cursor.execute(query)
        tuples = cursor.fetchall()
        for t in tuples:
            size = Size(id=t[0], name=t[1], dogs=[])
            self.sizes.append(size)

    def __load_breeds(self):
        self.breeds = []
        cursor = self.db.cursor()
        query = '''
            SELECT * FROM Breed
        '''
        cursor.execute(query)
        tuples = cursor.fetchall()
        for t in tuples:
            breed = Breed(id=t[0], name=t[1], dogs=[])
            self.breeds.append(breed)

    def __load_dogs(self):
        self.dogs = []
        cursor = self.db.cursor()
        query = '''
            SELECT * FROM Dog
         '''
        cursor.execute(query)
        tuples = cursor.fetchall()
        for t in tuples:
            id = t[0]
            name = t[1]
            id_owner = t[2]
            owner = next(filter(lambda o: o.id == id_owner, self.owners))
            id_breed = t[3]
            breed = next(filter(lambda b: b.id == id_breed, self.breeds))
            id_size = t[4]
            size = next(filter(lambda s: s.id == id_size, self.sizes))
            note = t[5]
            dog = Dog(id=id, name=name, owner=owner, breed=breed, size=size, note=note, appointments=[])
            owner.dogs.append(dog)
            breed.dogs.append(dog)
            size.dogs.append(dog)
            self.dogs.append(dog)

    def __load_services(self):
        self.services = []
        cursor = self.db.cursor()
        query = '''
            SELECT * FROM Service
         '''
        cursor.execute(query)
        tuples = cursor.fetchall()
        for t in tuples:
            service = Service(id=t[0], name=t[1], appointments=[])
            self.services.append(service)

    def __load_appointments(self):
        self.appointments = []
        cursor = self.db.cursor()
        query = '''
                    SELECT * FROM Appointment
                 '''
        cursor.execute(query)
        tuples = cursor.fetchall()
        for t in tuples:
            id = t[0]
            date = t[1]
            id_dog = t[2]
            dog = next(filter(lambda d: d.id == id_dog, self.dogs))
            id_service = t[3]
            service = next(filter(lambda s: s.id == id_service, self.services))
            cost = t[4]
            appointment = Appointment(id=id, date=date, dog=dog, service=service, cost=cost)
            dog.appointments.append(appointment)
            service.appointments.append(appointment)
            self.appointments.append(appointment)

    @staticmethod
    def convert_empty_string(string):
        if string == '':
            return None
        else:
            return string

    def insert_owner(self, owner: Owner):
        cursor = self.db.cursor()
        query = "INSERT INTO Owner(phone_number, phone_name, first_name, last_name, note) VALUES(%s, %s, %s, %s, %s)"
        values = (owner.phone_number, owner.phone_name, owner.first_name, owner.last_name, owner.note)
        values = [self.convert_empty_string(value) for value in values]
        try:
            cursor.execute(query, values)
            owner.id = cursor.lastrowid
            self.db.commit()
            self.owners.append(owner)
        except Error as err:
            raise err

    def insert_dog(self, dog: Dog):
        cursor = self.db.cursor()
        query = "INSERT INTO Dog(name, id_owner, id_breed, id_size, note) VALUES(%s, %s, %s, %s, %s)"
        values = (dog.name, dog.owner.id, dog.breed.id, dog.size.id, dog.note)
        values = [self.convert_empty_string(value) for value in values]
        try:
            cursor.execute(query, values)
            dog.id = cursor.lastrowid
            self.db.commit()
            self.dogs.append(dog)
            dog.owner.dogs.append(dog)
            dog.breed.dogs.append(dog)
            dog.size.dogs.append(dog)
        except Error as err:
            raise err

    # owner parameter HAS TO be a new instance of Owner class and not changed existing instance
    def update_owner(self, owner: Owner):
        cursor = self.db.cursor()
        query = "UPDATE Owner " \
                "SET phone_number = %s, phone_name = %s, first_name = %s, last_name = %s, note = %s " \
                "WHERE id = %s"
        values = (owner.phone_number, owner.phone_name, owner.first_name, owner.last_name, owner.note, owner.id)
        values = [self.convert_empty_string(value) for value in values]
        try:
            cursor.execute(query, values)
            self.db.commit()

            existing_owner = next(filter(lambda o: o.id == owner.id, self.owners))
            existing_owner.phone_number = owner.phone_number
            existing_owner.phone_name = owner.phone_name
            existing_owner.first_name = owner.first_name
            existing_owner.last_name = owner.last_name
            existing_owner.note = owner.note

        except Error as err:
            raise err

    # dog parameter HAS TO be a new instance of Dog class and not changed existing instance
    def update_dog(self, dog: Dog):
        cursor = self.db.cursor()
        query = "UPDATE Dog SET name = %s, id_breed = %s, id_size = %s, note = %s WHERE id = %s"
        values = (dog.name, dog.breed.id, dog.size.id, dog.note, dog.id)
        values = [self.convert_empty_string(value) for value in values]
        try:
            cursor.execute(query, values)
            self.db.commit()

            existing_dog = next(filter(lambda d: d.id == dog.id, self.dogs))
            existing_dog.breed.dogs.remove(existing_dog)
            existing_dog.size.dogs.remove(existing_dog)

            existing_dog.name = dog.name
            existing_dog.breed = dog.breed
            existing_dog.size = dog.size
            existing_dog.note = dog.note
            existing_dog.breed.dogs.append(existing_dog)
            existing_dog.size.dogs.append(existing_dog)

        except Error as err:
            raise err
