from manim import *
import numpy as np
import math


class Bend:
    def __init__(
        self, sector: Sector, r0: float, theta: float, axes: ThreeDAxes
    ) -> None:
        self.sector = sector
        self.r0 = r0
        self.theta = theta
        self.axes = axes

    def recalc_htr(self, alpha):
        """
        some magic calculating how to update the drawing parameters
        """
        if alpha < 0.1:
            alpha = 0.1
        h = (
            self.r0
            - (1 - math.sqrt(4 * PI * PI - self.theta * self.theta) / (2 * PI))
            * self.r0
            * alpha
        )
        t = 2 * PI * alpha
        r = math.sqrt(self.r0 * self.r0 - h * h) / (1 - math.cos(t / 2))
        return h, t, r

    def draw_cone(self, alpha):
        """
        `always_redraw' needs a function, but i dont know how to embed 2 expr in python's lambda, so we have this function
        """
        alpha = alpha.get_value()
        h, t, r = self.recalc_htr(alpha)
        cone = Surface(
            lambda u, v: self.axes.c2p(
                v,
                r * v * np.cos(u) / h,
                r * v * np.sin(u) / h,
            ),
            u_range=[0, t],
            v_range=[0, h],
        )
        return cone

    def animation(self, scene) -> None:
        alpha = ValueTracker(0)
        cone = always_redraw(lambda: self.draw_cone(alpha))
        # scene.play(Transform(self.sector, cone))
        # scene.wait()
        scene.add(cone)
        scene.play(ReplacementTransform(self.sector, cone))
        scene.play(alpha.animate(run_time=4, rate_func=smooth).set_value(1))
        
        h, t, r = self.recalc_htr(1)
        final_cone = Cone(base_radius=self.axes.c2p(0, r)[1],
                          height=self.axes.c2p(h, 0)[0],
                          direction=LEFT,
                          checkerboard_colors=False,
                          show_base=True)
        scene.play(ReplacementTransform(cone, final_cone))
        scene.wait()


class anim(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(x_range=[-6, 6, 1], y_range=[-6, 6, 1], z_range=[-6, 6, 1])
        self.set_camera_orientation(phi=PI / 4, theta=PI / 4)
        self.add(axes)
        self.begin_ambient_camera_rotation()
        self.wait()

        r0 = 5
        theta = PI / 2

        sector = Sector(r0)
        sector.rotate(PI / 2, axis=np.array([PI / 4, PI / 4, 0.0]))
        # .rotate(-PI / 4, about_point=ORIGIN)
        sector.set_fill(WHITE, opacity=0.3)
        self.add(sector)
        self.wait(3)

        bend = Bend(sector, r0, theta, axes)
        bend.animation(self)
        self.wait(3)
