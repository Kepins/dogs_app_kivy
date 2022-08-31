from entities.owner import Owner
from model import Model


class Controller:
    model: Model

    def __init__(self):
        self.model = Model()

    def get_owners(self, phone='', first_name='', last_name=''):
        owners = self.model.owners
        owners = filter(lambda o: phone in o.phone, owners)
        if first_name != '':
            owners = filter(lambda o: o.first_name is not None and o.first_name.startswith(first_name), owners)
        if last_name != '':
            owners = filter(lambda o: o.last_name is not None and o.last_name.startswith(last_name), owners)
        return list(owners)

    def get_breeds(self):
        breeds = self.model.breeds
        return breeds

    def get_sizes(self):
        sizes = self.model.sizes
        # temporary solution
        sizes_sorted = sorted(sizes, key=lambda s: s.id)
        return sizes_sorted

    def update_owner(self, owner: Owner):
        pass