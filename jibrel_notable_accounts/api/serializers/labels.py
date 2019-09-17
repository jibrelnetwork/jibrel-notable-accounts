from typing import Dict, Any, Iterable

import webargs.fields
from marshmallow import fields, post_dump

from jibrel_notable_accounts.api.serializers.base import ApiErrorSchema


class LabelListQueryParams(ApiErrorSchema):
    addresses = webargs.fields.DelimitedList(fields.Str(), load_from='address')


class Label(ApiErrorSchema):
    name = fields.Str()
    address = fields.Str()
    labels = fields.List(fields.Str())

    @post_dump(pass_many=True)
    def convert_to_dict(self, data: Iterable[Dict[str, Any]], **kwargs: Any) -> Dict[str, Any]:
        converted = dict()

        for item in data:
            converted[item['address']] = {
                'name': item['name'],
                'labels': item['labels'],
            }

        return converted
