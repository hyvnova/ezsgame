# New 
- `Camera` module 
- `Draggable` component now can freeze `x or y` axis
- `Resizable` component now can freeze `width or height`.
- `Controllable` component, Moves the object with keyboard.

- `Behaviors` : *[experimental]*
    - **Pos** : `static`, `dynamic`

-  **ezsgame events** (Base events)  :
    - **Events** : `update`

- `Object`'s now have a `z_index` property.
- `Styles` class, which can be used to manage styles in a json file. *[experimental]*
    - When creating objects, parameter `styles` should be a `dict` with the styles

- `Interface` class. *[experimental]*
- `build` function, to convert projects to exe files. *[experimental]*
- `Custom events` functions, to create a more "specific" way of creating events. *[experimetal]*
- 
# Changes
- `Screen` > `fill` function now can take a  image as a parameter.
- Now buttons are rect-like objects.
- `IRect`, `ICircle` and any other `IObject` child, were replaced by `IObject.extend()` method .
- ***Extender*** classes have a `.extend()` method, extends a object properties.
- `Iscreen` class was replaced by `Interface` ****exteder**** class
- `funcs` module now is imported `basics`.
- moved `outline` function to `funcs` module.
- `Controller` class now can use or not delta time
- `delta_time` method is now a property

# Fixed
- `Controller` class now deletes it's events when destroyed.
- `ComponentGroup` class now deletes it's components when  destroyed
- `mousewheelup` and `mousewheeldown` events now work 

- `Reloader` class now doesn't interrupt the program when variables are defined/update.
 - `EventHandler` > `on_key` function now doens't interrup execusion when events are added/removed
- `EvenHandler` class now is **~35%** more faster due to the elimination of **base events**,  now all events are taken as "Events", but handle in different ways.
- `Objects` now initialize `components` atribute even if no componens are passed.