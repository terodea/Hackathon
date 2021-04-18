import subprocess
import sys
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from marshmallow import Schema, fields
    from marshmallow.validate import Length
except ModuleNotFoundError:
    install("marshmallow")
    from marshmallow import Schema, fields
    from marshmallow.validate import Length


class ValidateDataModel(Schema):
    """
    Data Modle Validation module.
    """
    title = fields.Str(required=True, error_messages={"required": "title is required."},validate=Length(max=100, min=5))
    image_path = fields.Str(required=False, validate=Length(max=100))
    description = fields.Str(required=False, validate=Length(max=255))
    discount_price = fields.Int(required=True, error_messages={"required": "discount_price is required."})
    price = fields.Int(required=True, error_messages={"required": "price is required."})
    on_discount = fields.Boolean(required=True, error_messages={"required": "on_discount is required."})
    id = fields.Int(required=False)

class TestValidateDataModel(Schema):
    """
    Data Modle Validation module.
    """
    title = fields.Str(required=True, error_messages={"required": "title is required."},validate=Length(max=100, min=5))
    image_path = fields.Str(required=False, validate=Length(max=100))
    description = fields.Str(required=False, validate=Length(max=255))
    discount_price = fields.Int(required=True, error_messages={"required": "discount_price is required."})
    price = fields.Int(required=True, error_messages={"required": "price is required."})
    on_discount = fields.Boolean(required=True, error_messages={"required": "on_discount is required."})
    id = fields.Int(required=False)
    date_created = fields.Str(required=True, error_messages={"required": "date_created is required."})
    date_updated = fields.Str(required=True, error_messages={"required": "date_updated is required."})
