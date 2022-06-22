from _typeshed import Self
from collections.abc import AsyncIterator, Awaitable, Callable, Iterable, Mapping, MutableMapping
from typing import Any, Generic, NoReturn, Protocol
from typing_extensions import TypeAlias, TypedDict

from redis.asyncio.connection import ConnectCallbackT, Connection, ConnectionPool
from redis.asyncio.lock import Lock
from redis.asyncio.retry import Retry
from redis.client import AbstractRedis, _StrType
from redis.commands import AsyncCoreCommands, AsyncSentinelCommands, RedisModuleCommands
from redis.typing import ChannelT, EncodableT, KeyT

PubSubHandler: TypeAlias = Callable[[dict[str, str]], Awaitable[None]]

class ResponseCallbackProtocol(Protocol):
    def __call__(self, response: Any, **kwargs): ...

class AsyncResponseCallbackProtocol(Protocol):
    async def __call__(self, response: Any, **kwargs): ...

ResponseCallbackT: TypeAlias = ResponseCallbackProtocol | AsyncResponseCallbackProtocol

class Redis(AbstractRedis, RedisModuleCommands, AsyncCoreCommands[_StrType], AsyncSentinelCommands, Generic[_StrType]):
    response_callbacks: MutableMapping[str | bytes, ResponseCallbackT]
    @classmethod
    def from_url(cls, url: str, **kwargs) -> Redis[Any]: ...
    auto_close_connection_pool: Any
    connection_pool: Any
    single_connection_client: Any
    connection: Any
    def __init__(
        self,
        *,
        host: str = ...,
        port: int = ...,
        db: str | int = ...,
        password: str | None = ...,
        socket_timeout: float | None = ...,
        socket_connect_timeout: float | None = ...,
        socket_keepalive: bool | None = ...,
        socket_keepalive_options: Mapping[int, int | bytes] | None = ...,
        connection_pool: ConnectionPool | None = ...,
        unix_socket_path: str | None = ...,
        encoding: str = ...,
        encoding_errors: str = ...,
        decode_responses: bool = ...,
        retry_on_timeout: bool = ...,
        ssl: bool = ...,
        ssl_keyfile: str | None = ...,
        ssl_certfile: str | None = ...,
        ssl_cert_reqs: str = ...,
        ssl_ca_certs: str | None = ...,
        ssl_ca_data: str | None = ...,
        ssl_check_hostname: bool = ...,
        max_connections: int | None = ...,
        single_connection_client: bool = ...,
        health_check_interval: int = ...,
        client_name: str | None = ...,
        username: str | None = ...,
        retry: Retry | None = ...,
        auto_close_connection_pool: bool = ...,
        redis_connect_func: ConnectCallbackT | None = ...,
    ) -> None: ...
    def __await__(self): ...
    async def initialize(self: Self) -> Self: ...
    def set_response_callback(self, command: str, callback: ResponseCallbackT): ...
    def load_external_module(self, funcname, func) -> None: ...
    def pipeline(self, transaction: bool = ..., shard_hint: str | None = ...) -> Pipeline[_StrType]: ...
    async def transaction(
        self,
        func: Callable[[Pipeline[_StrType]], Any | Awaitable[Any]],
        *watches: KeyT,
        shard_hint: str | None = ...,
        value_from_callable: bool = ...,
        watch_delay: float | None = ...,
    ): ...
    def lock(
        self,
        name: KeyT,
        timeout: float | None = ...,
        sleep: float = ...,
        blocking_timeout: float | None = ...,
        lock_class: type[Lock] | None = ...,
        thread_local: bool = ...,
    ) -> Lock: ...
    def pubsub(self, **kwargs) -> PubSub: ...
    def monitor(self) -> Monitor: ...
    def client(self) -> Redis[_StrType]: ...
    async def __aenter__(self: Self) -> Self: ...
    async def __aexit__(self, exc_type, exc_value, traceback) -> None: ...
    def __del__(self, _warnings: Any = ...) -> None: ...
    async def close(self, close_connection_pool: bool | None = ...) -> None: ...
    async def execute_command(self, *args, **options): ...
    async def parse_response(self, connection: Connection, command_name: str | bytes, **options): ...

StrictRedis = Redis

class MonitorCommandInfo(TypedDict):
    time: float
    db: int
    client_address: str
    client_port: str
    client_type: str
    command: str

