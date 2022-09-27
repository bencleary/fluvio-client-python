import typing

from ._fluvio_python import (  # noqa: F401
    Error as FluviorError,
    ProducerBatchRecord as _ProducerBatchRecord,
    TopicProducer as _TopicProducer,
)


class TopicProducer:
    """An interface for producing events to a particular topic.

    A `TopicProducer` allows you to send events to the specific topic it was
    initialized for. Once you have a `TopicProducer`, you can send events to
    the topic, choosing which partition each event should be delivered to.
    """

    _inner: _TopicProducer

    def __init__(self, inner: _TopicProducer):
        self._inner = inner

    def send_string(self, buf: str) -> None:
        """Sends a string to this producer’s topic"""
        return self.send([], buf.encode("utf-8"))

    def send(self, key: typing.List[int], value: typing.List[int]) -> None:
        """
        Sends a key/value record to this producer's Topic.

        The partition that the record will be sent to is derived from the Key.
        """
        return self._inner.send(key, value)

    def flush(self) -> None:
        """
        Send all the queued records in the producer batches.
        """
        return self._inner.flush()

    def send_all(self, records: typing.List[typing.Tuple[bytes, bytes]]):
        """
        Sends a list of key/value records as a batch to this producer's Topic.
        :param records: The list of records to send
        """
        records_inner = [_ProducerBatchRecord(x, y) for (x, y) in records]
        return self._inner.send_all(records_inner)
