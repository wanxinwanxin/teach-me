from manim import *
from teachme_manim import BeatClock

YELLOW = "#F4D345"
BLUE = "#58C4DD"
RED = "#FC6255"
GREY_B = "#CCCCCC"

BEATS = [10.05, 11.72, 14.51, 16.75, 8.7, 12.69, 9.58, 10.12]


class TeachScene(Scene):
    def construct(self):
        self.camera.background_color = "#0e1015"
        clock = BeatClock(self, BEATS)

        # ---------- Beat 0: the calibration test ----------
        title = Text("Grading the model", font_size=44, color=WHITE).move_to([0, 3.1, 0])
        clock.play(Write(title), run_time=1.0)

        z_formula = MathTex(
            r"z", r"=", r"\frac{", r"\text{realized return}", r"}{", r"\text{forecast volatility}", r"}"
        ).scale(1.2).move_to([0, 1.0, 0])
        z_formula[0].set_color(WHITE)
        z_formula[1].set_color(WHITE)
        z_formula[2].set_color(WHITE)
        z_formula[3].set_color(YELLOW)
        z_formula[4].set_color(WHITE)
        z_formula[5].set_color(BLUE)
        z_formula[6].set_color(WHITE)

        clock.play(Write(VGroup(z_formula[0], z_formula[1])), run_time=0.4)
        clock.play(Write(VGroup(z_formula[2], z_formula[3], z_formula[4])), run_time=0.7)
        clock.play(Write(VGroup(z_formula[5], z_formula[6])), run_time=0.5)

        bias_formula = MathTex(r"\text{bias statistic} = \text{std}(z)", color=WHITE).scale(1.1).move_to(
            [0, -0.6, 0]
        )
        clock.play(Write(bias_formula), run_time=1.2)

        caption1 = Text("1.0 means calibrated", font_size=30, color=WHITE).move_to([0, -1.8, 0])
        clock.play(FadeIn(caption1), run_time=0.8)
        clock.wait(1.5)
        clock.end_beat(0)

        # ---------- Beat 1: which side is safe ----------
        clock.play(FadeOut(VGroup(z_formula, bias_formula, caption1)), run_time=1.0)

        title_small = Text("Grading the model", font_size=30, color=WHITE).move_to([-4.8, 3.25, 0])
        clock.play(ReplacementTransform(title, title_small), run_time=1.0)
        title = title_small

        number_line = NumberLine(
            x_range=[0.70, 1.30, 0.10],
            length=10.0,
            include_numbers=True,
            font_size=26,
            color=WHITE,
            decimal_number_config={"num_decimal_places": 1},
        ).move_to([0, 0, 0])
        clock.play(Create(number_line), run_time=1.2)

        bias_label = Text("bias statistic", font_size=28, color=WHITE).move_to([0, -0.9, 0])
        clock.play(FadeIn(bias_label), run_time=0.6)

        dashed_vert = DashedLine([0, -0.4, 0], [0, 2.05, 0], color=WHITE, stroke_width=3)
        clock.play(Create(dashed_vert), run_time=0.8)

        arrow_right = Arrow([2.5, 1.0, 0], [3.9, 1.0, 0], color=RED, buff=0, stroke_width=4)
        under_label = Text("underforecast", font_size=28, color=RED).move_to([3.2, 1.4, 0])
        clock.play(FadeIn(arrow_right), FadeIn(under_label), run_time=1.0)

        arrow_left = Arrow([-2.5, 1.0, 0], [-3.9, 1.0, 0], color=RED, buff=0, stroke_width=4)
        over_label = Text("overforecast", font_size=28, color=RED).move_to([-3.2, 1.4, 0])
        clock.play(FadeIn(arrow_left), FadeIn(over_label), run_time=1.0)

        safe_caption = Text("below 1.0 is not the safe side", font_size=28, color=GREY_B).move_to([0, 2.4, 0])
        clock.play(FadeIn(safe_caption), run_time=0.8)
        clock.wait(2.0)
        clock.end_beat(1)

        # ---------- Beat 2: the adversarial panel ----------
        clock.play(FadeOut(VGroup(arrow_right, under_label, arrow_left, over_label, safe_caption)), run_time=0.8)

        new_dashed = DashedLine([0, -2.1, 0], [0, 2.2, 0], color=WHITE, stroke_width=3)
        clock.play(
            number_line.animate.shift(DOWN * 2.6),
            ReplacementTransform(dashed_vert, new_dashed),
            bias_label.animate.move_to([0, -3.2, 0]),
            run_time=1.2,
        )
        dashed_vert = new_dashed
        clock.wait(1.0)

        band = Rectangle(width=4.0, height=4.3, fill_color=GREY_B, fill_opacity=0.12, stroke_width=0).move_to(
            [0, 0.05, 0]
        )
        band_label = Text("acceptance band", font_size=26, color=GREY_B).move_to([0, 2.6, 0])
        clock.play(FadeIn(band), FadeIn(band_label), run_time=1.2)
        clock.wait(0.8)

        row_specs = [
            ("overall", 1.8),
            ("min-var", 1.1),
            ("market", 0.4),
            ("industry", -0.3),
            ("ETFs", -1.0),
            ("styles", -1.7),
        ]
        row_mobs = []
        for name, y in row_specs:
            t = Text(name, font_size=28, color=WHITE)
            t.move_to([-5.6, y, 0], aligned_edge=LEFT)
            row_mobs.append(t)
        clock.play(LaggedStart(*[FadeIn(t) for t in row_mobs], lag_ratio=0.25), run_time=3.0)
        clock.wait(1.5)
        clock.end_beat(2)

        # ---------- Beat 3: the shipped scoreboard ----------
        score_dots = []
        score_value_labels = []

        def reveal_row(row_index, value_x, value_text, label_offset=None):
            row_y = row_specs[row_index][1]
            dot = Dot(point=[value_x, row_y, 0], radius=0.10, color=WHITE)
            offset = label_offset if label_offset is not None else UP * 0.32
            label = Text(value_text, font_size=26, color=WHITE).move_to(dot.get_center() + offset)
            score_dots.append(dot)
            score_value_labels.append(label)
            clock.play(FadeIn(dot), FadeIn(label), run_time=0.7)
            return dot

        reveal_row(0, -0.20, "0.988")
        clock.wait(0.3)

        # min-var sits almost directly under the overall dot (x nearly equal) -
        # push its label right so it does not stack in the same column, and
        # keep the vertical offset small so it clears the dot above.
        minvar_dot = reveal_row(1, -0.17, "0.99", label_offset=UP * 0.28 + RIGHT * 0.65)

        flash_circle = Circle(radius=0.28, color=RED, stroke_width=3).move_to(minvar_dot.get_center())
        clock.play(Create(flash_circle), run_time=0.4)
        hardest_label = Text("the hardest exam", font_size=26, color=RED).move_to([1.6, 1.1, 0])
        clock.play(FadeOut(flash_circle), FadeIn(hardest_label), run_time=0.4)
        clock.wait(1.5)
        clock.play(FadeOut(hardest_label), run_time=0.5)

        reveal_row(2, -1.33, "0.92")
        clock.wait(0.3)
        # industry shares market's x exactly - offset its label right for the
        # same reason as min-var above.
        reveal_row(3, -1.33, "0.92", label_offset=UP * 0.28 + RIGHT * 0.65)
        clock.wait(0.3)
        reveal_row(4, -0.50, "0.97")
        clock.wait(0.3)

        exceedance_label = Text("5.2% beyond 2 sigma, target 5%", font_size=28, color=GREY_B).move_to([2.9, 2.6, 0])
        clock.play(FadeOut(band_label), FadeIn(exceedance_label), run_time=1.0)
        clock.wait(2.0)
        clock.end_beat(3)

        # ---------- Beat 4: the miss, published anyway ----------
        styles_dot = Dot(point=[2.07, -1.7, 0], radius=0.10, color=RED)
        styles_label = Text("1.124", font_size=26, color=RED).next_to(styles_dot, UP, buff=0.15)
        clock.play(FadeIn(styles_dot), FadeIn(styles_label), run_time=0.8)
        clock.wait(1.0)

        published_label = Text("published anyway", font_size=28, color=RED).move_to([4.4, -1.7, 0])
        clock.play(FadeIn(published_label), run_time=0.8)
        clock.wait(2.5)
        clock.end_beat(4)

        # ---------- Beat 5: the compression, recalled ----------
        scoreboard = VGroup(
            number_line,
            dashed_vert,
            bias_label,
            band,
            band_label,
            *row_mobs,
            *score_dots,
            *score_value_labels,
            exceedance_label,
            styles_dot,
            styles_label,
            published_label,
        )
        clock.play(FadeOut(scoreboard), run_time=1.2)

        num1 = Text("19,892,278", font_size=44, color=RED).move_to([-3.4, 1.2, 0])
        clock.play(FadeIn(num1), run_time=1.0)
        num2 = Text("713 days", font_size=40, color=YELLOW).move_to([-3.4, 0.0, 0])
        clock.play(FadeIn(num2), run_time=1.0)

        arrow_compress = Arrow([-1.2, 0.6, 0], [1.4, 0.6, 0], color=WHITE, stroke_width=5)
        clock.play(Create(arrow_compress), run_time=1.0)

        num3 = Text("7,127", font_size=56, color=WHITE).move_to([3.4, 0.6, 0])
        clock.play(FadeIn(num3), run_time=1.0)
        clock.wait(3.0)
        clock.end_beat(5)

        # ---------- Beat 6: what paid for the compression ----------
        clock.play(FadeOut(VGroup(num1, num2, arrow_compress, num3)), run_time=1.0)

        bar1 = Rectangle(width=1.0, height=0.6, fill_color=GREY_B, fill_opacity=1.0, stroke_width=0).move_to(
            [-3.0 + 1.0 / 2, 0.9, 0]
        )
        bar1_label = Text("smarter matrix: 0.07", font_size=28, color=GREY_B).move_to([1.3, 0.9, 0])
        clock.play(Create(bar1), FadeIn(bar1_label), run_time=1.0)

        bar2 = Rectangle(width=3.86, height=0.6, fill_color=YELLOW, fill_opacity=1.0, stroke_width=0).move_to(
            [-3.0 + 3.86 / 2, -0.5, 0]
        )
        bar2_label = Text("more observations: 0.27", font_size=28, color=YELLOW).next_to(bar2, RIGHT, buff=0.3)
        clock.play(Create(bar2), FadeIn(bar2_label), run_time=1.0)
        clock.wait(2.5)
        clock.end_beat(6)

        # ---------- Beat 7: what a risk model tells you ----------
        clock.play(FadeOut(VGroup(bar1, bar1_label, bar2, bar2_label, title_small)), run_time=1.2)

        line1 = Text("how far you can move", font_size=40, color=YELLOW).move_to([0, 1.0, 0])
        clock.play(Write(line1), run_time=1.2)
        line2 = Text("what to blame", font_size=40, color=BLUE).move_to([0, 0.0, 0])
        clock.play(Write(line2), run_time=1.2)
        line3 = Text("and where it is still wrong", font_size=40, color=WHITE).move_to([0, -1.0, 0])
        clock.play(Write(line3), run_time=1.2)
        clock.wait(3.0)

        clock.play(FadeOut(Group(*self.mobjects)), run_time=1.5)
        clock.end_beat(7)
