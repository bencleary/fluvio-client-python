import typing

from ._fluvio_python import Record as _Record


class Record:
    """The individual record for a given stream."""

    _inner: _Record

    def __init__(self, inner: _Record):
        self._inner = inner

    def offset(self) -> int:
        """The offset from the initial offset for a given stream."""
        return self._inner.offset()

    def value(self) -> typing.List[int]:
        """Returns the contents of this Record's value"""
        return self._inner.value()

    def value_string(self) -> str:
        """The UTF-8 decoded value for this record."""
        return self._inner.value_string()

    def key(self) -> typing.List[int]:
        """Returns the contents of this Record's key, if it exists"""
        return self._inner.key()

    def key_string(self) -> str:
        """The UTF-8 decoded key for this record."""
        return self._inner.key_string()
