from ._fluvio_python import Fluvio as _Fluvio
from .consumer import PartitionConsumer
from .producer import TopicProducer


class Fluvio:
    """An interface for interacting with Fluvio streaming."""

    _inner: _Fluvio

    def __init__(self, inner: _Fluvio):
        self._inner = inner

    @classmethod
    def connect(cls):
        """Creates a new Fluvio client using the current profile from
        `~/.fluvio/config`

        If there is no current profile or the `~/.fluvio/config` file does not
        exist, then this will create a new profile with default settings and
        set it as current, then try to connect to the cluster using those
        settings.
        """
        return cls(_Fluvio.connect())

    def partition_consumer(self, topic: str, partition: int) -> PartitionConsumer:
        """Creates a new `PartitionConsumer` for the given topic and partition

        Currently, consumers are scoped to both a specific Fluvio topic and to
        a particular partition within that topic. That means that if you have a
        topic with multiple partitions, then in order to receive all of the
        events in all of the partitions, you will need to create one consumer
        per partition.
        """
        return PartitionConsumer(self._inner.partition_consumer(topic, partition))

    def topic_producer(self, topic: str) -> TopicProducer:
        """
        Creates a new `TopicProducer` for the given topic name.

        Currently, producers are scoped to a specific Fluvio topic. That means
        when you send events via a producer, you must specify which partition
        each event should go to.
        """
        return TopicProducer(self._inner.topic_producer(topic))
