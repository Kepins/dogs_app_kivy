import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import MySQLConnection

from entities.appointment import Appointment
from entities.breed import Breed
from entities.dog import Dog
from entities.owner import Owner
from entities.service import Service
from entities.size import Size


class Model:
    db: MySQLConnection

    owners: [Owner]
    sizes: [Size]
    breeds: [Breed]
    dogs: [Dog]
    services: [Service]
    appointments: [Appointment]

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
            owner = Owner(id=t[0], phone=t[1], first_name=t[2], last_name=t[3], note=t[4], dogs=[])
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


