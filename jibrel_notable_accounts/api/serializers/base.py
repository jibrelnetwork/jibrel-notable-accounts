import functools
from typing import Dict, Any, List, NoReturn, Union

from marshmallow import Schema
from marshmallow import ValidationError
from marshmallow.exceptions import SCHEMA

from jibrel_notable_accounts.api.utils.api_error import ApiError
from jibrel_notable_accounts.api.utils.error_code import ErrorCode


class ApiErrorSchema(Schema):
    def handle_error(self, error: ValidationError, data: Dict[str, Any], *, many: bool, **kwargs: Any) -> NoReturn:
        convert_to_api_error_and_raise(error)


def convert_to_api_error_and_raise(exc: ValidationError) -> NoReturn:
    raise ApiError(errors=get_flatten_error_messages(exc.messages), status=400)


def get_flatten_error_messages(messages: Union[List[Any], Dict[Any, Any]]) -> List[Dict[str, str]]:
    """
    >>> get_flatten_error_messages(['Whole schema is bad.']) == [
    ...     {'field': '__all__', 'message': 'Whole schema is bad.', 'code': 'VALIDATION_ERROR'}
    ... ]
    True
    >>> get_flatten_error_messages({'_schema': ['Everything is bad.']}) == [
    ...     {'field': '__all__', 'message': 'Everything is bad.', 'code': 'VALIDATION_ERROR'}
    ... ]
    True
    >>> get_flatten_error_messages({'value': ['Not a valid value.']}) == [
    ...     {'field': 'value', 'message': 'Not a valid value.', 'code': 'INVALID_VALUE'}
    ... ]
    True
    >>> get_flatten_error_messages({'f': {0: ['One.', 'Error.'], 1: ['Another.', 'Error.']}}) == [
    ...     {'field': 'f', 'message': 'One.', 'code': 'INVALID_VALUE'},
    ...     {'field': 'f', 'message': 'Error.', 'code': 'INVALID_VALUE'},
    ...     {'field': 'f', 'message': 'Another.', 'code': 'INVALID_VALUE'},
    ...     {'field': 'f', 'message': 'Error.', 'code': 'INVALID_VALUE'},
    ... ]
    True
    >>> get_flatten_error_messages({'field_with_multiple_errors': ['Error one.', 'Error two.']}) == [
    ...     {'field': 'field_with_multiple_errors', 'message': 'Error one.', 'code': 'INVALID_VALUE'},
    ...     {'field': 'field_with_multiple_errors', 'message': 'Error two.', 'code': 'INVALID_VALUE'},
    ... ]
    True
    """
    if isinstance(messages, list):
        return [{'field': '__all__', 'message': msg, 'code': ErrorCode.VALIDATION_ERROR} for msg in messages]

    flatten_messages = []

    for field, msgs in messages.items():
        if isinstance(msgs, dict):
            msgs = functools.reduce(lambda x, y: x + y, msgs.values(), [])

        for msg in msgs:
            message = {'field': _get_field(field), 'message': msg, 'code': _get_error_code(field)}
            flatten_messages.append(message)

    return flatten_messages


def _get_field(field: str) -> str:
    if field == SCHEMA:
        return '__all__'

    return field


def _get_error_code(field: str) -> str:
    if field == SCHEMA:
        return ErrorCode.VALIDATION_ERROR

    return ErrorCode.INVALID_VALUE
