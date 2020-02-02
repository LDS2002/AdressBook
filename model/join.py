from model.model import Model


class Join(Model):

    def __init__(self, model_a, model_b, field_name_a, field_name_b, **kwargs):
        self.model_a = model_a
        self.model_b = model_b
        self.field_name_a = field_name_a
        self.field_name_b = field_name_b
        model_name_a = model_a.get_model_name()
        model_name_b = model_b.get_model_name()
        fields_a = model_a.get_fields()
        fields_a = [
            f.add_prefix(model_name_a)
            for f in fields_a
            if f .get_name() != field_name_a
        ]
        fields_b = model_b.get_fields()
        fields_b = [
            f.add_prefix(model_name_b)
            for f in fields_b
            if f.get_name() != field_name_b
        ]
        self._fields = fields_a + fields_b
        self._model_name = "%s LEFT JOIN %s ON %s.%s=%s.%s" % (
            model_name_a,
            model_name_b,
            model_name_a,
            field_name_a,
            model_name_b,
            field_name_b,
        )
        super().__init__(**kwargs)

    def get_model_name(self):
        return self._model_name

    def get_fields(self):
        return self._fields
