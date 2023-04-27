# Version dev-0.5.2

# New
- `Scene`'s now have a `on_switch` and `on_switch_out` methods
- `SceneManager` now has a `lazy_init` option

# Fixes
- `Group` > `__getitem__` method only searching for objects inside the group, now it searches for properties of the own group too 

# Changes
- `id`'s don't exist anymore, now `id(obj)` is used instead 