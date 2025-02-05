from manim import *
from manim.utils.color.X11 import MAGENTA3

class MobiusTransformation(Scene):
    def place_point(self, plane, point, text, color, pos):
        dot = Dot().move_to(plane.n2p(point))
        dot.set_color(color)
        # make the label bold
        label = MathTex(text, font_size=20, color=color)
        label.next_to(dot, pos)
        # speed up the animation
        self.play(Create(dot), Create(label), run_time=0.2)
        return dot, label

    def transform_point(self, original_dot, original_label, new_label, target_plane, new_position, pos):
        # Create the new dot at the new position on the target plane
        new_dot = Dot().move_to(target_plane.n2p(new_position))
        new_dot.set_color(original_dot.get_color())

        # Create the new label
        new_label = MathTex(new_label, font_size=20, color=original_label.get_color())
        new_label.next_to(new_dot, pos)

        # Animate the transformation from the original to the new copy
        self.play(TransformFromCopy(original_dot, new_dot), TransformFromCopy(original_label, new_label))

        return new_dot, new_label

    def draw_line_between_points(self, point1, point2, color=WHITE):
        # Create the line between the two points
        # the line is long as the plane
        line = Line(point1.get_center(), point2.get_center(), color=color, stroke_width=3)
        line.set_length(7)

        # Animate if required
        self.play(Create(line))

        return line

    def create_circle_through_points(self, point1, point2, point3, color=WHITE):
        # use the function from_three_points to get the circle
        circle = Circle.from_three_points(point1.get_center(), point2.get_center(), point3.get_center())
        circle.set_color(color)
        circle.set_stroke(width=3)
        self.play(Create(circle))
        return circle

    def travel_along_path(self, path, color=WHITE):
        arrow = Arrow(start=path.start, end=path.end, color=color, buff=0, max_stroke_width_to_length_ratio=0, max_tip_length_to_length_ratio=0.4, tip_length=0.2)
        arrow.shift((path.end - path.start) * (-1))
        self.play(Create(path), arrow.animate.shift(path.end- path.start), run_time=1.5)
        self.play(FadeOut(arrow), run_time=0.09)
        self.wait(0.1)



    def construct(self):
        # function g defined on C infity to C infinity
        tex = MathTex(r'\text{Let } g: \mathbb{C}_{\infty} \to \mathbb{C}_{\infty} \text{ be a Möbius transformation defined by } g(z) = \frac{z + i}{z + 1} \text{ where } z \in \mathbb{C}_{\infty}.', font_size=24)
        tex2 = MathTex(r'\text{D = } \{ z \in \mathbb{C} : -1 < Re_z < 0, Im_z < 0 \}', font_size=24)
        tex2.next_to(tex, DOWN, buff=0.5)
        self.play(Write(tex))
        self.wait(0.5)
        self.play(Write(tex2))
        self.wait(0.5)
        # move it to the top left corner
        self.play(tex.animate.to_corner(UL), tex2.animate.to_corner(UL, buff=1))
        self.wait(0.5)

        # draw the complex plane
        complex_plane = ComplexPlane(
            x_range=[-3, 3],  # Define the x-range
            y_range=[-3, 3],  # Define the y-range
            background_line_style = {
                "stroke_width": 0.5
            },
            axis_config = {
                "stroke_width": 0.5
            }
        ).add_coordinates()
        # before playing fade out the text
        self.play(FadeOut(tex), FadeOut(tex2), Create(complex_plane))
        # self.play(Create(complex_plane))
        self.wait(0.5)

        # Define the width and height of the screen
        width = config.frame_width
        height = config.frame_height

        # Define the vertical strip region: -1 < Re(z) < 0
        real_region = Rectangle(
            width=1, height=height,  # Height covers full plane
            color=RED, fill_opacity=0.2, stroke_width=0
        ).move_to(complex_plane.get_center() + 0.5 * LEFT)  # Shift left

        # Define the lower half-plane: Im(z) < 0
        lower_half_plane = Rectangle(
            width=width, height=height / 2,
            color=BLUE, fill_opacity=0.2, stroke_width=0
        ).shift(DOWN * height / 4)  # Shift down

        # Create the intersection region
        intersection_region = Intersection(real_region, lower_half_plane, stroke_width=0)
        intersection_region.set_fill(PURPLE, opacity=0.2)  # Set intersection color
        intersection_region.set_stroke(width=0)

        # Animate each part
        self.play(Create(real_region))
        self.play(Create(lower_half_plane))
        self.wait(0.5)

        # Highlight the intersection
        self.play(Transform(real_region, intersection_region), Transform(lower_half_plane, intersection_region))
        self.wait(0.5)
        # create the normal text for the region inside the intersection
        label_D = Text("D", font_size=24, color=MAGENTA3)
        label_D.move_to(intersection_region.get_center())
        self.play(Create(label_D))
        self.wait(0.5)

        # create the path for the transformation

        # Animate shifting and scaling of the first complex plane
        # Create a group for the complex plane and its intersection region to apply transformations together
        group = VGroup(complex_plane, real_region, lower_half_plane, intersection_region, label_D)

        # Animate shifting and scaling of the entire group
        self.play(
            group.animate.shift(4 * LEFT + 0.7 * DOWN).scale(0.9)
        )
        self.wait(0.5)

        # Create the second complex plane and add coordinates
        second_plane = ComplexPlane(
            x_range=[-3, 3],
            y_range=[-3, 3],
            background_line_style = {
                "stroke_width": 0.5
            },
            axis_config = {
                "stroke_width": 0.5
            }
        ).add_coordinates()
        #
        second_plane.shift(4 * RIGHT)  # Shift to the right
        second_plane.shift(0.7 * DOWN)  # Shift down
        second_plane.scale(0.9)

        self.play(Create(second_plane))
        self.wait(0.5)

        # starting placing the points on the first complex plane
        # place A at 0 0
        A, label_A = self.place_point(complex_plane, 0, r'\mathbf{A}', GREEN, UR)

        # place B at -1 0
        B, label_B = self.place_point(complex_plane, -1, r'\mathbf{B}', BLUE, UL)

        # place C at -1 -1
        C, label_C = self.place_point(complex_plane, -1 - 1j, r'\mathbf{C}', RED, DL)

        # place D at 0 -1
        D, label_D = self.place_point(complex_plane, -1j, r'\mathbf{D}', YELLOW, RIGHT)

        # place E at the end of the graph -1 -1
        E, label_D = self.place_point(complex_plane, -1 - 3j, r'\mathbf{E}_{\infty}', GREEN, DOWN)

        # place E at the end of the graph 0 -3j
        self.place_point(complex_plane, - 3j, r'\mathbf{E}_{\infty}', GREEN, DOWN)

        # create the path
        # line between A and B
        line_AB = Line(A.get_center(), B.get_center(), color=GREEN, stroke_width=3)
        self.travel_along_path(line_AB, color=GREEN)

        # Create the line
        # line between B and the end of the graph
        infinity_B = complex_plane.n2p(-1 - 5j)
        line_B_I = Line(start=B.get_center(), end=infinity_B , color=RED, stroke_width=3)
        self.travel_along_path(line_B_I, MAGENTA3)

        infinity_A = complex_plane.n2p(0 - 5j)
        line_I_A = Line(start=infinity_A, end=A.get_center(), color=YELLOW, stroke_width=3)
        self.travel_along_path(line_I_A, BLUE)

        transformation = MathTex(
            r'using \ transformation \ g(z) = \frac{z + i}{z + 1}',
            font_size=24
        )

        # Position the text at the center of the screen
        transformation.move_to(ORIGIN)
        transformation.shift(UP * 3)

        # # Create the text on screen
        # self.play(Write(transformation))
        self.wait(5)
        #
        # # move each point to the second complex plane
        # # after transformation A will be  A' at 1 0
        # # Copy the point and move it to (1, 0) on the right plane
        A_prime, label_A_prime = self.transform_point(A, label_A, r'\mathbf{A}', second_plane, 0 + 1j, UR)
        self.wait(0.5)
        B_prime, label_B_prime = self.transform_point(B, label_B, r'\mathbf{B}', second_plane, -3 - 3j, UP)
        self.wait(0.5)
        C_prime, label_C_prime = self.transform_point(C, label_C, r'\mathbf{C}', second_plane, 1, UP)
        self.wait(0.5)
        D_prime, label_D_prime = self.transform_point(D, label_D, r'\mathbf{D}', second_plane, 0, UL)
        self.wait(0.5)
        E_prime, label_E_prime = self.transform_point(E, label_D, r'\mathbf{E}', second_plane, -1j, UL)
        self.wait(0.5)
        line_AC = self.draw_line_between_points(A_prime, C_prime, color=YELLOW)
        line_EC = self.draw_line_between_points(E_prime, C_prime, color=BLUE)
        self.wait(0.5)
        circle = self.create_circle_through_points(A_prime, C_prime, D_prime)

        self.wait(5)
