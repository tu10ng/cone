from manim import *
import numpy as np
import math


class Bend(Animation):
    def __init__(self, sector: Sector, r0, theta, axes, **kwargs) -> None:
        super().__init__(sector, **kwargs)
        self.r0 = r0
        self.theta = theta
        self.axes = axes

    def recalc_cone(self, r, h, t):
        coneSurface = Surface(
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

        return coneSurface

    def recalc_htr(self, alpha):
        """
        some magic calculating how to update the drawing parameters
        """
        h = self.r0 - (1 - math.sqrt(4 * PI * PI - self.theta * self.theta) / (2 * PI)) * self.r0 * alpha
        t = 2 * PI * alpha
        r = math.sqrt(self.r0 * self.r0 - h * h) / (1 - math.cos(t / 2))
        return h, t, r

    def interpolate_mobject(self, alpha: float) -> None:
        h, t, r = self.recalc_htr(alpha)
        cone = self.recalc_cone(h, t, r)
        self.mobject.set_value(cone)


class anim(ThreeDScene):
    def construct(self):
        # polygon = Polygon()
        # self.add(polygon)
        axes = ThreeDAxes(x_range=[-6, 6, 1], y_range=[-6, 6, 1], z_range=[-6, 6, 1])
        self.set_camera_orientation(phi=PI / 4, theta=PI / 4)
        self.add(axes)

        r0 = 2
        theta = PI / 2

        sector = Sector(r0).rotate(-PI / 4, about_point=ORIGIN)
        sector.set_fill(WHITE, opacity=0.3)
        self.add(sector)

        # alpha = 0.1
        # h, t, r = recalc_htr(alpha, r0, theta)
        # coneSurface = recalc_cone(axes, r, h, t)
        # self.add(coneSurface)
        # self.play(Transform(sector, coneSurface))
        tmp = []
        for alpha in [i / 10 for i in range(1, 11)]:
            h, t, r = recalc_htr(alpha, r0, theta)
            cone = recalc_cone(axes, r, h, t)
            tmp.append(cone)

        for i, j in zip(tmp, tmp[1:]):
            self.play(Transform(i, j))
