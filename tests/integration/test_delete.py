"""Tests for the Store.delete method."""
import time
import unittest
import uuid

from ipfsclient.ipfs import Ipfs

from ipfskvs.index import Index
from ipfskvs.store import Store

from protobuf.sample_pb2 import Example, Type


class TestDelete(unittest.TestCase):
    """Test class for Delete functionality."""
    ipfs: Ipfs

    def setUp(self: unittest.TestCase) -> None:
        """Set up the test."""
        self.ipfs = Ipfs()
        self.data = Example(type=Type.BUZZ, content="fizz")
        self.created = str(time.time_ns())
        self.index = Index(
            prefix='test',
            index={
                "testindex1": str(uuid.uuid4()),
                "testindex2": str(uuid.uuid4())
            },
            subindex=Index(
                index={
                    "created": self.created
                }
            )
        )

    def _generate_writer_store(self: unittest.TestCase) -> Store:
        return Store(
            index=self.index,
            ipfs=self.ipfs,
            writer=self.data
        )

    def _generate_reader_store(self: unittest.TestCase) -> Store:
        return Store(
            index=self.index,
            ipfs=self.ipfs,
            reader=Example()
        )

    def test_delete(self: unittest.TestCase) -> None:
        """Test the delete function."""
        writer_store = self._generate_writer_store()
        reader_store_1 = self._generate_reader_store()
        reader_store_2 = self._generate_reader_store()

        # Write it to IPFS
        writer_store.add()

        # Check that it exists
        reader_store_1.read()
        self.assertEqual(reader_store_1.reader, self.data)

        # Delete it
        writer_store.delete()

        # Check that it no longer exists
        try:
            reader_store_2.read()
        except RuntimeError as e:
            self.assertEqual(str(e), '{"Message":"file does not exist","Code":0,"Type":"error"}\n')  # noqa: E501
        else:
            self.fail("RuntimeError not raised")

    def test_delete_directories(self: unittest.TestCase) -> None:
        """Test the delete function on directories."""
        writer_store = self._generate_writer_store()
        reader_store_1 = self._generate_reader_store()
        reader_store_2 = self._generate_reader_store()

        # Write it to IPFS
        writer_store.add()

        # Check that it exists
        reader_store_1.read()
        self.assertEqual(reader_store_1.reader, self.data)

        # Delete it
        writer_store.delete(check_directory=True)

        # Check that it no longer exists
        try:
            reader_store_2.read()
        except RuntimeError as e:
            self.assertEqual(str(e), '{"Message":"file does not exist","Code":0,"Type":"error"}\n')  # noqa: E501
        else:
            self.fail("RuntimeError not raised")

        # Check that the directory no longer exists
        directory = self.index.get_directory()
        result = self.ipfs.stat(directory)
        self.assertEqual(result, {'Message': 'file does not exist', 'Code': 0, 'Type': 'error'})  # noqa: E501
