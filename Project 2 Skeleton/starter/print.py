import collections, sys, os
from logic import *
from planning import *
from csp import sum_constraint

print("HELLO")
initial_state = 'At(C1, D1) & At(C2, D1) & At(C3, D2) & At(R1, D1) & In(C1, R1)'
goal_state = 'At(C1, D3) & At(C2, D3) & At(C3, D3) & At(R1, D3)'
planning_problem = \
PlanningProblem(initial=initial_state,
                goals=goal_state,
                    actions=[Action('Load(c,r,d)',
                                    precond='At(c, d) & At(r, d)',
                                    effect='In(c, r) & ~At(c, d)',
                                    domain='Cargo(c) & Robot(r) & Dest(d)'),
                            Action('Unload(c, r, d)',
                                    precond='In(c, r) & At(r, d)',
                                    effect='At(c, d) & ~In(c, r)',
                                    domain='Cargo(c) & Robot(r) & Dest(d)'),
                            Action('Travel(r, f, to)',
                                    precond='At(r, f)',
                                    effect='At(r, to) & ~At(r, f)',
                                    domain='Robot(r) & Dest(f) & Dest(to)')],
                    domain='Cargo(C1) & Cargo(C2) & Cargo(C3) & Robot(R1) & Dest(D1) & Dest(D2) & Dest(D3)')
a = linearize(GraphPlan(planning_problem).execute())
print(*a, sep = '\n')
print('\n\n')
if(planning_problem.goal_test):
    print("goal reached")
else:
    print("goal not reached")