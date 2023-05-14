"""Test the index.get_directory function."""

import unittest
from typing import Self

from ipfsclient.ipfs import Ipfs

from ipfskvs.index import Index
from ipfskvs.store import Store

from protobuf.sample_pb2 import Example, Type


class TestGetDirectory(unittest.TestCase):
    """Test class for get_directory functionality."""

    def setUp(self: Self) -> None:
        """Set up the test."""
        self.ipfs = Ipfs()
        self.data = Example(type=Type.BUZZ, content="fizz")
        self.index = Index(
            prefix='test',
            index={
                "testindex1": "id1",
                "testindex2": "id2"
            },
            subindex=Index(
                index={
                    "created": "created"
                }
            )
        )

    def test_get_directory(self: Self) -> None:
        """Test the get_directory function."""
        store = Store(
            index=self.index,
            ipfs=self.ipfs,
            reader=Example()
        )

        # Get the directory
        directory = store.index.get_directory()

        # Check the directory
        self.assertEqual(directory, 'test/testindex1_id1.testindex2_id2')
