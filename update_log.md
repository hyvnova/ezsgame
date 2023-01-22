v3.0

# New 
- Changed overal proyect structure 
- Optimization: `Fonts`, Clock tiks, `Text`, `Vector2`
- Measure types: `Fraction`, `Pixel`, `Percent`

# Changes
- Removed `basics` and `extras` import files
- Temporality removed  `IObjects` 

# Fixed
- Audio Mixer init
- `Vector2.__repr__` method now gives correct representation
- other minor bugs

# Notes
This update was mainly focused in improving optimization even it some sacrifaces were needed. In this case all of hte interactive objects had to be deprecated by the moment. Later on i'll try to re-make them in a more efficent way.