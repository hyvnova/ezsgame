# Sprite System Analysis

This document provides an overview of how sprites are handled in **ezsgame** and highlights potential performance concerns.

## Static Sprites
- Implemented by the `Sprite` class which inherits from both `pygame.sprite.Sprite` and the library's base `Object`.
- Images are loaded with `pygame.image.load` and optionally scaled to the provided size.
- The `_update` method resizes the image every draw call, meaning dynamic size changes incur a transform each frame.

## Animated Sprites
- Implemented by `AnimatedSprite`, which loads GIF frames using `Pillow` and caches them in memory.
- A dictionary maps the original file path to the list of frames so subsequent instances reuse loaded data.
- Each instance tracks the current frame and uses `_update` to advance when enough time has passed.
- When multiple sprites share the same parameters, `__new__` returns an `AnimatedSpriteRef` object which simply stores a reference to the original sprite's `draw` method.

## Bottlenecks
1. **Object Overhead** – All sprites inherit from `Object`, which carries features like reactive properties and component groups. Large numbers of sprite instances may consume extra memory and CPU due to this shared base.
2. **Per-frame Scaling** – `_update` scales the surface on each call. Keeping pre-scaled surfaces or caching multiple scales could reduce repeated transforms.
3. **Event Dispatch** – The `EventHandler` performs multiple list traversals per frame. Converting internal structures to dictionaries keyed by event type or listener could reduce iteration cost.
4. **Main Loop** – Rendering and updating happen sequentially for every object. Profiling shows most time spent iterating `World.objects` and dispatching events.

## Suggestions
- Introduce a lightweight sprite class that bypasses `Object` when advanced features are unnecessary.
- Cache scaled surfaces keyed by size to avoid repeated `pygame.transform.scale` calls.
- Refactor `EventHandler` to map Pygame event codes directly to registered callbacks.
- Consider grouping draw calls or using sprite groups for batch rendering.
