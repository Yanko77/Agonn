######################################################################
# Copyright 2025 (c) Yanko Lemoine
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0
######################################################################

from __future__ import annotations
from typing import Any, Callable
import random


class QuickSet:
    """
    This class is a `set` of which it's possible to get a random element, remove an element
    and do `.__contains__()` with a complexity of O(1).
    """
    def __init__(self, data: list):
        self.data: list = data
        self.data_map: dict[Any, int] = {self.data[i]: i for i in range(len(self.data))}

    def remove(self, item):
        """
        Remove `item` from this set.

        Raises a ValueError if `item` is not in this

        Complexity : O(1)
        """
        # Get the last element and the index of the item to remove
        last = self.data[-1]
        index = self.data_map[item]

        # Swap the item to remove and the last
        self.data[index] = last
        self.data[-1] = item

        # Update data_map
        self.data_map[last] = index

        # Pop the last
        self.data.pop()
        # Pop item from data_map. ( O(1) )
        self.data_map.pop(item)
    
    def add(self, item):
        """
        Add `item` to this set.

        Complexity : O(1)
        """
        self.data_map[item] = len(self.data)
        self.data.append(item)
        

    def random_choice(self):
        """
        Returns a random element from this set.

        Complexity : O(1)
        """
        return random.choice(self.data)
    
    def filter(self, func: Callable[[Any], bool]) -> QuickSet:
        """
        Returns a copy of this set after filtering with using `func`.

        Filtering process:
        For all items in the result set : `func(item) == True`.
        """
        res_tuple = [el for el in self if func(el)]
        return QuickSet(res_tuple)


    def copy(self):
        return QuickSet(self.data)

    def __contains__(self, item):
        """
        Returns True if `item` is in this set. False otherwise.

        Complexity : O(1)
        """
        return item in self.data_map

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        for item in self.data:
            yield item