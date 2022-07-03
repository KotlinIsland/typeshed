import sys
from typing_extensions import TypeAlias

_version_info: TypeAlias = tuple[int, int, int, str, int]

class _Feature:
    def __init__(self, optionalRelease: _version_info, mandatoryRelease: _version_info | None, compiler_flag: int) -> None: ...
    def getOptionalRelease(self) -> _version_info: ...
    def getMandatoryRelease(self) -> _version_info | None: ...
    compiler_flag: int

absolute_import: _Feature
division: _Feature
generators: _Feature
nested_scopes: _Feature
print_function: _Feature
unicode_literals: _Feature
with_statement: _Feature
barry_as_FLUFL: _Feature
generator_stop: _Feature

if sys.version_info >= (3, 7):
    annotations: _Feature

all_feature_names: list[str]  # undocumented

__all__ = [
    "all_feature_names",
    "absolute_import",
    "division",
    "generators",
    "nested_scopes",
    "print_function",
    "unicode_literals",
    "with_statement",
    "barry_as_FLUFL",
    "generator_stop",
]

if sys.version_info >= (3, 7):
    __all__ += ["annotations"]
