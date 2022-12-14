from datetime import date

from mysql.connector import Error

from entities.appointment import Appointment
from entities.dog import Dog
from entities.owner import Owner
from controller.errors import InsertOwnerError, InsertDogError, EditDogError, EditOwnerError, InsertAppointmentError, \
    EditAppointmentError, RemoveAppointmentError, ConnectError
from model.model import Model


class Controller:
    model: Model

    def __init__(self):
        try:
            self.model = Model()
        except Error as err:
            raise ConnectError(err)

    def get_owners(self, phone_number: str = '', phone_name: str = '', last_name: str = ''):
        owners = self.model.owners
        owners = filter(lambda o: phone_number in o.phone_number, owners)
        if phone_name != '':
            owners = filter(lambda o: o.phone_name is not None and o.phone_name.startswith(phone_name), owners)
        if last_name != '':
            owners = filter(lambda o: o.last_name is not None and o.last_name.startswith(last_name), owners)
        return list(owners)

    def get_breeds(self):
        breeds = self.model.breeds
        breeds = sorted(breeds, key=lambda b: b.id)
        return breeds

    def get_sizes(self):
        sizes = self.model.sizes
        # temporary solution
        sizes_sorted = sorted(sizes, key=lambda s: s.id)
        return sizes_sorted

    def get_appointments(self, day: date):
        # appointment.date is datetime but day is date so .date() method must be used
        appointments = list(filter(lambda a: a.date.date() == day, self.model.appointments))
        appointments = sorted(appointments, key=lambda a: a.date)
        return appointments

    def get_services(self):
        services = self.model.services
        return services

    def add_owner(self, owner: Owner):
        try:
            self.model.insert_owner(owner)
        except Error as err:
            raise InsertOwnerError(err)

    def add_dog(self, dog: Dog):
        try:
            self.model.insert_dog(dog)
        except Error as err:
            raise InsertDogError(err)

    def edit_dog(self, dog: Dog):
        try:
            self.model.update_dog(dog)
        except Error as err:
            raise EditDogError(err)

    def edit_owner(self, owner: Owner):
        try:
            self.model.update_owner(owner)
        except Error as err:
            raise EditOwnerError(err)

    def add_appointment(self, appoint: Appointment):
        try:
            self.model.insert_appointment(appoint)
        except Error as err:
            raise InsertAppointmentError(err)

    def edit_appointment(self, appoint: Appointment):
        try:
            self.model.update_appointment(appoint)
        except Error as err:
            raise EditAppointmentError(err)

    def remove_appointment(self, appoint: Appointment):
        try:
            self.model.delete_appointment(appoint)
        except Error as err:
            raise RemoveAppointmentError(err)