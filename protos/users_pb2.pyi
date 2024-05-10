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

class UsernamePassword(_message.Message):
    __slots__ = ("username", "password")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class AccessToken(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class Credentials(_message.Message):
    __slots__ = ("username_password", "access_token")
    USERNAME_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    username_password: UsernamePassword
    access_token: AccessToken
    def __init__(self, username_password: _Optional[_Union[UsernamePassword, _Mapping]] = ..., access_token: _Optional[_Union[AccessToken, _Mapping]] = ...) -> None: ...

class UserAuth(_message.Message):
    __slots__ = ("user", "credentials")
    USER_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    user: User
    credentials: Credentials
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., credentials: _Optional[_Union[Credentials, _Mapping]] = ...) -> None: ...

class AuthReply(_message.Message):
    __slots__ = ("access_token",)
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    def __init__(self, access_token: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
