from model.user import User
from model.office import Office
from model.join import Join
from tabulate import tabulate
from view.shortcuts import shortcut, param_shortcut


@shortcut
class Commands:

    def __init__(self, controller):
        self.controller = controller
        self.controller.create_table(User())
        self.controller.create_table(Office())

    @param_shortcut
    def add_user(self, *args, **kwargs):
        user = User(*args, **kwargs)
        self.controller.insert_value(user)

    def add_office(self, *args, **kwargs):
        office = Office(*args, **kwargs)
        self.controller.insert_value(office)

    def get_users(self, *args, **kwargs):
        user = User(*args, **kwargs)
        col = None
        if "columns" in kwargs.keys():
            col = kwargs["columns"]
        res = self.controller.get_values(user, col)
        if len(res) == 0:
            print("No persons found")
            return
        print(tabulate([
            m.to_compressed_dict()
            for m in res
        ], headers="keys", tablefmt="github"))

    def get_offices(self, *args, **kwargs):
        office = Office(*args, **kwargs)
        col = None
        if "columns" in kwargs.keys():
            col = kwargs["columns"]
        res = self.controller.get_values(office, col)
        if len(res) == 0:
            print("No offices found")
            return
        print(tabulate([
            m.to_compressed_dict()
            for m in res
        ], headers="keys", tablefmt="github"))

    def delete_user(self, *args, **kwargs):
        user = User(*args, **kwargs)
        if "f" not in kwargs.keys():
            res = self.controller.get_values(user)
            print("Do you want to delete %i users? [y/N]" % len(res))
            if not input() in ['y', 'Y']:
                print("Aborted")
                return
        self.controller.delete_values(user)

    def delete_office(self, *args, **kwargs):
        office = Office(*args, **kwargs)
        if "f" not in kwargs.keys():
            res = self.controller.get_values(office)
            print("Do you want to delete %i offices? [y/N]" % len(res))
            if not input() in ['y', 'Y']:
                print("Aborted")
                return
        self.controller.delete_values(office)

    def update_user(self, usr_id, *args, **kwargs):
        user_old = User(id=usr_id)
        if len(self.controller.get_values(user_old)) == 0:
            print("No users to update")
        user = User(*args, **kwargs)
        self.controller.update_values(user_old, user)

    def update_office(self, office_id, *args, **kwargs):
        office_old = User(id=office_id)
        if len(self.controller.get_values(office_old)) == 0:
            print("No offices to update")
        office = Office(*args, **kwargs)
        self.controller.update_values(office_old, office)

    def get_all(self, *args, **kwargs):
        user = User(**kwargs)
        office = Office(**kwargs)
        table = Join(user, office, 'office_id', 'id')
        res = self.controller.get_values(table, args)
        if len(res) == 0:
            print("No users found")
            return
        print(tabulate([
            m.to_compressed_dict()
            for m in res
        ], headers="keys", tablefmt="github"))
