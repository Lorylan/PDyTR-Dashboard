# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sensor.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0csensor.proto\"\x07\n\x05\x45mpty\"\x1f\n\x0eSensorResponse\x12\r\n\x05value\x18\x01 \x01(\x03\x32\x30\n\x06Sensor\x12&\n\x07getData\x12\x06.Empty\x1a\x0f.SensorResponse\"\x00\x30\x01\x62\x06proto3')



_EMPTY = DESCRIPTOR.message_types_by_name['Empty']
_SENSORRESPONSE = DESCRIPTOR.message_types_by_name['SensorResponse']
Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'sensor_pb2'
  # @@protoc_insertion_point(class_scope:Empty)
  })
_sym_db.RegisterMessage(Empty)

SensorResponse = _reflection.GeneratedProtocolMessageType('SensorResponse', (_message.Message,), {
  'DESCRIPTOR' : _SENSORRESPONSE,
  '__module__' : 'sensor_pb2'
  # @@protoc_insertion_point(class_scope:SensorResponse)
  })
_sym_db.RegisterMessage(SensorResponse)

_SENSOR = DESCRIPTOR.services_by_name['Sensor']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTY._serialized_start=16
  _EMPTY._serialized_end=23
  _SENSORRESPONSE._serialized_start=25
  _SENSORRESPONSE._serialized_end=56
  _SENSOR._serialized_start=58
  _SENSOR._serialized_end=106
# @@protoc_insertion_point(module_scope)
