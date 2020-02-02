from model.model import Model, Field
from controller.validator import ValidationType


class Office(Model):
    @staticmethod
    def get_fields():
        return [
            Field('name', 'TEXT NOT NULL'),
            Field('phone', 'TEXT'),
            Field('email', 'INT', ValidationType.EMAIL),
            Field('adress', 'TEXT'),
            Field('id', 'INTEGER NOT NULL PRIMARY KEY', ValidationType.ID),
        ]

    @staticmethod
    def get_model_name():
        return 'Office'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
