from manim import *
######### References start ###############
#source: https://github.com/TheMathematicFanatic/MF_Tools
#owner: John Connell,2025
class TransformByGlyphMap(AnimationGroup):
    def __init__(
        self,
        mobA,
        mobB,
        *glyph_map,
        auto_resolve=False,
        from_copy=False,
        mobA_submobject_index=[0],
        mobB_submobject_index=[0],
        default_introducer=FadeIn,
        default_remover=FadeOut,
        introduce_individually=False,
        remove_individually=False,
        shift_fades=True,
        auto_resolve_delay=0.5,
        show_indices=False,
        A_index_labels_color=RED_D,
        B_index_labels_color=BLUE_D,
        index_label_height=0.18,
        printing=False,
        **kwargs
        ):

        A = mobA.copy() if from_copy else mobA
        for i in mobA_submobject_index:
            A = A[i]
        B = mobB
        for i in mobB_submobject_index:
            B = B[i]
        animations = []
        mentioned_from_indices = []
        mentioned_to_indices = []

        def VG(mob, index_list):
            return VGroup(*[mob[i] for i in index_list])
        
        if len(glyph_map)==0: show_indices=True

        for entry in glyph_map:
            if printing:
                print("Glyph map entry: ", entry)
            assert len(entry) in [2, 3], "Invalid glyph_map entry: " + str(entry)
            entry_kwargs = {} if len(entry) == 2 else entry[2]

            if not entry[0] and not entry[1]:
                print("Empty glyph_map entry: " + str(entry))
                show_indices = True
            elif (not entry[0]) or (isinstance(entry[0], type) and issubclass(entry[0], Animation)):
                Introducer = entry[0] if entry[0] else default_introducer
                introduced_mobs = [B[i] for i in entry[1]] if introduce_individually else [VG(B,entry[1])]
                for mob in introduced_mobs:
                    animations.append(Introducer(
                        mob,
                        **{
                            **kwargs,
                            **{"shift":B.get_center() - A.get_center() if shift_fades else ORIGIN},
                            **entry_kwargs
                        }
                        ))
                    if "delay" in entry_kwargs:
                        animations[-1] = Succession(Wait(entry_kwargs["delay"]), animations[-1])
                mentioned_to_indices += entry[1]
            elif not entry[1] or (isinstance(entry[1], type) and issubclass(entry[1], Animation)):
                Remover = entry[1] if entry[1] else default_remover
                removed_mobs = [A[i] for i in entry[0]] if remove_individually else [VG(A,entry[0])]
                for mob in removed_mobs:
                    animations.append(Remover(
                        mob,
                        **{
                            **kwargs,
                            **{"shift":B.get_center() - A.get_center() if shift_fades else ORIGIN},
                            **entry_kwargs
                        }
                        ))
                    if "delay" in entry_kwargs:
                        animations[-1] = Succession(Wait(entry_kwargs["delay"]), animations[-1])
                mentioned_from_indices += entry[0]
            elif len(entry[0]) > 0 and len(entry[1]) > 0:
                animations.append(ReplacementTransform(
                    VGroup(*[A[i].copy() if i in mentioned_from_indices else A[i] for i in entry[0]]),
                    VG(B,entry[1]),
                    **{
                        **kwargs,
                        **entry_kwargs
                        }
                    ))
                if "delay" in entry_kwargs:
                    animations[-1] = Succession(Wait(entry_kwargs["delay"]), animations[-1])
                mentioned_from_indices += entry[0]
                mentioned_to_indices += entry[1]
            else:
                raise ValueError("Invalid glyph_map entry: " + str(entry))
        
        
        remaining_from_indices = [i for i in range(len(A)) if i not in mentioned_from_indices]
        remaining_to_indices = [i for i in range(len(B)) if i not in mentioned_to_indices]
        if printing:
            print("All mentioned from indices: ", mentioned_from_indices)
            print("All mentioned to indices: ", mentioned_to_indices)
            print(f"All remaining from indices (length {len(remaining_from_indices)}): ", remaining_from_indices)
            print(f"All remaining to indices (length {len(remaining_to_indices)}):", remaining_to_indices)
        
        if not len(remaining_from_indices) == len(remaining_to_indices) and not auto_resolve:
            print("Error: lengths of unmentioned indices do not match.")
            show_indices = True
        
        if show_indices:
            print("Showing indices...")
            super().__init__(
                Create(index_labels(A, label_height=index_label_height, color=A_index_labels_color, background_stroke_width=3)),
                FadeIn(B.next_to(A, DOWN), shift=DOWN),
                Create(index_labels(B, label_height=index_label_height, color=B_index_labels_color, background_stroke_width=3)),
                Wait(5),
                lag_ratio=0.5
            )
        else:
            if auto_resolve:
                for j in remaining_to_indices:
                    animations.append(Succession(Wait(auto_resolve_delay), default_introducer(B[j])))
                for i in remaining_from_indices:
                    animations.append(Succession(Wait(auto_resolve_delay), default_remover(A[i])))
            else:
                for i,j in zip(remaining_from_indices, remaining_to_indices):
                    animations.append(ReplacementTransform(A[i], B[j], **kwargs))
            super().__init__(*animations, **kwargs)
