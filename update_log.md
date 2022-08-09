# New 
- **InputBox** > **onchange** function, to check when InputBox value changes
- **Line** object
- **center_of** function
- **Grid** objects now can fully style boxes, and **place**, **get** and **remove** functions to manipulate objects inside the grid.


# Changes
- **Vector2** class now can manage operations of sum, substraction and multiplication of vectors
- removed **Primitive Objects**, **styles**, **require**, **scene** modules


# Fixed
- **Grid** > **highlight_current** function now works correctly


# Notes
Optimization improvements:
 - **EventHandler** class now the major event checking algorithm it's now
    about 30% faster.

- **Object** class styles resolving algorithm was improved.
- now **Object** and **Screen** > **fill** will only be called if it's necessary.

- Many of the removed modules probably will be replaced by new ones.
