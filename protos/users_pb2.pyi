from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("name", "email", "id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    email: str
    id: int
    def __init__(self, name: _Optional[str] = ..., email: _Optional[str] = ..., id: _Optional[int] = ...) -> None: ...

class Credentials(_message.Message):
    __slots__ = ("password", "acess_token")
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    ACESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    password: str
    acess_token: str
    def __init__(self, password: _Optional[str] = ..., acess_token: _Optional[str] = ...) -> None: ...

class UserAuth(_message.Message):
    __slots__ = ("user", "credentials")
    USER_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    user: User
    credentials: Credentials
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., credentials: _Optional[_Union[Credentials, _Mapping]] = ...) -> None: ...

class AuthReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: bool
    def __init__(self, result: bool = ...) -> None: ...

class InformationRequest(_message.Message):
    __slots__ = ("user_auth", "information")
    USER_AUTH_FIELD_NUMBER: _ClassVar[int]
    INFORMATION_FIELD_NUMBER: _ClassVar[int]
    user_auth: UserAuth
    information: str
    def __init__(self, user_auth: _Optional[_Union[UserAuth, _Mapping]] = ..., information: _Optional[str] = ...) -> None: ...

class InformationReply(_message.Message):
    __slots__ = ("information",)
    INFORMATION_FIELD_NUMBER: _ClassVar[int]
    information: str
    def __init__(self, information: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
