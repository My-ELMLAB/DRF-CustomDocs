from rest_framework.schemas.openapi import SchemaGenerator, AutoSchema

import re
from rest_framework.settings import api_settings

from django.http import HttpRequest
from django.contrib.auth.models import User


header_regex = re.compile('^[a-zA-Z][0-9A-Za-z_]*:')

class AutoDescribeSchema(AutoSchema):

    def get_operation(self, path, method):
        self.view.request = HttpRequest()
        self.view.request.method = getattr(self.view, 'action', method).upper()
        self.view.request.user = User.objects.first()
        operation = super().get_operation(path, method)
        operation['description'] = self.get_description(path, method)
        return operation

    def get_description(self, path, method):
        """
        Determine a link description.
        This will be based on the method docstring if one exists,
        or else the class docstring.
        """
        view = self.view

        method_name = getattr(view, 'action', method.lower())
        method_docstring = getattr(view, method_name, None).__doc__
        if method_docstring:
            # An explicit docstring on the method or action.
            return self._get_description_section(view, method.lower(), formatting.dedent(smart_text(method_docstring)))
        else:
            return self._get_description_section(view, getattr(view, 'action', method.lower()), view.get_view_description())

    def _get_description_section(self, view, header, description):
        lines = [line for line in description.splitlines()]
        current_section = ''
        sections = {'': ''}

        line_number = 0
        for line in lines:
            # Count line number
            line_number += 1
            if header_regex.match(line):
                current_section, seperator, lead = line.partition(':')
                sections[current_section] = lead.strip()
            else:
                if line_number > 1:
                    # Only break starting from second line
                    sections[current_section] += '<br>'
                sections[current_section] += line

        # TODO: SCHEMA_COERCE_METHOD_NAMES appears here and in `SchemaGenerator.get_keys`
        coerce_method_names = api_settings.SCHEMA_COERCE_METHOD_NAMES
        if header in sections:
            return sections[header].strip()
        if header in coerce_method_names:
            if coerce_method_names[header] in sections:
                return sections[coerce_method_names[header]].strip()
        return sections[''].strip()

    # Support multilanguage in field descriptions
    def _map_serializer(self, serializer):
        mapping = super()._map_serializer(serializer)
        fields = mapping.get('properties')
        
        for field_name, schema in fields.items():
            if 'description' in schema.keys():
                description = schema.get('description')
                lines = [line for line in description.splitlines()]
                
                description = '<br>'.join(lines)
                    
                fields[field_name]['description'] = description

        mapping['properties'] = fields
        return mapping
