import typing

from ._fluvio_python import (  # noqa: F401
    Error as FluviorError,
    Offset as _Offset,
    PartitionConsumer as _PartitionConsumer,
    PartitionConsumerStream as _PartitionConsumerStream,
)
from .record import Record


class Offset:
    """Describes the location of an event stored in a Fluvio partition."""

    _inner: _Offset

    @classmethod
    def absolute(cls, index: int):
        """Creates an absolute offset with the given index"""
        return cls(_Offset.absolute(index))

    @classmethod
    def beginning(cls):
        """Creates a relative offset starting at the beginning of the saved log"""
        return cls(_Offset.beginning())

    @classmethod
    def end(cls):
        """Creates a relative offset pointing to the newest log entry"""
        return cls(_Offset.end())

    @classmethod
    def from_beginning(cls, offset: int):
        """Creates a relative offset a fixed distance after the oldest log
        entry
        """
        return cls(_Offset.from_beginning(offset))

    @classmethod
    def from_end(cls, offset: int):
        """Creates a relative offset a fixed distance before the newest log
        entry
        """
        return cls(_Offset.from_end(offset))

    def __init__(self, inner: _Offset):
        self._inner = inner


class PartitionConsumerStream:
    """An iterator for `PartitionConsumer.stream` method where each `__next__`
    returns a `Record`.

    Usage:

    ```python
    for i in consumer.stream(0):
        print(i.value())
        print(i.value_string())
    ```
    """

    _inner: _PartitionConsumerStream

    def __init__(self, inner: _PartitionConsumerStream):
        self._inner = inner

    def __iter__(self):
        return self

    def __next__(self) -> typing.Optional[Record]:
        return Record(self._inner.next())


class PartitionConsumer:
    """
    An interface for consuming events from a particular partition

    There are two ways to consume events: by "fetching" events and by
    "streaming" events. Fetching involves specifying a range of events that you
    want to consume via their Offset. A fetch is a sort of one-time batch
    operation: you’ll receive all of the events in your range all at once. When
    you consume events via Streaming, you specify a starting Offset and receive
    an object that will continuously yield new events as they arrive.
    """

    _inner: _PartitionConsumer

    def __init__(self, inner: _PartitionConsumer):
        self._inner = inner

    def stream(self, offset: Offset) -> PartitionConsumerStream:
        """
        Continuously streams events from a particular offset in the consumer’s
        partition. This returns a `PartitionConsumerStream` which is an
        iterator.

        Streaming is one of the two ways to consume events in Fluvio. It is a
        continuous request for new records arriving in a partition, beginning
        at a particular offset. You specify the starting point of the stream
        using an Offset and periodically receive events, either individually or
        in batches.
        """
        return PartitionConsumerStream(self._inner.stream(offset._inner))

    def stream_with_config(
        self, offset: Offset, wasm_path: str
    ) -> PartitionConsumerStream:
        """
        Continuously streams events from a particular offset with a SmartModule
        WASM module in the consumer’s partition. This returns a
        `PartitionConsumerStream` which is an iterator.

        Streaming is one of the two ways to consume events in Fluvio. It is a
        continuous request for new records arriving in a partition, beginning
        at a particular offset. You specify the starting point of the stream
        using an Offset and periodically receive events, either individually or
        in batches.

        Args:
            offset: Offset
            wasm_module_path: str - The absolute path to the WASM file

        Example:
            import os

            wmp = os.path.abspath("somefilter.wasm")
            for i in consumer.stream_with_config(Offset.beginning(), wmp):
                # do something with i

        Returns:
            PartionConsumerStream

        """
        return PartitionConsumerStream(
            self._inner.stream_with_config(offset._inner, wasm_path)
        )
