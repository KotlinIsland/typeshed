import datetime
from _typeshed import Self
from collections.abc import Iterable, Iterator, Mapping
from typing import Any, TypeVar, overload
from typing_extensions import Literal, TypeAlias
from urllib.parse import ParseResult, SplitResult

from vobject.base import VBase

from .davclient import DAVClient
from .elements.cdav import CompFilter, ScheduleInboxURL, ScheduleOutboxURL
from .lib.url import URL

_CC = TypeVar("_CC", bound=CalendarObjectResource)

_vCalAddress: TypeAlias = Any  # actually icalendar.vCalAddress

class DAVObject:
    id: str | None
    url: URL | None
    client: DAVClient | None
    parent: DAVObject | None
    name: str | None
    props: Mapping[Any, Any]
    extra_init_options: dict[str, Any]
    def __init__(
        self,
        client: DAVClient | None = ...,
        url: str | ParseResult | SplitResult | URL | None = ...,
        parent: DAVObject | None = ...,
        name: str | None = ...,
        id: str | None = ...,
        props: Mapping[Any, Any] | None = ...,
        **extra: Any,
    ) -> None: ...
    @property
    def canonical_url(self) -> str: ...
    def children(self, type: str | None = ...) -> list[tuple[URL, Any, Any]]: ...
    def get_property(self, prop, use_cached: bool = ..., **passthrough) -> Any | None: ...
    def get_properties(
        self, props: Any | None = ..., depth: int = ..., parse_response_xml: bool = ..., parse_props: bool = ...
    ): ...
    def set_properties(self: Self, props: Any | None = ...) -> Self: ...
    def save(self: Self) -> Self: ...
    def delete(self) -> None: ...

class CalendarSet(DAVObject):
    def calendars(self) -> list[Calendar]: ...
    def make_calendar(
        self, name: str | None = ..., cal_id: str | None = ..., supported_calendar_component_set: Any | None = ...
    ) -> Calendar: ...
    def calendar(self, name: str | None = ..., cal_id: str | None = ...) -> Calendar: ...

class Principal(DAVObject):
    def __init__(self, client: DAVClient | None = ..., url: str | ParseResult | SplitResult | URL | None = ...) -> None: ...
    def calendars(self) -> list[Calendar]: ...
    def make_calendar(
        self, name: str | None = ..., cal_id: str | None = ..., supported_calendar_component_set: Any | None = ...
    ) -> Calendar: ...
    def calendar(self, name: str | None = ..., cal_id: str | None = ...) -> Calendar: ...
    def get_vcal_address(self) -> _vCalAddress: ...
    calendar_home_set: CalendarSet  # can also be set to anything URL.objectify() accepts
    def freebusy_request(self, dtstart, dtend, attendees): ...
    def calendar_user_address_set(self) -> list[str]: ...
    def schedule_inbox(self) -> ScheduleInbox: ...
    def schedule_outbox(self) -> ScheduleOutbox: ...