class Monitor:
    monitor_re: Any
    command_re: Any
    connection_pool: Any
    connection: Any
    def __init__(self, connection_pool: ConnectionPool) -> None: ...
    async def connect(self) -> None: ...
    async def __aenter__(self): ...
    async def __aexit__(self, *args) -> None: ...
    async def next_command(self) -> MonitorCommandInfo: ...
    async def listen(self) -> AsyncIterator[MonitorCommandInfo]: ...

class PubSub:
    PUBLISH_MESSAGE_TYPES: Any
    UNSUBSCRIBE_MESSAGE_TYPES: Any
    HEALTH_CHECK_MESSAGE: str
    connection_pool: Any
    shard_hint: Any
    ignore_subscribe_messages: Any
    connection: Any
    encoder: Any
    health_check_response: Any
    channels: Any
    pending_unsubscribe_channels: Any
    patterns: Any
    pending_unsubscribe_patterns: Any
    def __init__(
        self,
        connection_pool: ConnectionPool,
        shard_hint: str | None = ...,
        ignore_subscribe_messages: bool = ...,
        encoder: Any | None = ...,
    ) -> None: ...
    async def __aenter__(self): ...
    async def __aexit__(self, exc_type, exc_value, traceback) -> None: ...
    def __del__(self) -> None: ...
    async def reset(self) -> None: ...
    def close(self) -> Awaitable[NoReturn]: ...
    async def on_connect(self, connection: Connection): ...
    @property
    def subscribed(self): ...
    async def execute_command(self, *args: EncodableT): ...
    async def parse_response(self, block: bool = ..., timeout: float = ...): ...
    async def check_health(self) -> None: ...
    async def psubscribe(self, *args: ChannelT, **kwargs: PubSubHandler): ...
    def punsubscribe(self, *args: ChannelT) -> Awaitable[Any]: ...
    async def subscribe(self, *args: ChannelT, **kwargs: Callable[..., Any]): ...
    def unsubscribe(self, *args) -> Awaitable[Any]: ...
    async def listen(self) -> AsyncIterator[Any]: ...
    async def get_message(self, ignore_subscribe_messages: bool = ..., timeout: float = ...): ...
    def ping(self, message: Any | None = ...) -> Awaitable[Any]: ...
    async def handle_message(self, response, ignore_subscribe_messages: bool = ...): ...
    async def run(self, *, exception_handler: PSWorkerThreadExcHandlerT | None = ..., poll_timeout: float = ...) -> None: ...

class PubsubWorkerExceptionHandler(Protocol):
    def __call__(self, e: BaseException, pubsub: PubSub): ...

class AsyncPubsubWorkerExceptionHandler(Protocol):
    async def __call__(self, e: BaseException, pubsub: PubSub): ...

PSWorkerThreadExcHandlerT: TypeAlias = PubsubWorkerExceptionHandler | AsyncPubsubWorkerExceptionHandler
CommandT: TypeAlias = tuple[tuple[str | bytes, ...], Mapping[str, Any]]
CommandStackT: TypeAlias = list[CommandT]

class Pipeline(Redis[_StrType], Generic[_StrType]):
    UNWATCH_COMMANDS: Any
    connection_pool: Any
    connection: Any
    response_callbacks: Any
    is_transaction: Any
    shard_hint: Any
    watching: bool
    command_stack: Any
    scripts: Any
    explicit_transaction: bool
    def __init__(
        self,
        connection_pool: ConnectionPool,
        response_callbacks: MutableMapping[str | bytes, ResponseCallbackT],
        transaction: bool,
        shard_hint: str | None,
    ) -> None: ...
    async def __aenter__(self: Self) -> Self: ...
    async def __aexit__(self, exc_type, exc_value, traceback) -> None: ...
    def __await__(self): ...
    def __len__(self): ...
    def __bool__(self): ...
    async def reset(self) -> None: ...  # type: ignore[override]
    def multi(self) -> None: ...
    def execute_command(self, *args, **kwargs) -> Pipeline[_StrType] | Awaitable[Pipeline[_StrType]]: ...
    async def immediate_execute_command(self, *args, **options): ...
    def pipeline_execute_command(self, *args, **options): ...
    def raise_first_error(self, commands: CommandStackT, response: Iterable[Any]): ...
    def annotate_exception(self, exception: Exception, number: int, command: Iterable[object]) -> None: ...
    async def parse_response(self, connection: Connection, command_name: str | bytes, **options): ...
    async def load_scripts(self) -> None: ...
    async def execute(self, raise_on_error: bool = ...): ...
    async def discard(self) -> None: ...
    async def watch(self, *names: KeyT): ...
    async def unwatch(self): ...
