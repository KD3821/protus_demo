# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: payments.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0epayments.proto"2\n\x0e\x41\x63\x63ountRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12\r\n\x05owner\x18\x02 \x01(\t")\n\x0f\x41\x63\x63ountResponse\x12\x16\n\x0e\x61\x63\x63ount_number\x18\x01 \x01(\t"G\n\x11\x41\x63\x63ountingRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x10\n\x08username\x18\x03 \x01(\t"N\n\rChargeRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12\x12\n\nservice_id\x18\x02 \x01(\t\x12\x16\n\x0e\x61\x63\x63ount_number\x18\x03 \x01(\t"\x8d\x01\n\x0e\x43hargeResponse\x12\x12\n\nservice_id\x18\x01 \x01(\t\x12\x14\n\x0cservice_name\x18\x02 \x01(\t\x12\x16\n\x0e\x61\x63\x63ount_number\x18\x03 \x01(\t\x12\x16\n\x0einvoice_number\x18\x04 \x01(\t\x12\x11\n\tissued_at\x18\x05 \x01(\x03\x12\x0e\n\x06\x61mount\x18\x06 \x01(\x02\x32\xb5\x01\n\rPaymentsProto\x12\x34\n\rCreateAccount\x12\x0f.AccountRequest\x1a\x10.AccountResponse"\x00\x12:\n\x10\x43reateAccounting\x12\x12.AccountingRequest\x1a\x10.AccountResponse"\x00\x12\x32\n\rChargeAccount\x12\x0e.ChargeRequest\x1a\x0f.ChargeResponse"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "payments_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_ACCOUNTREQUEST"]._serialized_start = 18
    _globals["_ACCOUNTREQUEST"]._serialized_end = 68
    _globals["_ACCOUNTRESPONSE"]._serialized_start = 70
    _globals["_ACCOUNTRESPONSE"]._serialized_end = 111
    _globals["_ACCOUNTINGREQUEST"]._serialized_start = 113
    _globals["_ACCOUNTINGREQUEST"]._serialized_end = 184
    _globals["_CHARGEREQUEST"]._serialized_start = 186
    _globals["_CHARGEREQUEST"]._serialized_end = 264
    _globals["_CHARGERESPONSE"]._serialized_start = 267
    _globals["_CHARGERESPONSE"]._serialized_end = 408
    _globals["_PAYMENTSPROTO"]._serialized_start = 411
    _globals["_PAYMENTSPROTO"]._serialized_end = 592
# @@protoc_insertion_point(module_scope)
