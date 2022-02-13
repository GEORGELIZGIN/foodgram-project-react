import re
from django.core.exceptions import ValidationError


def validate_tag_color(color):
    r = r'#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})'
    if not re.fullmatch(r, color):
        raise ValidationError(
            'color must have HEX format')
