"""SheetSync - Sync local data to Google Sheets."""

from .sync import sync_to_google_sheet

__version__ = "0.1.0"
__all__ = ["sync_to_google_sheet", "__version__"]