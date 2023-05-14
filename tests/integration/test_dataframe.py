import unittest

from ipfsclient.ipfs import Ipfs

from ipfskvs.index import Index
from ipfskvs.store import Store

import pandas as pd

from protobuf.sample_pb2 import Example, Type


class TestDataframe(unittest.TestCase):
    """Unit test class for testing DataFrame related operations."""

    def setUp(self: unittest.TestCase) -> None:
        """Initialize necessary objects for the test cases."""
        self.ipfs = Ipfs()

    def test_to_dataframe(self: unittest.TestCase) -> None:
        """Test case for checking the to_dataframe method."""
        data = [
            Store(
                index=Index(
                    prefix="vouch",
                    index={
                        "voucher": "123",
                        "vouchee": "456"
                    }
                ),
                reader=Example(type=Type.BUZZ, content="fizz"),
                ipfs=self.ipfs
            ),
            Store(
                index=Index(
                    prefix="vouch",
                    index={
                        "voucher": "12356",
                        "vouchee": "45678"
                    }
                ),
                reader=Example(type=Type.FIZZ, content="buzz"),
                ipfs=self.ipfs
            ),
        ]

        # Mock protobuf parsers
        protobuf_parsers = {
            'type': lambda store: store.reader.type,
            'content': lambda store: store.reader.content
        }

        # Call the function
        result = Store.to_dataframe(data, protobuf_parsers)

        # Check the result
        expected_data = {
            'voucher': ['123', '12356'],
            'vouchee': ['456', '45678'],
            'type': [Type.BUZZ, Type.FIZZ],
            'content': ['fizz', 'buzz'],
        }
        expected_df = pd.DataFrame(expected_data)
        self.assertTrue(result.equals(expected_df))
