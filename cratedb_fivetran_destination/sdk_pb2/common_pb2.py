# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: common.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x63ommon.proto\x12\x0f\x66ivetran_sdk.v2\x1a\x1fgoogle/protobuf/timestamp.proto\"\x1a\n\x18\x43onfigurationFormRequest\"\xc1\x01\n\x19\x43onfigurationFormResponse\x12\"\n\x1aschema_selection_supported\x18\x01 \x01(\x08\x12!\n\x19table_selection_supported\x18\x02 \x01(\x08\x12*\n\x06\x66ields\x18\x03 \x03(\x0b\x32\x1a.fivetran_sdk.v2.FormField\x12\x31\n\x05tests\x18\x04 \x03(\x0b\x32\".fivetran_sdk.v2.ConfigurationTest\"\xba\x03\n\tFormField\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05label\x18\x02 \x01(\t\x12\x15\n\x08required\x18\x03 \x01(\x08H\x01\x88\x01\x01\x12\x18\n\x0b\x64\x65scription\x18\x04 \x01(\tH\x02\x88\x01\x01\x12\x30\n\ntext_field\x18\x05 \x01(\x0e\x32\x1a.fivetran_sdk.v2.TextFieldH\x00\x12\x38\n\x0e\x64ropdown_field\x18\x06 \x01(\x0b\x32\x1e.fivetran_sdk.v2.DropdownFieldH\x00\x12\x34\n\x0ctoggle_field\x18\x07 \x01(\x0b\x32\x1c.fivetran_sdk.v2.ToggleFieldH\x00\x12@\n\x12\x63onditional_fields\x18\n \x01(\x0b\x32\".fivetran_sdk.v2.ConditionalFieldsH\x00\x12\x1a\n\rdefault_value\x18\x08 \x01(\tH\x03\x88\x01\x01\x12\x18\n\x0bplaceholder\x18\t \x01(\tH\x04\x88\x01\x01\x42\x06\n\x04typeB\x0b\n\t_requiredB\x0e\n\x0c_descriptionB\x10\n\x0e_default_valueB\x0e\n\x0c_placeholder\"x\n\x11\x43onditionalFields\x12\x37\n\tcondition\x18\x01 \x01(\x0b\x32$.fivetran_sdk.v2.VisibilityCondition\x12*\n\x06\x66ields\x18\x02 \x03(\x0b\x32\x1a.fivetran_sdk.v2.FormField\"\x83\x01\n\x13VisibilityCondition\x12\x17\n\x0f\x63ondition_field\x18\x01 \x01(\t\x12\x14\n\nbool_value\x18\x02 \x01(\x08H\x00\x12\x16\n\x0cstring_value\x18\x03 \x01(\tH\x00\x12\x15\n\x0b\x65mpty_value\x18\x04 \x01(\x08H\x00\x42\x0e\n\x0cvisible_when\"\'\n\rDropdownField\x12\x16\n\x0e\x64ropdown_field\x18\x01 \x03(\t\"\r\n\x0bToggleField\"0\n\x11\x43onfigurationTest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05label\x18\x02 \x01(\t\"\x99\x01\n\x0bTestRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x46\n\rconfiguration\x18\x02 \x03(\x0b\x32/.fivetran_sdk.v2.TestRequest.ConfigurationEntry\x1a\x34\n\x12\x43onfigurationEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"@\n\x0cTestResponse\x12\x11\n\x07success\x18\x01 \x01(\x08H\x00\x12\x11\n\x07\x66\x61ilure\x18\x02 \x01(\tH\x00\x42\n\n\x08response\"6\n\nSchemaList\x12(\n\x07schemas\x18\x01 \x03(\x0b\x32\x17.fivetran_sdk.v2.Schema\"3\n\tTableList\x12&\n\x06tables\x18\x01 \x03(\x0b\x32\x16.fivetran_sdk.v2.Table\">\n\x06Schema\x12\x0c\n\x04name\x18\x01 \x01(\t\x12&\n\x06tables\x18\x02 \x03(\x0b\x32\x16.fivetran_sdk.v2.Table\"k\n\x0e\x44\x61taTypeParams\x12\x31\n\x07\x64\x65\x63imal\x18\x01 \x01(\x0b\x32\x1e.fivetran_sdk.v2.DecimalParamsH\x00\x12\x1c\n\x12string_byte_length\x18\x02 \x01(\x05H\x00\x42\x08\n\x06params\"1\n\rDecimalParams\x12\x11\n\tprecision\x18\x01 \x01(\r\x12\r\n\x05scale\x18\x02 \x01(\r\"\xab\x03\n\tValueType\x12\x0e\n\x04null\x18\x01 \x01(\x08H\x00\x12\x0e\n\x04\x62ool\x18\x02 \x01(\x08H\x00\x12\x0f\n\x05short\x18\x03 \x01(\x05H\x00\x12\r\n\x03int\x18\x04 \x01(\x05H\x00\x12\x0e\n\x04long\x18\x05 \x01(\x03H\x00\x12\x0f\n\x05\x66loat\x18\x06 \x01(\x02H\x00\x12\x10\n\x06\x64ouble\x18\x07 \x01(\x01H\x00\x12\x30\n\nnaive_date\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00\x12\x34\n\x0enaive_datetime\x18\t \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00\x12\x32\n\x0cutc_datetime\x18\n \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00\x12\x11\n\x07\x64\x65\x63imal\x18\x0b \x01(\tH\x00\x12\x10\n\x06\x62inary\x18\x0c \x01(\x0cH\x00\x12\x10\n\x06string\x18\r \x01(\tH\x00\x12\x0e\n\x04json\x18\x0e \x01(\tH\x00\x12\r\n\x03xml\x18\x0f \x01(\tH\x00\x12\x30\n\nnaive_time\x18\x10 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00\x42\x07\n\x05inner\"?\n\x05Table\x12\x0c\n\x04name\x18\x01 \x01(\t\x12(\n\x07\x63olumns\x18\x02 \x03(\x0b\x32\x17.fivetran_sdk.v2.Column\"\x95\x01\n\x06\x43olumn\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\'\n\x04type\x18\x02 \x01(\x0e\x32\x19.fivetran_sdk.v2.DataType\x12\x13\n\x0bprimary_key\x18\x03 \x01(\x08\x12\x34\n\x06params\x18\x04 \x01(\x0b\x32\x1f.fivetran_sdk.v2.DataTypeParamsH\x00\x88\x01\x01\x42\t\n\x07_params\"\x1a\n\x07Warning\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x17\n\x04Task\x12\x0f\n\x07message\x18\x01 \x01(\t*4\n\tTextField\x12\r\n\tPlainText\x10\x00\x12\x0c\n\x08Password\x10\x01\x12\n\n\x06Hidden\x10\x02*\xdb\x01\n\x08\x44\x61taType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07\x42OOLEAN\x10\x01\x12\t\n\x05SHORT\x10\x02\x12\x07\n\x03INT\x10\x03\x12\x08\n\x04LONG\x10\x04\x12\x0b\n\x07\x44\x45\x43IMAL\x10\x05\x12\t\n\x05\x46LOAT\x10\x06\x12\n\n\x06\x44OUBLE\x10\x07\x12\x0e\n\nNAIVE_DATE\x10\x08\x12\x12\n\x0eNAIVE_DATETIME\x10\t\x12\x10\n\x0cUTC_DATETIME\x10\n\x12\n\n\x06\x42INARY\x10\x0b\x12\x07\n\x03XML\x10\x0c\x12\n\n\x06STRING\x10\r\x12\x08\n\x04JSON\x10\x0e\x12\x0e\n\nNAIVE_TIME\x10\x0f*>\n\nRecordType\x12\n\n\x06UPSERT\x10\x00\x12\n\n\x06UPDATE\x10\x01\x12\n\n\x06\x44\x45LETE\x10\x02\x12\x0c\n\x08TRUNCATE\x10\x03\x42\"H\x01P\x01Z\x1c\x66ivetran.com/fivetran_sdk_v2b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'common_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'H\001P\001Z\034fivetran.com/fivetran_sdk_v2'
  _globals['_TESTREQUEST_CONFIGURATIONENTRY']._options = None
  _globals['_TESTREQUEST_CONFIGURATIONENTRY']._serialized_options = b'8\001'
  _globals['_TEXTFIELD']._serialized_start=2352
  _globals['_TEXTFIELD']._serialized_end=2404
  _globals['_DATATYPE']._serialized_start=2407
  _globals['_DATATYPE']._serialized_end=2626
  _globals['_RECORDTYPE']._serialized_start=2628
  _globals['_RECORDTYPE']._serialized_end=2690
  _globals['_CONFIGURATIONFORMREQUEST']._serialized_start=66
  _globals['_CONFIGURATIONFORMREQUEST']._serialized_end=92
  _globals['_CONFIGURATIONFORMRESPONSE']._serialized_start=95
  _globals['_CONFIGURATIONFORMRESPONSE']._serialized_end=288
  _globals['_FORMFIELD']._serialized_start=291
  _globals['_FORMFIELD']._serialized_end=733
  _globals['_CONDITIONALFIELDS']._serialized_start=735
  _globals['_CONDITIONALFIELDS']._serialized_end=855
  _globals['_VISIBILITYCONDITION']._serialized_start=858
  _globals['_VISIBILITYCONDITION']._serialized_end=989
  _globals['_DROPDOWNFIELD']._serialized_start=991
  _globals['_DROPDOWNFIELD']._serialized_end=1030
  _globals['_TOGGLEFIELD']._serialized_start=1032
  _globals['_TOGGLEFIELD']._serialized_end=1045
  _globals['_CONFIGURATIONTEST']._serialized_start=1047
  _globals['_CONFIGURATIONTEST']._serialized_end=1095
  _globals['_TESTREQUEST']._serialized_start=1098
  _globals['_TESTREQUEST']._serialized_end=1251
  _globals['_TESTREQUEST_CONFIGURATIONENTRY']._serialized_start=1199
  _globals['_TESTREQUEST_CONFIGURATIONENTRY']._serialized_end=1251
  _globals['_TESTRESPONSE']._serialized_start=1253
  _globals['_TESTRESPONSE']._serialized_end=1317
  _globals['_SCHEMALIST']._serialized_start=1319
  _globals['_SCHEMALIST']._serialized_end=1373
  _globals['_TABLELIST']._serialized_start=1375
  _globals['_TABLELIST']._serialized_end=1426
  _globals['_SCHEMA']._serialized_start=1428
  _globals['_SCHEMA']._serialized_end=1490
  _globals['_DATATYPEPARAMS']._serialized_start=1492
  _globals['_DATATYPEPARAMS']._serialized_end=1599
  _globals['_DECIMALPARAMS']._serialized_start=1601
  _globals['_DECIMALPARAMS']._serialized_end=1650
  _globals['_VALUETYPE']._serialized_start=1653
  _globals['_VALUETYPE']._serialized_end=2080
  _globals['_TABLE']._serialized_start=2082
  _globals['_TABLE']._serialized_end=2145
  _globals['_COLUMN']._serialized_start=2148
  _globals['_COLUMN']._serialized_end=2297
  _globals['_WARNING']._serialized_start=2299
  _globals['_WARNING']._serialized_end=2325
  _globals['_TASK']._serialized_start=2327
  _globals['_TASK']._serialized_end=2350
# @@protoc_insertion_point(module_scope)