class Calendar(DAVObject):
    def get_supported_components(self) -> list[Any]: ...
    def save_with_invites(self, ical: str, attendees, **attendeeoptions) -> None: ...
    def save_event(self, ical: str | None = ..., no_overwrite: bool = ..., no_create: bool = ..., **ical_data: Any) -> Event: ...
    def save_todo(self, ical: str | None = ..., no_overwrite: bool = ..., no_create: bool = ..., **ical_data: Any) -> Todo: ...
    def save_journal(
        self, ical: str | None = ..., no_overwrite: bool = ..., no_create: bool = ..., **ical_data: Any
    ) -> Journal: ...
    add_event = save_event
    add_todo = save_todo
    add_journal = save_journal
    def calendar_multiget(self, event_urls: Iterable[URL]) -> list[Event]: ...
    def build_date_search_query(
        self,
        start,
        end: datetime.datetime | None = ...,
        compfilter: Literal["VEVENT"] | None = ...,
        expand: bool | Literal["maybe"] = ...,
    ): ...
    @overload
    def date_search(
        self,
        start: datetime.datetime,
        end: datetime.datetime | None = ...,
        compfilter: Literal["VEVENT"] = ...,
        expand: bool | Literal["maybe"] = ...,
        verify_expand: bool = ...,
    ) -> list[Event]: ...
    @overload
    def date_search(
        self, start: datetime.datetime, *, compfilter: None, expand: bool | Literal["maybe"] = ..., verify_expand: bool = ...
    ) -> list[CalendarObjectResource]: ...
    @overload
    def date_search(
        self,
        start: datetime.datetime,
        end: datetime.datetime | None,
        compfilter: None,
        expand: bool | Literal["maybe"] = ...,
        verify_expand: bool = ...,
    ) -> list[CalendarObjectResource]: ...
    @overload
    def search(self, xml, comp_class: None = ...) -> list[CalendarObjectResource]: ...
    @overload
    def search(self, xml, comp_class: type[_CC]) -> list[_CC]: ...
    def freebusy_request(self, start: datetime.datetime, end: datetime.datetime) -> FreeBusy: ...
    def todos(self, sort_keys: Iterable[str] = ..., include_completed: bool = ..., sort_key: str | None = ...) -> list[Todo]: ...
    def event_by_url(self, href, data: Any | None = ...) -> Event: ...
    def object_by_uid(self, uid: str, comp_filter: CompFilter | None = ...) -> Event: ...
    def todo_by_uid(self, uid: str) -> CalendarObjectResource: ...
    def event_by_uid(self, uid: str) -> CalendarObjectResource: ...
    def journal_by_uid(self, uid: str) -> CalendarObjectResource: ...
    event = event_by_uid
    def events(self) -> list[Event]: ...
    def objects_by_sync_token(
        self, sync_token: Any | None = ..., load_objects: bool = ...
    ) -> SynchronizableCalendarObjectCollection: ...
    objects = objects_by_sync_token
    def journals(self) -> list[Journal]: ...

class ScheduleMailbox(Calendar):
    def __init__(
        self,
        client: DAVClient | None = ...,
        principal: Principal | None = ...,
        url: str | ParseResult | SplitResult | URL | None = ...,
    ) -> None: ...
    def get_items(self): ...

class ScheduleInbox(ScheduleMailbox):
    findprop = ScheduleInboxURL

class ScheduleOutbox(ScheduleMailbox):
    findprop = ScheduleOutboxURL

class SynchronizableCalendarObjectCollection:
    def __init__(self, calendar, objects, sync_token) -> None: ...
    def __iter__(self) -> Iterator[Any]: ...
    def objects_by_url(self): ...
    def sync(self) -> tuple[Any, Any]: ...

class CalendarObjectResource(DAVObject):
    def __init__(
        self,
        client: DAVClient | None = ...,
        url: str | ParseResult | SplitResult | URL | None = ...,
        data: Any | None = ...,
        parent: Any | None = ...,
        id: Any | None = ...,
        props: Any | None = ...,
    ) -> None: ...
    def add_organizer(self) -> None: ...
    def add_attendee(self, attendee, no_default_parameters: bool = ..., **parameters) -> None: ...
    def is_invite_request(self) -> bool: ...
    def accept_invite(self, calendar: Any | None = ...) -> None: ...
    def decline_invite(self, calendar: Any | None = ...) -> None: ...
    def tentatively_accept_invite(self, calendar: Any | None = ...) -> None: ...
    def copy(self: Self, keep_uid: bool = ..., new_parent: Any | None = ...) -> Self: ...
    def load(self: Self) -> Self: ...
    def change_attendee_status(self, attendee: Any | None = ..., **kwargs) -> None: ...
    def save(
        self: Self, no_overwrite: bool = ..., no_create: bool = ..., obj_type: Any | None = ..., if_schedule_tag_match: bool = ...
    ) -> Self: ...
    data: Any
    vobject_instance: VBase
    icalendar_instance: Any
    instance: VBase

class Event(CalendarObjectResource): ...
class Journal(CalendarObjectResource): ...

class FreeBusy(CalendarObjectResource):
    def __init__(self, parent, data, url: str | ParseResult | SplitResult | URL | None = ..., id: Any | None = ...) -> None: ...

class Todo(CalendarObjectResource):
    def complete(self, completion_timestamp: datetime.datetime | None = ...) -> None: ...
