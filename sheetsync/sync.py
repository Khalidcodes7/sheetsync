"""Core logic to sync local data to Google Sheets."""
from __future__ import annotations

import logging
from pathlib import Path

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)

# The permissions required to read/write to Google Sheets and Drive
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def sync_to_google_sheet(
    csv_path: str | Path,
    sheet_id: str,
    credentials_path: str | Path,
) -> None:
    """
    Reads a CSV file and pushes its contents to a Google Sheet.
    
    Args:
        csv_path: Path to the local CSV file.
        sheet_id: The ID of the Google Sheet (found in the URL).
        credentials_path: Path to the service_account.json file.
    """
    csv_file = Path(csv_path)
    creds_file = Path(credentials_path)

    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    if not creds_file.exists():
        raise FileNotFoundError(f"Credentials file not found: {credentials_path}")

    logger.info("Authenticating with Google...")
    creds = Credentials.from_service_account_file(str(creds_file), scopes=SCOPES)
    client = gspread.authorize(creds)

    logger.info("Opening Google Sheet (ID: %s)...", sheet_id)
    sheet = client.open_by_key(sheet_id)
    
    # We will use the first tab/sheet in the document
    worksheet = sheet.sheet1

    logger.info("Reading local CSV: %s", csv_file.name)
    # Read CSV, fill empty cells with empty strings instead of NaN
    df = pd.read_csv(csv_file).fillna("")
    
    # Convert to list of lists for gspread
    data = [df.columns.values.tolist()] + df.values.tolist()

    logger.info("Clearing old data from Google Sheet...")
    worksheet.clear()

    logger.info("Uploading %d rows...", len(data))
    worksheet.update(values=data, range_name="A1")
    
    logger.info("Sync complete!")