import os
import unittest
from unittest.mock import patch, MagicMock
import uuid

from ipfsclient.ipfs import Ipfs
from ipfskvs.index import Index
from ipfskvs.store import Store

class TestDelete(unittest.TestCase):
    ipfs: Ipfs

    def setUp(self) -> None:
        self.ipfs = Ipfs()

    @patch.object(Ipfs, "delete")
    @patch.object(Ipfs, "list_files")
    @patch("os.path.dirname")
    def test_delete(self, mock_dirname, mock_list_files, mock_delete):
        """Test the delete function."""
        
        # Mock the os.path.dirname function to return a test value
        mock_dirname.side_effect = ["/test_dir/test_sub_dir", "/test_dir", "/"]

        # Mock the Store instance
        store = Store(index=Index(index={
            "testindex1": str(uuid.uuid4()),
            "testindex2": str(uuid.uuid4())
        }), ipfs=self.ipfs)

        # Mock the list_files function to return an empty list
        mock_list_files.return_value = []

        # Call the delete function with check_directory set to True
        store.delete(check_directory=True)

        # Assert that delete and list_files were called with the correct arguments
        mock_delete.assert_any_call("/test_dir/test_sub_dir")
        mock_delete.assert_any_call("/test_dir")
        mock_list_files.assert_called_with("/test_dir")

    @patch.object(Ipfs, "delete")
    @patch.object(Ipfs, "list_files")
    @patch("os.path.dirname")
    def test__delete_if_empty(self, mock_dirname, mock_list_files, mock_delete):
        """Test the _delete_if_empty function."""

        # Mock the os.path.dirname function to return a test value
        mock_dirname.side_effect = ["/test_dir/test_sub_dir", "/test_dir", "/"]

        # Mock the Store instance
        store = Store(index=Index(index={
            "testindex1": str(uuid.uuid4()),
            "testindex2": str(uuid.uuid4())
        }), ipfs=self.ipfs)

        # Mock the list_files function to return an empty list
        mock_list_files.return_value = []

        # Call the _delete_if_empty function
        store._delete_if_empty("test_dir")

        # Assert that delete and list_files were called with the correct arguments
        mock_delete.assert_called_with("/test_dir")
        mock_list_files.assert_called_with("/test_dir")
