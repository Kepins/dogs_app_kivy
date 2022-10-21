from datetime import date


from entities.appointment import Appointment
from entities.dog import Dog
from entities.owner import Owner
from entities.breed import Breed
from entities.service import Service
from entities.size import Size

from model.model import Model


class Controller:
    model: Model

    def __init__(self):
        self.model = Model()

    def get_owners(self, phone_number: str = '', phone_name: str = '', last_name: str = '') -> list[Owner]:
        owners = self.model.select_all_owners()
        owners = filter(lambda o: phone_number in o.phone_number, owners)
        if phone_name != '':
            owners = filter(lambda o: o.phone_name is not None and o.phone_name.startswith(phone_name), owners)
        if last_name != '':
            owners = filter(lambda o: o.last_name is not None and o.last_name.startswith(last_name), owners)
        return list(owners)

    def get_dogs(self, owner: Owner) -> list[Dog]:
        dogs = self.model.select_all_dogs()
        dogs = filter(lambda d: d.owner.id == owner.id, dogs)
        return list(dogs)

    def get_breeds(self) -> list[Breed]:
        breeds = self.model.select_all_breeds()
        breeds = sorted(breeds, key=lambda b: b.id)
        return breeds

    def get_sizes(self) -> list[Size]:
        sizes = self.model.select_all_sizes()
        # temporary solution
        sizes_sorted = sorted(sizes, key=lambda s: s.id)
        return sizes_sorted

    def get_appointments(self, day: date) -> list[Appointment]:
        # appointment.date is datetime but day is date so .date() method must be used
        appointments = list(filter(lambda a: a.date.date() == day, self.model.select_all_appointments()))
        appointments = sorted(appointments, key=lambda a: a.date)
        return appointments

    def get_services(self) -> list[Service]:
        services = self.model.select_all_services()
        return services

    def add_owner(self, owner: Owner) -> Owner:
        return self.model.insert_owner(owner)

    def add_dog(self, dog: Dog) -> Dog:

        return self.model.insert_dog(dog)

    def edit_dog(self, dog: Dog) -> Dog:
        return self.model.update_dog(dog)

    def edit_owner(self, owner: Owner) -> Owner:
        return self.model.update_owner(owner)

    def add_appointment(self, appoint: Appointment) -> Appointment:
        return self.model.insert_appointment(appoint)

    def edit_appointment(self, appoint: Appointment) -> Appointment:
        return self.model.update_appointment(appoint)

    def remove_appointment(self, appoint: Appointment) -> None:
        self.model.delete_appointment(appoint)
