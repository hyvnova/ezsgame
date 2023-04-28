
from typing import Iterable
from path import Path
from ezsgame.styles.units import Measure
from ezsgame.types import Pos, Size


class Tile:
    def __init__(
            self,
            sprite: Path | str,
            pos: Pos | Iterable[Measure],
            size: Measure # Tiles are always square
    ):
        self.sprite = sprite
        self.pos = pos
        self.size = size
        self.rect = (self.pos, self.size)
    
    
    def __repr__(self):
        return f"Tile(sprite={self.sprite}, pos={self.pos}, size={self.size})"
    
    def __str__(self):
        return f"Tile(sprite={self.sprite}, pos={self.pos}, size={self.size})"
    

class TileMap:
    def __init__(
            self,
            tiles: list[Tile],
            pos: Pos | Iterable[Measure],
            size: Size | Iterable[Measure]
    ):
        self.tiles = tiles
        self.pos = pos
        self.size = size
        self.rect = (self.pos, self.size)
    
    
    def __repr__(self):
        return f"TileMap(tiles={self.tiles}, pos={self.pos}, size={self.size})"
    
    def __str__(self):
        return f"TileMap(tiles={self.tiles}, pos={self.pos}, size={self.size})"