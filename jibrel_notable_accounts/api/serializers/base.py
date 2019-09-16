from typing import Dict, Any, List, NoReturn

from marshmallow import Schema as MarshmallowSchema
from marshmallow import ValidationError
from marshmallow.marshalling import SCHEMA

from jibrel_notable_accounts.api.utils.api_error import ApiError
from jibrel_notable_accounts.api.utils.error_code import ErrorCode


class ApiErrorSchema(MarshmallowSchema):
    def handle_error(self, exc: ValidationError, data: Dict[str, Any]) -> None:
        convert_to_api_error_and_raise(exc)


def convert_to_api_error_and_raise(exc: ValidationError) -> NoReturn:
    raise ApiError(errors=get_flatten_error_messages(exc.messages), status=400)


def get_flatten_error_messages(messages: Dict[str, List[str]]) -> List[Dict[str, str]]:
    flatten_messages = []

    for field, msgs in messages.items():
        for msg in msgs:
            message = {'field': get_field(field), 'message': msg, 'code': get_error_code(field)}
            flatten_messages.append(message)

    return flatten_messages


def get_field(field: str) -> str:
    if field == SCHEMA:
        return '__all__'

    return field


def get_error_code(field: str) -> str:
    if field == SCHEMA:
        return ErrorCode.VALIDATION_ERROR

    return ErrorCode.INVALID_VALUE