def ir(a,b): #inclusive_range
    return list(range(a,b+1))
######### References end #########

class Main(Scene): #half down
    def construct(self):
        #start
        ax = Axes((-7, 7, 1), (-4, 4, 1), 14, 8).add_coordinates().set_opacity(0.5)
        plane = NumberPlane().set_opacity(0.3)
        #line and dot
        mainDot = Dot(ax.c2p(2, 2), color=GREEN)
        dot_label = always_redraw(lambda: Tex(f"({mainDot.get_x():.1f}, {mainDot.get_y():.1f})",color = GREEN).next_to(mainDot, RIGHT))
        y2func_projection = always_redraw(lambda: Dot(ax.c2p(mainDot.get_x(), 1.25 + 0.75 * mainDot.get_x()), color=RED))
        x2func_projection = always_redraw(lambda: Dot(ax.c2p((4 / 3) * mainDot.get_y() - (5 / 3), mainDot.get_y()), color=RED))
        x2f_proj_label = always_redraw(lambda: Tex(f"({x2func_projection.get_x():.2f}, {mainDot.get_y():.2f})",color = RED).next_to(x2func_projection, DR))
        y2f_proj_label = always_redraw(lambda: Tex(f"({mainDot.get_x():.2f}, {y2func_projection.get_y():.2f})",color = RED).next_to(y2func_projection, RIGHT))
        lineFunction = FunctionGraph(lambda t: 1.25 + 0.75 * t)
        y_distance = always_redraw(lambda: Line(y2func_projection, mainDot).set_opacity(0.7))
        x_distance = always_redraw(lambda: Line(x2func_projection, mainDot).set_opacity(0.7))
        func_name = Tex("3x-4y+5=0", color=YELLOW).move_to((-3,1,0))
        hypotenuse = always_redraw(lambda: Line(y2func_projection,x2func_projection))
        right_triangle = always_redraw(lambda: Polygon(x2func_projection.get_center(), y2func_projection.get_center(), mainDot.get_center()).set_fill(TEAL, opacity=0.7).set_stroke(width=0))
        #ex_1 = Tex(r"$\\text{slope}=-\\frac{a}{b}$")
        u = VGroup()
        u.add(*[plane, ax, lineFunction, func_name, mainDot, dot_label,x2func_projection,y2func_projection,x_distance, y_distance])
        l_AP_label = Tex(r"$\overline{AP} = \left| b \right| \cdot \ell$").move_to((-1, -2.5, 0))
        l_BP_label = Tex(r"$\overline{BP} = \left| a \right| \cdot \ell$").move_to((3.5, 0.5, 0))
        l_AB_label = Tex(r"$\overline{AB} = \sqrt{a^{2}+b^{2}}\cdot \ell$").move_to((-3.5,0.5,0))
        perpendicular_line = always_redraw(lambda: Line(mainDot.get_center(), hypotenuse.get_projection(mainDot.get_center())).set_opacity(0.7))
        foot_of_perpendicular = always_redraw(lambda: Dot(hypotenuse.get_projection(mainDot.get_center()), color=BLUE))
        foot_label = always_redraw(lambda: Tex("Q").next_to(foot_of_perpendicular,UL))
        right_angle_marker = always_redraw(lambda: RightAngle(perpendicular_line, hypotenuse, length=0.2, quadrant=(-1, -1)))
        qs =VGroup().add(*[perpendicular_line,foot_of_perpendicular,right_angle_marker,foot_label]) 
        areaTransform = Tex(r"$2\cdot \text{Triangle area} = \overline{AP} \cdot \overline{BP} = \overline{AB} \cdot \overline{PQ}$").move_to((-3.5,2.5,0)).scale(0.75)
        
        #################play########################
        self.play(Create(u), run_time=8)
        self.wait(0.5)
        self.play(Write(x2f_proj_label))
        y2f_proj_label.update()
        self.play(Write(y2f_proj_label))
        self.play(mainDot.animate.move_to(ax.c2p(1, 3)), run_time=2)
        self.play(mainDot.animate.move_to(ax.c2p(2, -2)), run_time=2)
        dot_label.clear_updaters()
        self.play(Transform(dot_label, Tex("$P(x_{0},y_{0})$",color = GREEN).next_to(mainDot, RIGHT)))
        self.play(Transform(func_name,Tex("ax+by+c=0", color=YELLOW).move_to((-3,1,0))))
        y2f_proj_label.clear_updaters()
        x2f_proj_label.clear_updaters()
        self.play(Transform(x2f_proj_label, Tex("$A(\\frac{-c-by_{0}}{a},y_{0})$",color = RED).move_to((-5.25, -1.25, 0))))
        self.play(Transform(y2f_proj_label, Tex("$B(x_{0},\\frac{-c-ax_{0}}{b})$",color = RED).next_to(y2func_projection, RIGHT)))
        right_triangle.update()
        self.play(FadeIn(right_triangle),FadeIn(hypotenuse))

        self.play(FadeOut(func_name,ax,lineFunction))
        self.play(Write(l_AP_label))
        self.play(Write(l_BP_label))
        self.play(Write(l_AB_label))
        qs.update()
        self.play(FadeIn(qs))
        self.play(Transform(l_AP_label,Tex(r"$\overline{AP} = \left| b \right| \cdot \ell$").move_to((-1.75, -2.5, 0))))
        self.play(TransformMatchingShapes(l_AP_label,Tex(r"$\overline{AP} = \left| b \right| \cdot \ell = |x_{0}-\frac{-c-by_{0}}{a}|$").move_to((-1.75, -2.5, 0))))
        self.play(Write(areaTransform))
        self.play(FadeOut(plane, qs, x_distance, y_distance, mainDot, dot_label, x2func_projection, x2f_proj_label, y2func_projection, y2f_proj_label, right_triangle, hypotenuse))
        
        
        #end
        self.wait(1)

