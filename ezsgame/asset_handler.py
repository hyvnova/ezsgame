# Paths to search first, meaning, when an asset path it's request it will go through each location here and check if the assset exists.
# Full asset path  = asset_location[i] + asset_path
from functools import cache
import os
from pathlib import Path
from typing import List, Set


HERE = Path(__file__).absolute().parent.parent

asset_locations: Set[Path] = {HERE, }


def assets_at(*paths: str) -> None:
    """
    Adds paths to asset locations, meaning when an asset path is requested,
    it will go through each location here and check if the asset exists.
    Full asset path = asset_location[i] / asset_path
    """
    for path in paths:
        full_path = HERE / path
        asset_locations.add(full_path)

@cache
def find_asset(asset_path: str) -> str:
    # Check if asset exists at provided path
    absolute_input_path = HERE / asset_path
    if absolute_input_path.exists():
        return str(absolute_input_path)
    
    # print(f"searching for {asset_path}")

    # Otherwise go through all possible asset locations
    for location in asset_locations:
        full_asset_path = (location / asset_path).resolve()
        # print(f"\t{full_asset_path}")

        if full_asset_path.exists():
            return full_asset_path

    raise ValueError(f'path "{asset_path}" couldn\'t be found')
