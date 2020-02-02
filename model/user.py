from model.model import Model, Field
from controller.validator import ValidationType


class User(Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_fields():
        return [
            Field('first_name', 'TEXT'),
            Field('surname', 'TEXT'),
            Field('age', 'INT', ValidationType.AGE),
            Field('phone', 'TEXT'),
            Field('email', 'TEXT', ValidationType.EMAIL),
            Field(
                'office_id',
                'INTEGER  REFERENCES Office(id) ON DELETE SET NULL'
            ),
            Field('id', 'INTEGER NOT NULL PRIMARY KEY', ValidationType.ID),
        ]

    @staticmethod
    def get_model_name():
        return 'User'