class deELL(Scene): #DONE
    def construct(self): #manim -pql linepoint.py deELL
        f0 = MathTex("\\overline{AB} = \\sqrt{a^2 + b^2} \\cdot \\ell").move_to((0,2,0)).align_on_border(LEFT,buff=1)
        f1 = MathTex("\\overline{BP} = |a| \\cdot \\ell").move_to((0,0,0)).align_on_border(LEFT,buff=1)   
        f2 = MathTex("\\overline{AP} = |b| \\cdot \\ell = \\left| x_0 - \\frac{-c - by_0}{a} \\right|").move_to((0,-2,0)).align_on_border(LEFT,buff=1)
        f3 =MathTex("\\frac{\\overline{AB}}{\\sqrt{a^2 + b^2}} = \\frac{\overline{BP}}{|a|} = \\frac{\overline{AP}}{|b|}=\\ell")
        #self.play(Write(f0to2))
        f02 = MathTex("\\frac{\\overline{AB}}{\\sqrt{a^2 + b^2}} =\\ell").move_to((0,2,0)).align_on_border(LEFT,buff=1)
        f12 = MathTex("\\frac{\\overline{BP}}{|a|} =\\ell").move_to((0,0,0)).align_on_border(LEFT,buff=1)   
        f22 = MathTex("\\frac{\\overline{AP}}{|b|} = \\ell").move_to((0,-2,0)).align_on_border(LEFT,buff=1)
        f_0_2 =VGroup(f02,f12,f22)
        f3 = MathTex("\\frac{\\overline{AB}}{\\sqrt{a^2 + b^2}} = \\frac{\\overline{BP}}{|a|} = \\frac{\\overline{AP}}{|b|}=\\ell").move_to(ORIGIN).shift(UP*2)
        f4 = Text("\"ell\" could be anything,\n and it wouldn't break the relation between others.\n So let's let it be 1, and now they look like this...").shift(DOWN).scale(0.75)

        f03 = MathTex("\\overline{AB} = \\sqrt{a^2 + b^2}").move_to((0,1.25,0)).align_on_border(LEFT,buff=1)
        f13 = MathTex("\\overline{BP} = |a|").move_to((0,0,0)).align_on_border(LEFT,buff=1)
        f23 = MathTex("\\overline{AP} = |b| = \\left| x_0 - \\frac{-c - by_0}{a} \\right|").move_to((0,-1.25,0)).align_on_border(LEFT,buff=1)

        self.play(FadeIn(f0))
        self.play(TransformByGlyphMap(f0,f02,([3],[11]),([11],[3])))
        self.play(FadeIn(f1))
        self.play(TransformByGlyphMap(f1,f12,([3],[7]),([7],[3])))
        self.play(FadeIn(f2))
        self.play(TransformByGlyphMap(f2,f22,([3],[7]),([7],[3]),(range(9,29),[])))
        
        self.play(Transform(f_0_2,f3))
        self.play(Write(f4))
        self.wait()
        self.play(FadeOut(f3),FadeOut(f4),FadeOut(f_0_2),FadeIn(f03),FadeIn(f13),FadeIn(f23))

        self.wait()
        #self.play(ReplacementTransform(f012,f3))

