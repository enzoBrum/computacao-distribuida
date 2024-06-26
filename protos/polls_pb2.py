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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bpolls.proto\x1a\x0busers.proto\".\n\x08VoteInfo\x12\x0f\n\x07id_user\x18\x01 \x01(\x05\x12\x11\n\tid_option\x18\x02 \x01(\x05\"Q\n\x0bPollOptions\x12\x0f\n\x02id\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x0c\n\x04text\x18\x02 \x01(\t\x12\x12\n\x05votes\x18\x03 \x01(\x05H\x01\x88\x01\x01\x42\x05\n\x03_idB\x08\n\x06_votes\"Z\n\x04Poll\x12\x0f\n\x02id\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0c\n\x04text\x18\x03 \x01(\t\x12\x1d\n\x07options\x18\x04 \x03(\x0b\x32\x0c.PollOptionsB\x05\n\x03_id\"%\n\rGetPollsReply\x12\x14\n\x05polls\x18\x01 \x03(\x0b\x32\x05.Poll\"7\n\x0bPollRequest\x12\x13\n\x04user\x18\x01 \x01(\x0b\x32\x05.User\x12\x13\n\x04poll\x18\x02 \x01(\x0b\x32\x05.Poll2\xaa\x02\n\x05Polls\x12$\n\x08GetPolls\x12\x06.Empty\x1a\x0e.GetPollsReply\"\x00\x12#\n\nCreatePoll\x12\x0c.PollRequest\x1a\x05.Poll\"\x00\x12$\n\nDeletePoll\x12\x0c.PollRequest\x1a\x06.Empty\"\x00\x12\x1b\n\x04Vote\x12\t.VoteInfo\x1a\x06.Empty\"\x00\x12\x1d\n\x06Unvote\x12\t.VoteInfo\x1a\x06.Empty\"\x00\x12.\n\x13GetPollsVotedByUser\x12\x05.User\x1a\x0e.GetPollsReply\"\x00\x12\'\n\x0cGetUserPolls\x12\x05.User\x1a\x0e.GetPollsReply\"\x00\x12\x1b\n\tGetPollID\x12\x05.Poll\x1a\x05.Poll\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'polls_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_VOTEINFO']._serialized_start=28
  _globals['_VOTEINFO']._serialized_end=74
  _globals['_POLLOPTIONS']._serialized_start=76
  _globals['_POLLOPTIONS']._serialized_end=157
  _globals['_POLL']._serialized_start=159
  _globals['_POLL']._serialized_end=249
  _globals['_GETPOLLSREPLY']._serialized_start=251
  _globals['_GETPOLLSREPLY']._serialized_end=288
  _globals['_POLLREQUEST']._serialized_start=290
  _globals['_POLLREQUEST']._serialized_end=345
  _globals['_POLLS']._serialized_start=348
  _globals['_POLLS']._serialized_end=646
# @@protoc_insertion_point(module_scope)
