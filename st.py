from manim import *
import numpy as np


class Square2Circle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)

        square = Square()
        square.rotate(PI / 4)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))


class SquareAndCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)

        square = Square()
        square.set_fill(BLUE, opacity=0.5)

        square.next_to(circle, RIGHT, buff=0.5)
        self.play(Create(circle), Create(square))


class AnimatedSquare2Circle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()

        self.play(Create(square))
        self.play(square.animate.rotate(PI / 4))
        self.play(ReplacementTransform(square, circle))
        self.play(circle.animate.set_fill(PINK, opacity=0.5))
        self.wait(1)


class Count(Animation):
    def __init__(
        self, number: DecimalNumber, start: float, end: float, **kwargs
    ) -> None:
        super().__init__(number, **kwargs)
        self.start = start
        self.end = end

    def interpolate_mobject(self, alpha: float) -> None:
        value = self.start + (alpha * (self.end - self.start))
        self.mobject.set_value(value)


class Counting(Scene):
    def construct(self):
        number = DecimalNumber().set_color(WHITE).scale(5)
        number.add_updater(lambda number: number.move_to(ORIGIN))

        self.add(number)
        self.wait()

        self.play(Count(number, 114, 514), run_time=4, rate_func=linear)

        self.wait()


class ExampleRotation(Scene):
    def construct(self):
        m1a = Square().shift(LEFT)
        m1b = Circle().shift(LEFT)
        m2a = Square().shift(RIGHT)
        m2b = Circle().shift(RIGHT)

        points = m2a.points
        points = np.roll(points, int(len(points) / 4), axis=0)
        m2a.points = points

        self.play(Transform(m1a, m1b), Transform(m2a, m2b))
