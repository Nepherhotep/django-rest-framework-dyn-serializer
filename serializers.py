from rest_framework import serializers


class DynModelSerializer(serializers.ModelSerializer):
    """
    Factory to include/exclude fields dynamically
    """

    def __init__(self, *args, **kwargs):
        self._requested_fields = []

        s_type = type(self)
        assert hasattr(self.Meta, 'model'), '{} Meta.model param is required'.format(s_type)

        if hasattr(self.Meta, 'default_fields'):
            self.default_fields = self.Meta.default_fields
        else:
            self.default_fields = ['id']

        assert hasattr(self.Meta, 'fields'), \
            '{} Meta.fields param cannot be empty'.format(s_type)
        assert hasattr(self.Meta, 'fields_param'), \
            '{} Meta.fields_param param cannot be empty'.format(s_type)

        for field_name in self.default_fields:
            assert field_name in self.Meta.fields, '{} Meta.default_fields contains field not in' \
                                                   'Meta.fields list'

        super(DynModelSerializer, self).__init__(*args, **kwargs)

        request = self.context.get('request')
        if request:
            self.limit_fields(request)

            for field_name, field_name in self.fields.items():
                # assigning parent context to allow child serializers to update their fields later
                field_name.context = self.context

    def limit_fields(self, request):
        field_names = self._get_requested_field_names(request)
        self._requested_fields = field_names

        if field_names is not None:
            # Drop any fields that are not specified in passed query param
            allowed = set(field_names)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

            for field_name in self.fields:
                field = self.fields[field_name]
                if isinstance(field, DynModelSerializer):
                    field.limit_fields(request)

    def _get_requested_field_names(self, request):
        fields_param_value = request.query_params.get(self.Meta.fields_param)
        if fields_param_value is not None:
            requested_fields = fields_param_value.split(',')
            if requested_fields:
                return list(set(self.Meta.fields).intersection(set(requested_fields)))
        return self.default_fields

    def get_field_names(self, declared_fields, info):
        """
        Return only requested and allowed field names
        """
        return self._requested_fields

    class Meta:
        model = None
        fields = []
        default_fields = []
        fields_param = None
