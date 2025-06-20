from pathlib import Path
import pickle
import os
import logging
from typing import List, Optional
from logger import get_logger


logger = get_logger("Product_Title_Saver")

class ProductTitleStorage:
    def __init__(self, save_folder: str = "./bucket", filename: str = "product_titles.pkl") -> None:
        Path(save_folder).mkdir(parents=True, exist_ok=True)
        self.file_path: str = os.path.join(save_folder, filename)
        self._strings: List[str] = self._load()

    def add_item(self, item: str) -> None:
        """Add single string to the list."""
        self._strings.append(item)

    def add_items(self, items: List[str]) -> None:
        """Add multiple items to the list."""
        self._strings.extend(items)

    def save(self) -> bool:
        """Save the list to a pickle file."""
        try:
            with open(self.file_path, 'wb') as f:
                pickle.dump(self._strings, f)
            logger.info("Successfully Saved Product Titles File")
            return True
        except (OSError, pickle.PickleError) as e:
            logger.error(f"Error saving: {e}")
            return False

    def _load(self) -> List[str]:
        """Load the list from a pickle file."""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'rb') as f:
                    return pickle.load(f)
        except (OSError, pickle.PickleError) as e:
            logger.error(f"Error loading: {e}")
        return []

    def get_all(self) -> List[str]:
        """Get all stored strings."""
        self._strings: List[str] = self._load()
        return self._strings.copy()

    def count(self) -> int:
        """Get count of stored strings."""
        return len(self._strings)

    def clear(self) -> None:
        """Clear all stored strings."""
        self._strings = []


if __name__ == "__main__":
    # Create product feed manager
    manager = ProductTitleStorage()
    print(manager.count())
    print(manager.get_all())
