#!/usr/bin/env python3
"""
This module contains the `index_range` function and the `Server` class
for paginating a database of popular baby names.
"""

import csv
import math
from typing import List, Tuple, Dict, Any


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Returns the start and end indices for the given page and page size.

    Args:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing the start and end indices for the
        given page and page size.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Returns the appropriate page of the dataset.

        Args:
            page (int, optional): The page number (1-indexed). Defaults to 1.
            page_size : The number of items per page. Defaults to 10.

        Returns:
            List[List]: The appropriate page of the dataset.
        """
        assert isinstance(page, int) and page > 0, "bad page"
        assert isinstance(page_size, int) and page_size > 0, "bad page_size"

        dataset = self.dataset()
        start_index, end_index = index_range(page, page_size)

        if start_index >= len(dataset):
            return []
        else:
            return dataset[start_index:end_index]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Returns a dictionary containing the hyperdata about the page.

        Args:
            page (int, optional): The page number (1-indexed). Defaults to 1.
            page_size : The number of items per page. Defaults to 10.

        Returns:
            Dict[str, Any]: A dictionary containing the hyperdata.
        """
        data = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.dataset()) / page_size)

        return {
            "page_size": len(data),
            "page": page,
            "data": data,
            "next_page": page + 1 if page < total_pages else None,
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": total_pages
        }
