from pathlib import Path
import pickle
import os
import logging
from typing import Set
from logger import get_logger


logger = get_logger("Product_Title_Saver")

class ProductTitleStorage:
    def __init__(self, save_folder: str = "./bucket", filename: str = "product_titles.pkl") -> None:
        Path(save_folder).mkdir(parents=True, exist_ok=True)
        self.file_path: str = os.path.join(save_folder, filename)
        self._titles: Set[str] = self._load()

    def add_item(self, item: str) -> None:
        """Add a single string to the set."""
        self._titles.add(item)

    def add_items(self, items: Set[str] | list[str]) -> None:
        """Add multiple items to the set."""
        self._titles.update(items)

    def save(self) -> bool:
        """Save the set to a pickle file."""
        try:
            with open(self.file_path, 'wb') as f:
                pickle.dump(self._titles, f)
            logger.info("Successfully saved Product Titles file.")
            return True
        except (OSError, pickle.PickleError) as e:
            logger.error(f"Error saving: {e}")
            return False

    def _load(self) -> Set[str]:
        """Load the set from a pickle file."""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'rb') as f:
                    data = pickle.load(f)
                    if isinstance(data, set):
                        return data
                    elif isinstance(data, list):
                        return set(data)
        except (OSError, pickle.PickleError) as e:
            logger.error(f"Error loading: {e}")
        return set()

    def get_all(self) -> Set[str]:
        """Get all stored strings."""
        self._titles: Set[str] = self._load()
        return self._titles.copy()

    def count(self) -> int:
        """Get count of stored strings."""
        return len(self._titles)

    def clear(self) -> None:
        """Clear all stored strings."""
        self._titles.clear()


if __name__ == "__main__":
    # Create product feed manager
    manager = ProductTitleStorage()
    print(manager.count())
    print(manager.get_all())
