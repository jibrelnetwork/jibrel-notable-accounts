from marshmallow.fields import List, Str

from jibrel_notable_accounts.api.serializers.base import ApiErrorSchema


class LabelListSchema(ApiErrorSchema):
    addresses = List(Str())