class y2XZero(Scene): #DONE S2
    def construct(self):
        f0 = MathTex("ax","+","b","y","+","c","=","0")
        f1 = MathTex("ax_{{0}}","+","b","y","+","c","=","0")
        f2 = MathTex("ax_{{0}}","+","b","y","=","-","c")
        f3 = MathTex("b","y","=","-","c","-","ax_{{0}}")
        f4 = MathTex("y","=","\\frac{-c-ax_{0}}{b}")     
        self.play(Write(f0))
        self.play(TransformMatchingShapes(f0,f1),run_time = 2)
        self.play(TransformMatchingShapes(f1,f2),run_time = 2)
        self.play(TransformMatchingShapes(f2,f3),run_time = 2)
        self.play(TransformMatchingShapes(f3,f4),run_time = 2)
        self.wait(1)

class x2YZero(Scene): #DONE S3
    def construct(self):
        f0 = MathTex("a","x","+","b","y","+","c","=","0")
        f1 = MathTex("a","x","+","b","y_{{0}}","+","c","=","0")
        f2 = MathTex("a","x","+","b","y_{{0}}","=","-","c")
        f3 = MathTex("a","x","=","-","c","-","b","y_{{0}}")
        f4 = MathTex("x","=","\\frac{-c-by_{0}}{a}")
        self.play(Write(f0))
        self.play(TransformMatchingShapes(f0,f1),run_time = 2)
        self.play(TransformMatchingShapes(f1,f2),run_time = 2)
        self.play(TransformMatchingShapes(f2,f3),run_time = 2)
        self.play(TransformMatchingShapes(f3,f4),run_time = 2)
        self.wait(1)

