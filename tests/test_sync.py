"""Tests for SheetSync."""
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from sheetsync.sync import sync_to_google_sheet


def test_missing_files_raise_error(tmp_path):
    """Test that it fails safely if the CSV or credentials don't exist."""
    # Test missing CSV
    with pytest.raises(FileNotFoundError, match="CSV file not found"):
        sync_to_google_sheet("fake.csv", "fake_id", "fake_creds.json")

    # Test missing credentials
    fake_csv = tmp_path / "data.csv"
    fake_csv.touch()
    with pytest.raises(FileNotFoundError, match="Credentials file not found"):
        sync_to_google_sheet(fake_csv, "fake_id", "fake_creds.json")


@patch("sheetsync.sync.gspread.authorize")
@patch("sheetsync.sync.Credentials.from_service_account_file")
def test_sync_success(mock_creds, mock_authorize, tmp_path):
    """Test the happy path (using mocks so we don't actually hit Google)."""
    # Create a fake CSV
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("Name,Age\nAlice,30\nBob,25", encoding="utf-8")
    
    # Create fake credentials file
    creds_file = tmp_path / "creds.json"
    creds_file.touch()

    # Setup mocks
    mock_client = MagicMock()
    mock_sheet = MagicMock()
    mock_worksheet = MagicMock()
    
    mock_authorize.return_value = mock_client
    mock_client.open_by_key.return_value = mock_sheet
    mock_sheet.sheet1 = mock_worksheet

    # Run the function
    sync_to_google_sheet(csv_file, "fake_sheet_id", creds_file)

    # Verify the Google Sheet methods were called correctly
    mock_worksheet.clear.assert_called_once()
    mock_worksheet.update.assert_called_once()
    
    # Check that the data was formatted correctly
    args, kwargs = mock_worksheet.update.call_args
    assert kwargs["values"] == [["Name", "Age"], ["Alice", 30], ["Bob", 25]]