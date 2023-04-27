# Version dev-0.5.1

# New
- `Window.run_scenes` method

# Fixes
- `Vector2`: 1 paramter creation error
- `AnimatedSprite` & `Sprite` -> `pos` and `size` resolve on init

# Changes
- `Sprite` now can't transpile into `AnimatedSprite` automatically (due to class instanciation errors)
- `Module`'s can't be `Scene`'s anymore (due to declaration errors with `Window`)