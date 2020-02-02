import sqlite3 as sql
from controller.validator import Validator
from controller.log import log
import settings


def query(f):
    def wrapper(*args, **kwargs):
        self = args[0]
        connection = sql.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        q, args = f(*args, **kwargs)
        log('query', q, *args)
        cursor.execute(q, args)
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        return result
    return wrapper


class Controller:

    def __init__(self, path=settings.DATA_PATH):
        self.db_path = path
        self._validator = Validator(self)

    @staticmethod
    def get_data(model):
        return

    @query
    def create_table(self, model):
        q = 'CREATE TABLE IF NOT EXISTS %s(%s);' % (
            model.get_model_name(),
            ', '.join([
                k + ' ' + v
                for k, v in model.get_fields_dict().items()
            ]),
        )
        return q, []

    @query
    def insert_value(self, model):
        self._validator.validate(model)
        data = model.get_data()
        q = 'INSERT INTO %s(%s) VALUES (%s);' % (
            model.get_model_name(),
            ', '.join([k for k, _ in data]),
            ', '.join(['?' for _, _ in data]),
        )
        return q, [v for _, v in data]

    @query
    def _get_values(self, model, columns):
        data_filter = model.get_data()
        q = 'SELECT %s FROM %s' % (
            ', '.join(columns),
            model.get_model_name(),
        )
        if len(data_filter) != 0:
            q += ' WHERE %s;' % (
                ', '.join([k + '=?' for k, v in data_filter]),
            )
        else:
            q += ';'
        return q, [v for _, v in data_filter]

    def get_values(self, model, columns=None):
        if columns is None:
            columns = []
        if len(columns) == 0:
            columns = list(model.get_fields_names())
        data = self._get_values(model, columns)
        res = []
        for v in data:
            curr = dict()
            for i, c in enumerate(columns):
                curr[c] = v[i]
            res.append(model.copy(**curr))
        return res

    @query
    def delete_values(self, model):
        data_filter = model.get_data()
        q = 'DELETE FROM %s' % (
            model.get_model_name(),
        )
        if len(data_filter) != 0:
            q += ' WHERE %s;' % (
                ', '.join([k + '=?' for k, v in data_filter]),
            )
        else:
            q += ';'
        return q, [v for _, v in data_filter]

    @query
    def update_values(self, model, set_model):
        self._validator.validate(model, True)
        self._validator.validate(set_model)
        data_filter = model.get_data()
        data = set_model.get_data()
        q = 'UPDATE %s SET %s ' % (
            model.get_model_name(),
            ' ,'.join([k + '=?' for k, v in data])
        )
        if len(data_filter) != 0:
            q += ' WHERE %s;' % (
                ', '.join([k + '=?' for k, v in data_filter]),
            )
        else:
            q += ';'
        return q, [v for _, v in data] + [v for _, v in data_filter]
