"""Test the Store.delete functions."""
import unittest
import uuid
from typing import Self
from unittest.mock import patch

from ipfsclient.ipfs import Ipfs

from ipfskvs.index import Index
from ipfskvs.store import Store


class TestDelete(unittest.TestCase):
    """Test class for Delete functionality."""

    def setUp(self: Self) -> None:
        """Set up the test."""
        self.ipfs = Ipfs()

    @patch("os.path.dirname")
    @patch.object(Ipfs, "list_files")
    @patch.object(Ipfs, "delete")
    def test_delete(
            self: Self,
            mock_delete: unittest.mock,
            mock_list_files: unittest.mock,
            mock_dirname: unittest.mock) -> None:
        """Test the delete function."""
        mock_dirname.side_effect = ["/test_dir/test_sub_dir", "/test_dir", "/"]
        store = Store(index=Index(index={
            "testindex1": str(uuid.uuid4()),
            "testindex2": str(uuid.uuid4())
        }), ipfs=self.ipfs)
        mock_list_files.return_value = []
        store.delete(check_directory=True)
        mock_delete.assert_any_call("/test_dir/test_sub_dir")
        mock_delete.assert_any_call("/test_dir")
        mock_list_files.assert_called_with("/test_dir")

    @patch("os.path.dirname")
    @patch.object(Ipfs, "list_files")
    @patch.object(Ipfs, "delete")
    def test__delete_if_empty(
            self: Self,
            mock_delete: unittest.mock,
            mock_list_files: unittest.mock,
            mock_dirname: unittest.mock) -> None:
        """Test the _delete_if_empty function."""
        mock_dirname.side_effect = ["/test_dir/test_sub_dir", "/test_dir", "/"]
        store = Store(index=Index(index={
            "testindex1": str(uuid.uuid4()),
            "testindex2": str(uuid.uuid4())
        }), ipfs=self.ipfs)
        mock_list_files.return_value = []
        store._delete_if_empty("test_dir")
        mock_delete.assert_called_with("/test_dir")
        mock_list_files.assert_called_with("/test_dir")
