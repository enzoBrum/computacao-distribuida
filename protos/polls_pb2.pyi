import users_pb2 as _users_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Vote(_message.Message):
    __slots__ = ("poll_id", "option_id", "user_id")
    POLL_ID_FIELD_NUMBER: _ClassVar[int]
    OPTION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    poll_id: int
    option_id: int
    user_id: int
    def __init__(self, poll_id: _Optional[int] = ..., option_id: _Optional[int] = ..., user_id: _Optional[int] = ...) -> None: ...

class PollOptions(_message.Message):
    __slots__ = ("id", "quantity", "text")
    ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    id: int
    quantity: int
    text: str
    def __init__(self, id: _Optional[int] = ..., quantity: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

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
    class PollsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: Poll
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[Poll, _Mapping]] = ...) -> None: ...
    POLLS_FIELD_NUMBER: _ClassVar[int]
    polls: _containers.MessageMap[int, Poll]
    def __init__(self, polls: _Optional[_Mapping[int, Poll]] = ...) -> None: ...

class PollRequest(_message.Message):
    __slots__ = ("user", "poll")
    USER_FIELD_NUMBER: _ClassVar[int]
    POLL_FIELD_NUMBER: _ClassVar[int]
    user: _users_pb2.User
    poll: Poll
    def __init__(self, user: _Optional[_Union[_users_pb2.User, _Mapping]] = ..., poll: _Optional[_Union[Poll, _Mapping]] = ...) -> None: ...
