# A Mobius Transformation Animation using Manim

### Description
This is a simple animation of a Mobius Transformation using the Manim library. The Mobius Transformation is a complex function of the form f(z) = (az + b)/(cz + d) where a, b, c, and d are complex numbers. The animation shows how the Mobius Transformation maps the complex plane to itself.

### Requirements
- Python 3.7
- Manim library

### Usage
To run the animation, simply run the following command in the terminal <br>
```
manim -pqh mobius.py

the last argument can be changed as follows:
'pqh' High quality
'pqm' Medium quality
'pql' Low quality

```
~ If you don't want to run the animation yourself it can be found at the following link:
[Mobius Transformation Animation](https://www.youtube.com/watch?v=YyQQ7imWXn4)

### Output
The output of the animation is a video file named `mobius.mp4` which will be saved in the `media` folder.
If you want to modify the quality of the animation or the resolution of the video, you can change the parameters in the `mobius.py` file.

### Important Notes
- This is my first animation using Manim so the code might not be the most efficient.
- The animation is based on the code provided in the Manim documentation.

### Updates for the future
- For now the animation is kinda harcoded besides the computation for the secondary points. I will plan to make it more dynamic in the future.
I am thinking to get the transformation functions from the user and also the region of the complex plane. I guess this will make it far complex but also more interesting.
<br><br>Special Thanks to 3Blue1Brown and my Complex Analysis Professor for the inspiration.

### References
- [Manim Documentation](https://docs.manim.community/en/stable/index.html)
- [Mobius Transformation](https://en.wikipedia.org/wiki/M%C3%B6bius_transformation)
- [Official Manim Repository](https://github.com/3b1b/manim)
- [Manim Community Repository](https://github.com/ManimCommunity/manim)
