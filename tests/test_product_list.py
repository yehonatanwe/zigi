from typing import List

import pytest

from src.product_list import product_list


@pytest.mark.parametrize(
    argnames=['array', 'product'], argvalues=[
        ([2, 3, 4, 5], [60, 40, 30, 24]),
        ([0, 1, 2, 3], [6, 0, 0, 0]),
        ([1, 2], [2, 1]),
        ([1], [0])
    ]
)
def test_product_array(array: List[int], product: List[int]) -> None:
    assert product == product_list(array=array)
