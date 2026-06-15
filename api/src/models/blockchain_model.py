from marshmallow import Schema, fields, validate


class OwnershipModel(Schema):
    org_id = fields.String(required=True)
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))


class TransferRecordModel(Schema):
    from_org_id = fields.String(required=True)
    to_org_id = fields.String(required=True)
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))
    timestamp = fields.String(required=True)
    metadata = fields.Dict(required=True)


class BatchModel(Schema):
    batch_id = fields.String(required=True)
    product_name = fields.String(required=True)
    manufacture_date = fields.String(required=True)
    expiry_date = fields.String(required=True)
    total_quantity = fields.Integer(required=True)
    unit_dosage = fields.String(required=True)
    status = fields.String(required=True)
    ownerships = fields.List(fields.Nested(OwnershipModel))
    last_transfer = fields.Nested(TransferRecordModel, allow_none=True)
    transfers = fields.List(fields.Nested(TransferRecordModel))
    created_at = fields.String(allow_none=True)
    updated_at = fields.String(allow_none=True)


batch_output = BatchModel()
batch_list_output = BatchModel(many=True)


class CreateBatchDTO(Schema):
    batch_id = fields.String(required=True)
    product_name = fields.String(required=True)
    manufacture_date = fields.String(required=True)
    expiry_date = fields.String(required=True)
    total_quantity = fields.Integer(required=True, validate=validate.Range(min=1))
    unit_dosage = fields.String(required=True)
    unit_price = fields.Float(required=True, validate=validate.Range(min=0.01))
    owner_org_id = fields.String(required=True)


class TransferBatchDTO(Schema):
    batch_id = fields.String(required=True)
    from_org_id = fields.String(required=True)
    to_org_id = fields.String(required=True)
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))
    metadata = fields.Dict(required=False)

