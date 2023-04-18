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

    def recalc_cone(self, h, t, r):
        cone = Surface(
            lambda u, v: self.axes.c2p(
                v,
                r * v * np.cos(u) / h,
                r * v * np.sin(u) / h,
            ),
            u_range=[0, t],
            v_range=[0, h],
            checkerboard_colors=[YELLOW_B, YELLOW_B],
            stroke_color=YELLOW,
        )
        return cone

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

    def animation(self, scene) -> None:
        tmp = []
        rate = 10
        for alpha in [i / rate for i in range(1, rate + 1)]:
            h, t, r = self.recalc_htr(alpha)
            cone = self.recalc_cone(h, t, r)
            tmp.append(cone)

        scene.play(Transform(self.sector, tmp[0], rate_func=linear, run_time=1/rate))
        for i, j in zip(tmp, tmp[1:]):
            scene.play(Transform(i, j), rate_func=linear, run_time=1/rate)


class anim(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(x_range=[-6, 6, 1], y_range=[-6, 6, 1], z_range=[-6, 6, 1])
        self.set_camera_orientation(phi=PI / 4, theta=PI / 4)
        self.add(axes)

        r0 = 2
        theta = PI / 2

        sector = Sector(r0).rotate(-PI / 4, about_point=ORIGIN)
        sector.set_fill(WHITE, opacity=0.3)
        self.add(sector)
        self.wait()

        bend = Bend(sector, r0, theta, axes)
        bend.animation(self)
        self.wait()

        # alpha = 0.1
        # h, t, r = recalc_htr(alpha, r0, theta)
        # coneSurface = recalc_cone(axes, r, h, t)
        # self.add(coneSurface)
        # self.play(Transform(sector, coneSurface))
        # tmp = []
        # for alpha in [i / 10 for i in range(1, 11)]:
        #     h, t, r = recalc_htr(alpha, r0, theta)
        #     cone = recalc_cone(axes, r, h, t)
        #     tmp.append(cone)

        # for i, j in zip(tmp, tmp[1:]):
        #     self.play(Transform(i, j))
