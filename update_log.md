# Version dev-0.6

## New
- Component creation system
- z-index style is back
- Shortcut to reduce boilerplate code `window.run` decorator
- `World` now has a `objects` attribute that contains all the objects in the world
- `utils` moved to new `utilities` module which also includes `timer` utility

## Fixes

## Changes
- `World` replaced `global_data`
- Time related functions now use seconds instead of milliseconds (Because it's easier to work with)
- `futures` module its now deprecated
- `Examples` are now deprecated