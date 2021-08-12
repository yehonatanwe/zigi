#!/usr/bin/env python3

import argparse
from argparse import Namespace
from typing import List


def product_list(array: List[int]) -> List[int]:
    length: int = len(array)
    if length == 1:
        return [0]

    left: List[int] = [1]
    product: List[int] = []

    right: List[int] = [0] * length
    right[length - 1] = 1

    # each cell i holds the product of array[:i - 1], except for i == 0
    for i in range(length - 1):
        left.append(array[i] * left[i])
        print(f'left: {left}')

    # each cell i holds the product of array[i + 1:], except for i == length - 1
    for i in range(length - 1, 0, -1):
        right[i - 1] = array[i] * right[i]
        print(f'right: {right}')

    # each cell i holds the product of array[:i - 1] * array[i + 1:] == reduce(lambda x, y: x * y, array) / array[i]
    for i in range(length):
        product.append(left[i] * right[i])
        print(f'product: {product}')

    return product


def parse_arguments() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--array', type=list, dest='array')
    return parser.parse_args()


def main(args: Namespace) -> None:
    print(product_list(array=args.array))


if __name__ == '__main__':
    main(parse_arguments())
