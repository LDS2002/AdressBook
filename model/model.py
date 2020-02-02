class Model:

    def __init__(self, *args, **kwargs):
        fields = self.get_fields_names()
        prefixes = [
            self.get_model_name().lower() + '_',
            self.get_model_name() + '.',
        ]
        for f in fields:
            self.__dict__[f] = None
            if f in kwargs.keys():
                self.__dict__[f] = kwargs[f]
            for prefix in prefixes:
                if prefix + f in kwargs.keys():
                    self.__dict__[f] = kwargs[prefix + f]
        for i, arg in enumerate(args):
            if i >= len(fields):
                break
            self.__dict__[fields[i]] = args[i]

    @staticmethod
    def get_fields():
        return []

    def get_fields_dict(self):
        return {f.get_name(): f.get_description() for f in self.get_fields()}

    def get_fields_names(self):
        return [f.get_name() for f in self.get_fields()]

    @staticmethod
    def get_model_name():
        pass

    def get_data(self):
        d = self.to_dict()
        res = [(k, v) for k, v in d.items() if v is not None]
        return res

    def __str__(self):
        fields = self.get_fields_names()
        return '{' + ', '.join([
            f + ' : ' + str(self.__dict__[f])
            for f in fields
        ]) + '}'

    def to_dict(self):
        d = dict()
        fields = self.get_fields_names()
        for f in fields:
            d[f] = self.__dict__[f]
        return d

    def to_compressed_dict(self):
        return {k: v for k, v in self.to_dict().items() if v is not None}

    def copy(self, *args, **kwargs):
        d = self.__dict__
        d.update(kwargs)
        return type(self)(*args, **d)


class Field:

    def __init__(self, name, description, validation_type=None):
        self._name = name
        self._description = description
        self._validation_type = validation_type

    def get_validation_type(self):
        return self._validation_type

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def add_prefix(self, prefix):
        self._name = prefix + '.' + self._name
        return self
