import collections, sys, os
from logic import *
from planning import *
from csp import sum_constraint

    # REFLECTION IN COMMENTS, AFTER 4B #

############################################################
# Problem 1: propositional logic
# Convert each of the following natural language sentences into a propositional
# logic formula.  See rainWet() in examples.py for a relevant example.

# Sentence: "If it's summer and we're in California, then it doesn't rain."
def formula1a():
    # Predicates to use:
    Summer = Atom('Summer')               # whether it's summer
    California = Atom('California')       # whether we're in California
    Rain = Atom('Rain')                   # whether it's raining
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return Implies(And(Summer, California),Not(Rain))
    # END_YOUR_CODE

# Sentence: "It's wet if and only if it is raining or the sprinklers are on."
def formula1b():
    # Predicates to use:
    Rain = Atom('Rain')              # whether it is raining
    Wet = Atom('Wet')                # whether it it wet
    Sprinklers = Atom('Sprinklers')  # whether the sprinklers are on
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return Equiv(And(Not(Rain),Not(Sprinklers)),Not(Wet))
    # END_YOUR_CODE

# Sentence: "Either it's day or night (but not both)."
def formula1c():
    # Predicates to use:
    Day = Atom('Day')     # whether it's day
    Night = Atom('Night') # whether it's night
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return Equiv(Day,Not(Night))
    # END_YOUR_CODE

############################################################
# Problem 2: first-order logic

# Sentence: "Every person has a mother."
def formula2a():
    # Predicates to use:
    def Person(x): return Atom('Person', x)        # whether x is a person
    def Mother(x, y): return Atom('Mother', x, y)  # whether x's mother is y

    # Note: You do NOT have to enforce that the mother is a "person"
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return Forall('$x',Exists('$y',Implies(Person('$x'),Mother('$x','$y'))))
    # END_YOUR_CODE

# Sentence: "At least one person has no children."
def formula2b():
    # Predicates to use:
    def Person(x): return Atom('Person', x)        # whether x is a person
    def Child(x, y): return Atom('Child', x, y)    # whether x has a child y

    # Note: You do NOT have to enforce that the child is a "person"
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return Exists('$x',Forall('$y',And(Person('$x'),Not(Child('$x','$y')))))
    # END_YOUR_CODE

# Return a formula which defines Daughter in terms of Female and Child.
# See parentChild() in examples.py for a relevant example.
def formula2c():
    # Predicates to use:
    def Female(x): return Atom('Female', x)            # whether x is female
    def Child(x, y): return Atom('Child', x, y)        # whether x has a child y
    def Daughter(x, y): return Atom('Daughter', x, y)  # whether x has a daughter y
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    return Forall('$x', Forall('$y', Equiv(Daughter('$x', '$y'), And(Child('$x', '$y'), Female('$y')))))
    # END_YOUR_CODE

# Return a formula which defines Grandmother in terms of Female and Parent.
# Note: It is ok for a person to be her own parent
def formula2d():
    # Predicates to use:
    def Female(x): return Atom('Female', x)                  # whether x is female
    def Parent(x, y): return Atom('Parent', x, y)            # whether x has a parent y
    def Grandmother(x, y): return Atom('Grandmother', x, y)  # whether x has a grandmother y
    # BEGIN_YOUR_CODE (our solution is 5 lines of code, but don't worry if you deviate from this)
    return Forall('$x', Forall('$z', Equiv(Grandmother('$x', '$z'),
    And(Female('$z'),Exists('$y',And(Parent('$x','$y'),Parent('$y','$z')))))))                                      
    # END_YOUR_CODE

############################################################
# Problem 3: Liar puzzle

# Facts:
# 0. John: "It wasn't me!"
# 1. Susan: "It was Nicole!"
# 2. Mark: "No, it was Susan!"
# 3. Nicole: "Susan's a liar."
# 4. Exactly one person is telling the truth.
# 5. Exactly one person crashed the server.
# Query: Who did it?
# This function returns a list of 6 formulas corresponding to each of the
# above facts.
# Hint: You might want to use the Equals predicate, defined in logic.py.  This
# predicate is used to assert that two objects are the same.
# In particular, Equals(x,x) = True and Equals(x,y) = False iff x is not equal to y.
def liar():
    def TellTruth(x): return Atom('TellTruth', x)
    def CrashedServer(x): return Atom('CrashedServer', x)
    john = Constant('john')
    susan = Constant('susan')
    nicole = Constant('nicole')
    mark = Constant('mark')
    formulas = []
    # We provide the formula for fact 0 here.
    formulas.append(Equiv(TellTruth(john), Not(CrashedServer(john))))
    # You should add 5 formulas, one for each of facts 1-5.
    # BEGIN_YOUR_CODE (our solution is 11 lines of code, but don't worry if you deviate from this)
    formulas.append(Equiv(TellTruth(susan), CrashedServer(nicole)))
    formulas.append(Equiv(TellTruth(mark),CrashedServer(susan)))
    formulas.append(Equiv(TellTruth(nicole),Not(TellTruth(susan))))
    formulas.append(Exists('$y',Forall('$x',Equiv(TellTruth('$x'),Equals('$x','$y')))))
    formulas.append(Exists('$y', Forall('$x',Equiv(CrashedServer('$x'), Equals('$x', '$y')))))
    # END_YOUR_CODE
    query = CrashedServer('$x')
    return (formulas, query)


############################################################
# Problem 4: Planning 

# Blocks world modification
def blocksWorldModPlan():
    # BEGIN_YOUR_CODE (make modifications to the initial and goal states)
    initial_state = 'On(A, B) & Clear(A) & OnTable(B) & OnTable(D) & On(C,D) & Clear(C)'
    goal_state = 'On(B, A) & On(C, B) & On(D, C)'
    # END_YOUR_CODE

    planning_problem = \
    PlanningProblem(initial=initial_state,
                    goals=goal_state,
                    actions=[Action('ToTable(x, y)',
                                    precond='On(x, y) & Clear(x)',
                                    effect='~On(x, y) & Clear(y) & OnTable(x)'),
                             Action('FromTable(y, x)',
                                    precond='OnTable(y) & Clear(y) & Clear(x)',
                                    effect='~OnTable(y) & ~Clear(x) & On(y, x)')])
    
    return linearize(GraphPlan(planning_problem).execute())

def logisticsPlan():
    # BEGIN_YOUR_CODE (use the previous problem as a guide and uncomment the starter code below if you want!)
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
    # END_YOUR_CODE     
    return linearize(GraphPlan(planning_problem).execute())


# **IMPORTANT** Reflection (4 pts)
# Please *breifly* report your findings and 
# reflect on what they mean:
#While the planning problem reports that the goal state has been reached,
#after running the problem multiple times and printing out the actions taken,
#the execution seems to interchange between an incorrect and correct set of actions. For example, 
#on a particular run, the first step that the GraphPlan.execute() took was: Unload(C2, R1, D3)
#However, initially, we know that R1 is currently carrying C1, which means that a slew
#of actions, including an unload of C1, a load of C2, and multiple travels to D2 & D3 had been
#skipped. On a different run, the plan started with a Load(C3, R1, D2), followed by an Unload(C1,R1,D3). 
#In this case, we see that the correct first move should've been the second one (Unload), as it is the 
#most effective one, time-wise, and the one that makes the most sense. At the end of every run, however, 
#we check the final state produced by the planning problem against the goal state that we manually put in, 
#and see that the function returns true, meaning the goal was reached. I believe this disordering of actions
#is due to them being executed synchronously, causing some actions to overlap, and be printed out of order,
#but still produce the correct result.
