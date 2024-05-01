# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: polls.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import users_pb2 as users__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bpolls.proto\x1a\x0busers.proto\";\n\x04Vote\x12\x0f\n\x07poll_id\x18\x01 \x01(\x05\x12\x11\n\toption_id\x18\x02 \x01(\x05\x12\x0f\n\x07user_id\x18\x03 \x01(\x05\"E\n\x0bPollOptions\x12\x0f\n\x02id\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x10\n\x08quantity\x18\x02 \x01(\x05\x12\x0c\n\x04text\x18\x03 \x01(\tB\x05\n\x03_id\"Z\n\x04Poll\x12\x0f\n\x02id\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0c\n\x04text\x18\x03 \x01(\t\x12\x1d\n\x07options\x18\x04 \x03(\x0b\x32\x0c.PollOptionsB\x05\n\x03_id\"n\n\rGetPollsReply\x12(\n\x05polls\x18\x01 \x03(\x0b\x32\x19.GetPollsReply.PollsEntry\x1a\x33\n\nPollsEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\x14\n\x05value\x18\x02 \x01(\x0b\x32\x05.Poll:\x02\x38\x01\"7\n\x0bPollRequest\x12\x13\n\x04user\x18\x01 \x01(\x0b\x32\x05.User\x12\x13\n\x04poll\x18\x02 \x01(\x0b\x32\x05.Poll2\x93\x02\n\x05Polls\x12$\n\x08GetPolls\x12\x06.Empty\x1a\x0e.GetPollsReply\"\x00\x12#\n\nCreatePoll\x12\x0c.PollRequest\x1a\x05.Poll\"\x00\x12$\n\nDeletePoll\x12\x0c.PollRequest\x1a\x06.Empty\"\x00\x12\x1e\n\x04Vote\x12\x0c.PollRequest\x1a\x06.Empty\"\x00\x12 \n\x06Unvote\x12\x0c.PollRequest\x1a\x06.Empty\"\x00\x12.\n\x13GetPollsVotedByUser\x12\x05.User\x1a\x0e.GetPollsReply\"\x00\x12\'\n\x0cGetUserPolls\x12\x05.User\x1a\x0e.GetPollsReply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'polls_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_GETPOLLSREPLY_POLLSENTRY']._options = None
  _globals['_GETPOLLSREPLY_POLLSENTRY']._serialized_options = b'8\001'
  _globals['_VOTE']._serialized_start=28
  _globals['_VOTE']._serialized_end=87
  _globals['_POLLOPTIONS']._serialized_start=89
  _globals['_POLLOPTIONS']._serialized_end=158
  _globals['_POLL']._serialized_start=160
  _globals['_POLL']._serialized_end=250
  _globals['_GETPOLLSREPLY']._serialized_start=252
  _globals['_GETPOLLSREPLY']._serialized_end=362
  _globals['_GETPOLLSREPLY_POLLSENTRY']._serialized_start=311
  _globals['_GETPOLLSREPLY_POLLSENTRY']._serialized_end=362
  _globals['_POLLREQUEST']._serialized_start=364
  _globals['_POLLREQUEST']._serialized_end=419
  _globals['_POLLS']._serialized_start=422
  _globals['_POLLS']._serialized_end=697
# @@protoc_insertion_point(module_scope)