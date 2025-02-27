from manim import *
from manim.utils.color.AS2700 import B13_NAVY_BLUE
from manim.utils.color.BS381 import DEEP_SAXE_BLUE
from manim.utils.color.DVIPSNAMES import CYAN, TEALBLUE, VIOLET
from manim.utils.color.SVGNAMES import OLIVE, SLATEBLUE
from manim.utils.color.XKCD import PINKISHORANGE, PISTACHIO, RUSTBROWN, RUSTORANGE, SAFFRON

class MobiusThumbnail(Scene):
    def construct(self):
        # Create the original grid (left side)
        original_grid = ComplexPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": "#FF00FF",  # Indigo for grid lines
                "stroke_width": 1.7,
                "stroke_opacity": 0.5
            },
            axis_config = {
                "stroke_width": 0.4,
                "decimal_number_config": {
                    "num_decimal_places": 0,  # No decimal places for integers
                },
            }
        ).add_coordinates()
        original_grid.scale(0.8)  # Scale down to fit on the left
        original_grid.to_edge(LEFT)  # Move to the left side of the screen
        original_grid.to_edge(DOWN)

        # Create the transformed grid (right side)
        transformed_grid = ComplexPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": "#FF00FF",  # Slate blue for transformed grid lines
                "stroke_width": 1.7,
                "stroke_opacity": 0.5
            },
            axis_config = {
                "stroke_width": 0.4
            }
        )

        # Apply the Möbius transformation (z + i) / (z + 1)
        def mobius_transform(point):
            z = complex(point[0], point[1])
            w = (z + 1j) / (z + 1)  # Möbius transformation
            return np.array([w.real, w.imag, 0])

        transformed_grid = transformed_grid.apply_function(mobius_transform)
        transformed_grid.scale(6.5)  # Scale down to fit on the right
        transformed_grid.shift(RIGHT * 1.5)
        transformed_grid.shift(DOWN)

        # Add the title "Portals at Infinity" with gradient colors for each letter
        title = Text("Portals at Infinity", font_size=65)
        title.set_color_by_gradient("#00FFFF", "#FF00FF")  # Cyan to Magenta gradient
        title.to_edge(UP)

        # Add a subtitle with gradient colors for each letter
        subtitle = Text("Exploring Möbius Transformations in 2D", font_size=45)
        subtitle.set_color_by_gradient("#00FFFF", "#FF00FF")  # Cyan to Magenta gradient
        subtitle.next_to(title, DOWN)

        # Add all elements to the scene
        self.add(original_grid, transformed_grid, title, subtitle)
