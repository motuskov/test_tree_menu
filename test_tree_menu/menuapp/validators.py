'''
Implements custom validators for model fields.
'''
from django.core.exceptions import ValidationError
from django.urls import (
    resolve,
    reverse,
    Resolver404,
    NoReverseMatch,
)


def validate_path(value: str) -> None:
    '''
    Checks if "value" (path or path name) exists in the project.
    '''
    # Path doesn't need, return
    if not value:
        return

    # Check path or path name existence
    try:
        if value.startswith('/'):
            resolve(value)
        else:
            reverse(value)
    except Resolver404:
        raise ValidationError(
            'The given path does not exist.'
        )
    except NoReverseMatch:
        raise ValidationError(
            'A path with the given name does not exist.'
        )
