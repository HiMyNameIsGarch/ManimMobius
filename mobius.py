from manim import *
from manim.utils.color.SVGNAMES import DARKBLUE
from manim.utils.color.X11 import MAGENTA3

class MobiusTransformation(Scene):
    def g(self, z): # the main function (Mobius transformation)
        if abs(z) == float('inf'):
            return 1 + 0j
        try:
            return (z + 1j) / (z + 1)
        except ZeroDivisionError:
            return float('inf')

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
        line.set_length(6.5)

        # Animate if required
        self.play(Create(line))

        return line

    def create_circle_through_points(self, point1, point2, point3, color=WHITE):
        # use the function from_three_points to get the circle
        circle = Circle.from_three_points(point1.get_center(), point2.get_center(), point3.get_center(), color=color)
        circle.set_stroke(width=3)
        self.play(Create(circle))
        return circle

    def travel_along_path(self, path):
        arrow = Arrow(start=path.start, end=path.end, color=DARKBLUE, buff=0, max_stroke_width_to_length_ratio=0, max_tip_length_to_length_ratio=0.4, tip_length=0.2)
        arrow.shift((path.end - path.start) * (-1))
        self.bring_to_front(arrow)
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
        x_range = [-3, 3]
        y_range = [-3, 3]
        complex_plane = ComplexPlane(
            x_range=x_range,
            y_range=y_range,
            background_line_style = {
                "stroke_width": 0.4
            },
            axis_config = {
                "stroke_width": 0.4
            }
        ).add_coordinates()
        # before playing fade out the text
        self.play(FadeOut(tex), FadeOut(tex2), Create(complex_plane))
        # self.play(Create(complex_plane))
        self.wait(0.5)

                # Compute dimensions based on the complex plane's ranges
        x_min, x_max = x_range
        y_min, y_max = y_range

        # Width and height of the real_region (vertical strip: -1 < Re(z) < 0)
        real_region_width = 1  # From x = -1 to x = 0
        real_region_height = y_max - y_min  # Full height of the plane

        # Width and height of the lower_half_plane (Im(z) < 0)
        lower_half_plane_width = x_max - x_min  # Full width of the plane
        lower_half_plane_height = (0 - y_min)  # From y = -3 to y = 0

        # Define the vertical strip region: -1 < Re(z) < 0
        center_real_region = -abs(real_region_width)/2
        real_region = Rectangle(
            width=real_region_width,
            height=real_region_height,
            color=RED, fill_opacity=0.2, stroke_width=0
        ).move_to(complex_plane.c2p(center_real_region, 0))  # Center at x = -0.5, y = 0

        # Define the lower half-plane: Im(z) < 0
        center_img_region = -abs(lower_half_plane_height)/2
        lower_half_plane = Rectangle(
            width=lower_half_plane_width,
            height=lower_half_plane_height,
            color=BLUE, fill_opacity=0.2, stroke_width=0
        ).move_to(complex_plane.c2p(0, center_img_region))  # Center at x = 0, y = -1.5

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
        E, label_E = self.place_point(complex_plane, -1 - 3j, r'\mathbf{E}_{\infty}', ORANGE, DOWN)

        # place E at the end of the graph 0 -3j
        E2, label_E2 = self.place_point(complex_plane, - 3j, r'\mathbf{E}_{\infty}', ORANGE, DOWN)

        # create the path
        # line between A and B
        line_AB = Line(A.get_center(), B.get_center(), color=GREEN, stroke_width=3)
        self.bring_to_back(line_AB)
        self.travel_along_path(line_AB)
        self.bring_to_front(A, B)

        # Create the line
        # line between B and the end of the graph
        infinity_B = complex_plane.n2p(-1 - 5j)
        line_B_I = Line(start=B.get_center(), end=infinity_B , color=RED, stroke_width=3)
        self.bring_to_back(line_B_I)
        self.travel_along_path(line_B_I)
        self.bring_to_front(D, E)

        infinity_A = complex_plane.n2p(0 - 5j)
        line_I_A = Line(start=infinity_A, end=A.get_center(), color=YELLOW, stroke_width=3)
        self.bring_to_back(line_I_A)
        self.travel_along_path(line_I_A)
        self.bring_to_front(E2, A, B)

        transformation = MathTex(
            r'using \ transformation \ g(z) = \frac{z + i}{z + 1}',
            font_size=24
        )

        # Position the text at the center of the screen
        transformation.move_to(ORIGIN)
        transformation.shift(UP * 3.3)

        # Create the text on screen
        self.play(Write(transformation))
        self.wait(2.5)
        #
        # # move each point to the second complex plane
        # # after transformation A will be  A' at 1 0
        # # Copy the point and move it to (1, 0) on the right plane
        A_prime, label_A_prime = self.transform_point(A, label_A, r'\mathbf{A}\textquotesingle', second_plane, 0 + 1j, UR)
        self.wait(0.4)
        B_prime, label_B_prime = self.transform_point(B, label_B, r'\mathbf{B}\textquotesingle_{\infty}', second_plane, -2 - 3j, UP)
        self.wait(0.4)
        C_prime, label_C_prime = self.transform_point(C, label_C, r'\mathbf{C}\textquotesingle', second_plane, -1j, UP)
        self.wait(0.4)
        D_prime, label_D_prime = self.transform_point(D, label_D, r'\mathbf{D}\textquotesingle', second_plane, 0, UL)
        self.wait(0.4)
        E_prime, label_E_prime = self.transform_point(E, label_E, r'\mathbf{E}\textquotesingle', second_plane, 1, RIGHT)
        self.wait(0.4)
        line_AE = self.draw_line_between_points(A_prime, E_prime, color=GREEN)
        line_EC = self.draw_line_between_points(E_prime, C_prime, color=RED)
        self.wait(0.4)

        B_prime1, label_B_prime1 = self.transform_point(B, label_B, r'\mathbf{B}\textquotesingle_{\infty}', second_plane, -2 + 3j, UP)
        self.wait(0.3)
        circle = self.create_circle_through_points(A_prime, E_prime, D_prime, YELLOW)
        self.bring_to_front(A_prime, C_prime, D_prime, E_prime, B_prime, B_prime1)

        #
        point_i = second_plane.n2p(1j)  # i
        point_1 = second_plane.n2p(1)   # 1
        point_neg_i = second_plane.n2p(-1j)  # -i

        ## create the region for the second set g(D)
        boundary_points = [
            second_plane.n2p(-3 + 4j),  # Top-left corner
            second_plane.n2p(-3 - 4j),  # Bottom-left corner
            second_plane.n2p(0 - 1j),   # Top-right corner (near the circle)
            second_plane.n2p(1 + 0j),   # Bottom-right corner (near the circle)
        ]
        region = Polygon(*boundary_points, color=BLUE, fill_opacity=1)

        # Subtract the circle from the region
        region = Difference(region, circle)

        # Subtract the right side of the lines from the region
        # We'll use a custom approach to clip the region
        # Create a polygon to represent the right side of line1
        right_side_line1 = Polygon(
            point_i, point_1, second_plane.n2p(1 + 1j), second_plane.n2p(-1 + 1j), color=RED, fill_opacity=1
        )
        # Create a polygon to represent the right side of line2
        right_side_line2 = Polygon(
            point_neg_i, point_1, second_plane.n2p(1 - 1j), second_plane.n2p(-1 - 1j), color=RED, fill_opacity=1
        )

        # Subtract the right sides of the lines from the region
        region = Difference(region, Union(right_side_line1, right_side_line2))
        region.set_fill(PURPLE, opacity=0.4)  # Set intersection color
        region.set_stroke(width=0)

        self.play(Create(region), run_time=1.5)

        label_gD = Text("g(D)", font_size=20, color=MAGENTA3)
        label_gD.move_to(region.get_center() + 0.5 * UP)
        self.play(Create(label_gD))
        self.wait(0.5)

        # Define the path
        path = VMobject()
        path.append_points(Line(start=A_prime, end=B_prime1).points)

        half_circle = Arc(
            radius=np.sqrt(2) / 2,
            start_angle=135 * DEGREES,
            angle=180 * DEGREES,
            arc_center=second_plane.n2p(0.5 + 0.5j),
        ).reverse_points()

        path.append_points(Line(start=B_prime, end=E_prime).points)
        path.append_points(half_circle.points)
                # Create a very short arrow, so only the tip is visible
        arrow = ArrowTriangleFilledTip(color=DARKBLUE, fill_opacity=1).scale(0.7)
        # Place the arrow at the start of the path
        arrow.move_to(path.get_start())

        old_arrow = arrow.copy()
        old_path = VMobject()
        old_path.append_points(line_AB.points)
        old_path.append_points(line_B_I.points)
        old_path.append_points(line_I_A.points)

        old_arrow.move_to(old_path.get_start())
        # Animate the arrow along the path
        self.play(Create(old_arrow), Create(arrow), run_time=0.1)
        for _ in range(6):
            self.play(MoveAlongPath(old_arrow, old_path),MoveAlongPath(arrow, path), rate_func=linear, run_time=6)

        # Fade out the arrow at the end
        self.play(FadeOut(arrow, old_arrow), run_time=0.09)

        self.wait(5)