class exABPQ(Scene): #DONE S5
    def construct(self):
        fs = [
            MathTex("\\overline{PQ}\\cdot\\overline{AB}=\\overline{AP}\\cdot\\overline{BP}"),
            MathTex("\\overline{PQ}=\\overline{AP} \\cdot\\frac{\\overline{BP}}{\\overline{AB}}"),
            MathTex("\\overline{PQ}=|x_{0}-\\frac{-by_{0}-c}{a}|\\cdot\\frac{\\overline{BP}}{\\overline{AB}}"),
            MathTex("\\overline{PQ}=|x_{0}-\\frac{-by_{0}-c}{a}|\\cdot\\frac{|a|}{\\overline{AB}}"),
            MathTex("\\overline{PQ}=|x_{0}-\\frac{-by_{0}-c}{a}|\\cdot\\frac{|a|}{\\sqrt{a^{2}+b^{2}}}"),
            MathTex("\\overline{PQ}=|x_{0}+\\frac{by_{0}+c}{a}|\\cdot\\frac{|a|}{\\sqrt{a^{2}+b^{2}}}"),
            MathTex("\\overline{PQ}=|\\frac{ax_{0}}{a}+\\frac{by_{0}+c}{a}|\\cdot\\frac{|a|}{\\sqrt{a^{2}+b^{2}}}"),
            MathTex("\\overline{PQ}=|\\frac{ax_{0}+by_{0}+c}{a}|\\cdot\\frac{|a|}{\\sqrt{a^{2}+b^{2}}}"),
            MathTex("\\overline{PQ}=\\frac{|ax_{0}+by_{0}+c|}{|a|}\\cdot\\frac{|a|}{\\sqrt{a^{2}+b^{2}}}"),
            MathTex("\\overline{PQ}=\\frac{|ax_{0}+by_{0}+c|\\cdot|a|}{|a|\\cdot\\sqrt{a^{2}+b^{2}}}"),
            MathTex("\\overline{PQ}=\\frac{|ax_{0}+by_{0}+c|}{\\sqrt{a^{2}+b^{2}}}")

            #MathTex(""),
        ]
        #it takes two day
        self.play(TransformByGlyphMap(fs[0],fs[1],([3],[11]),([4,5,6],[12,13,14]),([7],[3]),([8,9,10],[4,5,6]),([11],[7]),([12,13,14],[8,9,10])),run_time = 1.5)
        self.wait(1)
        self.play(TransformByGlyphMap(fs[1],fs[2],([] ,[4,5,6,7,8,9,10,11,12,13,14,15,16]),([0,1,2],[0,1,2]), ([4,5,6],[])),run_time = 1.5)
        self.wait(1)
        self.play(TransformByGlyphMap(fs[2],fs[3],([18,19,20],[]),([],[18,19,20])),run_time = 1.5)
        self.wait(1)
        self.play(TransformByGlyphMap(fs[3],fs[4],(range(22,25),[]),([],range(22,29))),run_time = 1.5)
        self.wait(1)
        self.play(TransformByGlyphMap(fs[4],fs[5],([8],[]),([7],[7]),([12],[11]),([13],[12])),run_time = 1.5)
        self.wait(1)
        self.play(TransformByGlyphMap(fs[5],fs[6],(range(7,28),range(10,31)),([],[5,8,9])),run_time = 1.5)
        self.wait(1)
        self.play(TransformByGlyphMap(fs[6],fs[7],([10],[8]),([8],[14]),(range(11,31),range(9,29)),([9],[15])),run_time = 1.5)
        self.wait(1)
        self.play(TransformByGlyphMap(fs[7],fs[8],([4],[4,16]),([16],[14,18]),([14],[15]),([15],[17]),(range(17,29),range(19,31))),run_time = 1.5)
        self.wait(1)
        self.play(TransformByGlyphMap(fs[8],fs[9],([15,23],[19]),([20,21,22],[16,17,18]),([16,17,18],[20,21,22]),([19],[15,23]),(range(24,31),range(24,31))),run_time = 1.5)
        self.wait(1)
        self.play(TransformByGlyphMap(fs[9],fs[10],(range(15,19),[]),(range(20,24),[])),run_time = 1.5)
        self.wait(2)

# code end
