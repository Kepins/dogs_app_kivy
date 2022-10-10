import datetime
import sqlite3

from entities.appointment import Appointment
from entities.breed import Breed
from entities.dog import Dog
from entities.owner import Owner
from entities.service import Service
from entities.size import Size

DB_FILENAME = 'db_dogs.db'


class Model:
    def __init__(self):
        # Create database or connect to existing one
        self.db = sqlite3.connect(DB_FILENAME)
        # Create tables if database does not exist
        self.__create_tables_if_not_exists()
        # Inserts default values if they are not set
        self.__insert_default()

    def __create_tables_if_not_exists(self):
        # Create a cursor
        cursor = self.db.cursor()

        breed_create_query = """
            CREATE TABLE if not exists Breed (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            )
        """

        size_create_query = """
            CREATE TABLE if not exists Size (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            )
        """

        owner_create_query = """
            CREATE TABLE if not exists Owner (
                id INTEGER PRIMARY KEY,
                phone_number TEXT NOT NULL UNIQUE,
                phone_name TEXT,
                first_name TEXT,
                last_name TEXT,
                note TEXT
            )
        """

        dog_create_query = """
            CREATE TABLE if not exists Dog (
                id INTEGER PRIMARY KEY,
                name TEXT,
                id_owner INTEGER,
                id_breed INTEGER,
                id_size INTEGER,
                note TEXT,
                FOREIGN KEY(id_owner) REFERENCES Owner(id),
                FOREIGN KEY(id_breed) REFERENCES Breed(id),
                FOREIGN KEY(id_size) REFERENCES Size(id)
            )
        """

        service_create_query = """
            CREATE TABLE if not exists Service (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            )
        """

        appointment_create_query = """
            CREATE TABLE if not exists Appointment(
                id INTEGER PRIMARY KEY,
                date TEXT NOT NULL,
                time INTEGER NOT NULL,
                id_dog INTEGER,
                id_service INTEGER,
                cost INTEGER,
                FOREIGN KEY(id_dog) REFERENCES Dog(id),
                FOREIGN KEY(id_service) REFERENCES Service(id)
            )
        """

        cursor.execute(breed_create_query)
        cursor.execute(size_create_query)
        cursor.execute(owner_create_query)
        cursor.execute(dog_create_query)
        cursor.execute(service_create_query)
        cursor.execute(appointment_create_query)


    def __insert_default(self):
        query = """
            -- breeds
            INSERT INTO Breed(name) VALUES('Nieznana');
            INSERT INTO Breed(name) VALUES('Yorkshire terrier');
            INSERT INTO Breed(name) VALUES('Maltańczyk');
            INSERT INTO Breed(name) VALUES('Pudel');
            INSERT INTO Breed(name) VALUES('West highland white terier');
            INSERT INTO Breed(name) VALUES('Sznaucer');
            INSERT INTO Breed(name) VALUES('Cocker spaniel angielski');
            INSERT INTO Breed(name) VALUES('Mops');
            INSERT INTO Breed(name) VALUES('Buldog francuski');
            INSERT INTO Breed(name) VALUES('Labrador retriever');
            INSERT INTO Breed(name) VALUES('Golden retriever');
            INSERT INTO Breed(name) VALUES('Inna');
            
            
            -- sizes
            INSERT INTO Size(name) VALUES('Nieznana');
            INSERT INTO Size(name) VALUES('Mały');
            INSERT INTO Size(name) VALUES('Średni');
            INSERT INTO Size(name) VALUES('Duży');
            
            -- services
            INSERT INTO Service(name) VALUES('Strzyżenie');
            INSERT INTO Service(name) VALUES('Mycie i strzyżenie');
        """
        try:
            # Try to insert default values
            cursor = self.db.cursor()
            cursor.executescript(query)
        except sqlite3.IntegrityError:
            # Default values are already inserted
            pass

    def select_all_appointments(self) -> list[Appointment]:
        cursor = self.db.cursor()
        query = '''
            SELECT * FROM Appointment
        '''
        cursor.execute(query)
        tuples = cursor.fetchall()
        appointments = [Appointment(id=t[0], dog=self.select_dog(id=t[3]), service=self.select_service(id=t[4]),
                                    date=datetime.datetime.strptime(t[1], '%Y-%m-%dT%H:%M:%S'),
                                    time=datetime.timedelta(minutes=t[2]), cost=t[5]) for t in tuples]
        return appointments

    def select_all_owners(self) -> list[Owner]:
        cursor = self.db.cursor()
        query = '''
            SELECT * FROM Owner
        '''
        cursor.execute(query)
        tuples = cursor.fetchall()
        owners = [Owner(id=t[0], phone_number=t[1], phone_name=t[2], first_name=t[3], last_name=t[4], note=t[5])
                  for t in tuples]
        return owners

    def select_all_breeds(self) -> list[Breed]:
        cursor = self.db.cursor()
        query = '''
            SELECT * FROM Breed
        '''
        cursor.execute(query)
        tuples = cursor.fetchall()
        breeds = [Breed(id=t[0], name=t[1])
                  for t in tuples]
        return breeds

    def select_all_sizes(self) -> list[Size]:
        cursor = self.db.cursor()
        query = '''
            SELECT * FROM Size
        '''
        cursor.execute(query)
        tuples = cursor.fetchall()
        sizes = [Size(id=t[0], name=t[1])
                 for t in tuples]
        return sizes

    def select_all_services(self) -> list[Service]:
        cursor = self.db.cursor()
        query = '''
            SELECT * FROM Service
        '''
        cursor.execute(query)
        tuples = cursor.fetchall()
        services = [Service(id=t[0], name=t[1])
                    for t in tuples]
        return services

    def select_appointment(self, id: int) -> Appointment:
        cursor = self.db.cursor()
        query = '''
            SELECT * FROM Appointment
            WHERE id = ?
        '''
        cursor.execute(query, [id])
        t = cursor.fetchone()
        return Appointment(id=t[0], dog=self.select_dog(id=t[3]), service=self.select_service(id=t[4]),
                           date=datetime.datetime.strptime(t[1], '%Y-%m-%dT%H:%M:%S'),
                           time=datetime.timedelta(minutes=t[2]), cost=t[5])

    def select_dog(self, id: int) -> Dog:
        cursor = self.db.cursor()
        query = '''
            SELECT * FROM Dog
            WHERE id = ?
        '''
        cursor.execute(query, [id])
        t = cursor.fetchone()
        return Dog(id=t[0], name=t[1], owner=self.select_owner(id=t[2]), breed=self.select_breed(id=t[3]),
                   size=self.select_size(id=t[4]), note=t[5])

    def select_owner(self, id: int) -> Owner:
        cursor = self.db.cursor()
        query = '''
            SELECT * FROM Owner
            WHERE id = ?
        '''
        cursor.execute(query, [id])
        t = cursor.fetchone()
        return Owner(id=t[0], phone_number=t[1], phone_name=t[2], first_name=t[3], last_name=t[4], note=t[5])

    def select_breed(self, id: int) -> Breed:
        cursor = self.db.cursor()
        query = '''
            SELECT * FROM Breed
            WHERE id = ?
        '''
        cursor.execute(query, [id])
        t = cursor.fetchone()
        return Breed(id=t[0], name=t[1])

    def select_size(self, id: int) -> Size:
        cursor = self.db.cursor()
        query = '''
            SELECT * FROM Size
            WHERE id = ?
        '''
        cursor.execute(query, [id])
        t = cursor.fetchone()
        return Size(id=t[0], name=t[1])

    def select_service(self, id: int) -> Service:
        cursor = self.db.cursor()
        query = '''
            SELECT * FROM Service
            WHERE id = ?
        '''
        cursor.execute(query, [id])
        t = cursor.fetchone()
        return Service(id=t[0], name=t[1])

    @staticmethod
    def convert_empty_string(string):
        if string == '':
            return None
        else:
            return string

    def insert_owner(self, owner: Owner) -> Owner:
        cursor = self.db.cursor()
        query = "INSERT INTO Owner(phone_number, phone_name, first_name, last_name, note) VALUES(?, ?, ?, ?, ?)"
        values = (owner.phone_number, owner.phone_name, owner.first_name, owner.last_name, owner.note)
        values = [self.convert_empty_string(value) for value in values]

        cursor.execute(query, values)
        owner = self.select_owner(id=cursor.lastrowid)
        self.db.commit()
        return owner

    def insert_dog(self, dog: Dog) -> Dog:
        cursor = self.db.cursor()
        query = "INSERT INTO Dog(name, id_owner, id_breed, id_size, note) VALUES(?, ?, ?, ?, ?)"
        values = (dog.name, dog.owner.id, dog.breed.id, dog.size.id, dog.note)
        values = [self.convert_empty_string(value) for value in values]

        cursor.execute(query, values)
        dog = self.select_dog(id=cursor.lastrowid)
        self.db.commit()
        return dog

    def insert_appointment(self, appoint: Appointment) -> Appointment:
        cursor = self.db.cursor()
        query = "INSERT INTO Appointment(date, time, id_dog, id_service, cost) VALUES(?, ?, ?, ?, ?)"
        values = (appoint.date, appoint.time.total_seconds()//60, appoint.dog.id, appoint.service.id, appoint.cost)
        values = [self.convert_empty_string(value) for value in values]

        cursor.execute(query, values)
        appoint = self.select_appointment(id=cursor.lastrowid)
        self.db.commit()
        return appoint

    def update_owner(self, owner: Owner) -> Owner:
        cursor = self.db.cursor()
        query = "UPDATE Owner " \
                "SET phone_number = ?, phone_name = ?, first_name = ?, last_name = ?, note = ? " \
                "WHERE id = ?"
        values = (owner.phone_number, owner.phone_name, owner.first_name, owner.last_name, owner.note, owner.id)
        values = [self.convert_empty_string(value) for value in values]

        cursor.execute(query, values)
        owner = self.select_owner(id=owner.id)
        self.db.commit()
        return owner

    def update_dog(self, dog: Dog) -> Dog:
        cursor = self.db.cursor()
        query = "UPDATE Dog SET name = ?, id_breed = ?, id_size = ?, note = ? WHERE id = ?"
        values = (dog.name, dog.breed.id, dog.size.id, dog.note, dog.id)
        values = [self.convert_empty_string(value) for value in values]

        cursor.execute(query, values)
        dog = self.select_dog(id=dog.id)
        self.db.commit()
        return dog

    def update_appointment(self, appoint: Appointment) -> Appointment:
        cursor = self.db.cursor()
        query = "UPDATE Appointment " \
                "SET date = ?, time = ?, id_dog = ?, id_service = ?, cost = ? " \
                "WHERE id = ?"
        values = (appoint.date, appoint.time.total_seconds()//60,
                  appoint.dog.id, appoint.service.id, appoint.cost, appoint.id)
        values = [self.convert_empty_string(value) for value in values]

        cursor.execute(query, values)
        appoint = self.select_appointment(id=appoint.id)
        self.db.commit()
        return appoint

    def delete_appointment(self, appoint: Appointment) -> None:
        cursor = self.db.cursor()
        query = "DELETE FROM Appointment WHERE id = ?"
        values = [appoint.id]

        cursor.execute(query, values)
        self.db.commit()

