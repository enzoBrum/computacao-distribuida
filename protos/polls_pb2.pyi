import users_pb2 as _users_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VoteInfo(_message.Message):
    __slots__ = ("id_user", "id_option")
    ID_USER_FIELD_NUMBER: _ClassVar[int]
    ID_OPTION_FIELD_NUMBER: _ClassVar[int]
    id_user: int
    id_option: int
    def __init__(self, id_user: _Optional[int] = ..., id_option: _Optional[int] = ...) -> None: ...

class PollOptions(_message.Message):
    __slots__ = ("id", "text", "votes")
    ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    VOTES_FIELD_NUMBER: _ClassVar[int]
    id: int
    text: str
    votes: int
    def __init__(self, id: _Optional[int] = ..., text: _Optional[str] = ..., votes: _Optional[int] = ...) -> None: ...

class Poll(_message.Message):
    __slots__ = ("id", "title", "text", "options")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    text: str
    options: _containers.RepeatedCompositeFieldContainer[PollOptions]
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., text: _Optional[str] = ..., options: _Optional[_Iterable[_Union[PollOptions, _Mapping]]] = ...) -> None: ...

class GetPollsReply(_message.Message):
    __slots__ = ("polls",)
    POLLS_FIELD_NUMBER: _ClassVar[int]
    polls: _containers.RepeatedCompositeFieldContainer[Poll]
    def __init__(self, polls: _Optional[_Iterable[_Union[Poll, _Mapping]]] = ...) -> None: ...

class PollRequest(_message.Message):
    __slots__ = ("user", "poll")
    USER_FIELD_NUMBER: _ClassVar[int]
    POLL_FIELD_NUMBER: _ClassVar[int]
    user: _users_pb2.User
    poll: Poll
    def __init__(self, user: _Optional[_Union[_users_pb2.User, _Mapping]] = ..., poll: _Optional[_Union[Poll, _Mapping]] = ...) -> None: ...
