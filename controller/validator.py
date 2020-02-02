import re
from enum import Enum


class InputException(Exception):
    pass


class ValidationType(Enum):
    AGE = 1,
    ID = 2,
    EMAIL = 3,


class Validator:

    def __init__(self, controller):
        self._controller = controller

    def validate(self, model, is_update=False):
        for f in model.get_fields():
            if model.__dict__[f.get_name()] is None:
                continue
            validation_type = f.get_validation_type()
            if validation_type == ValidationType.AGE:
                self.validate_age(model, f)
            elif validation_type == ValidationType.ID:
                if is_update:
                    self.validate_existing_id(model, f)
                else:
                    self.validate_new_id(model, f)
            elif validation_type == ValidationType.EMAIL:
                self.validate_email(model, f)

    @staticmethod
    def validate_age(model, field):
        value = model.__dict__[field.get_model_name()]
        if not isinstance(value, int):
            raise InputException("Age is not number")
        if value not in range(0, 130):
            raise InputException("Incorrect age")

    def validate_existing_id(self, model, field):
        if self.validate_id(model, field):
            raise InputException("Incorrect id")

    def validate_new_id(self, model, field):
        if not self.validate_id(model, field):
            raise InputException("Id is already used")

    def validate_id(self, model, field):
        usr_id = model.__dict__[field.get_model_name()]
        if not isinstance(usr_id, int):
            raise InputException("Incorrect id")
        model_filter = type(model)(id=usr_id)
        return len(self._controller.get_values(model_filter)) == 0

    @staticmethod
    def validate_email(model, field):
        email = model.__dict__[field.get_model_name()]
        if not isinstance(email, str):
            raise InputException("Incorrect email")
        r = re.compile(r'\w+@[a-z]+\.[a-z]+')
        if not re.match(r, email):
            raise InputException("Incorrect email")
