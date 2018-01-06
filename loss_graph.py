class LossGraph:

    def __init__(self):
        self.fightersToLosses = {}
        self.fightersToWins = {}
        self.fighters = {}

    def getFighters(self):
        return self.fighters

    def addFight(self, winner, loser):
        if not (winner in self.fighters):
            self.fighters[winner] = True
        if not (loser in self.fighters):
            self.fighters[loser] = True

        if not (winner in self.fightersToWins):
            self.fightersToWins[winner] = []

        if not (loser in self.fightersToLosses):
            self.fightersToLosses[loser] = []

        self.fightersToWins[winner].append(loser)
        self.fightersToLosses[loser].append(winner)
        
    def fighter_wins(self, fighter):
        if not (fighter in self.fightersToWins):
            return {}

        return self.fightersToWins[fighter]

    def fighter_losses(self, fighter):
        if not (fighter in self.fightersToLosses):
            return {}

        return self.fightersToLosses[fighter]
    
# Idea: PageRank fighters, that gives a ranking based on wins and losses, but
# it doesnt give any insight into how well those rankings reflect actual ability

# Idea: Measure distance of the fighter win graph to a lattice. Question here is
# how to interpret results

# Idea: Follow the existing "Does MMA math work?" study and build a classifier
# that predicts MMA wins / losses by conditioning priors on rankings

# Idea: Measure the effect of reach in MMA. A different question, but one I'm
# interested in. Closer to classical statistics as well, which makes getting started
# easier. Also the conclusions may be less obvious

# Idea: Model fighters ability A(t) as a random function of time. A(t) is sampled
# at each fight. Task is to estimate which fighter has best average A(t)? I like this
# model because it is logically consistent, eg it can accomodate all the data without
# requiring logical contradictions. OTOH what can we assume about fighter ability
# functions to allow inference? Also, how do we start to assign numbers to these
# functions? Just create an arbitrary baseline like calling one guy zero and another
# guy one at some fight? Problem: Are there multiple disconnected components in
# the fight graph? Q: How fast do these ability functions change? Rate of change of
# ability functions might actually be an interesting study

# Note: When Silva lost to Chris Weidman was that a sign that his ability function
# went way down, or that Weidmans ability function went way up?

# In this model time is a list of points (matches at each time). At each match
# point the skill of the winner is substantially above the skill of the loser

# Goal of the regression is to assign numerical values to each one such that the
# skill changes are minimized across the same fighter over time. Or so that sudden
# ability changes dont happen much. Problem: Sudden ability changes do sometimes
# happen, (injuries, guy comes off PEDs, gets on PEDs, life tragedies, etc)

# Idea: Let eps be the maximum acceptable skill change between fights, then
# do a series of SAT problems that solve for this skill change? Extreme case:
# epsilon = 0, then skills are a constant. Hyp: eps = 0 change can only
# fit the data if the data is a lattice?

# What is the contraint problem: a_t > b_t for each fight, and for each
# fighter with n fights, s_1, ..., s_n it must be the case that
#
#           | s_i - s_(i + 1) | < eps
#
# This is going to be a quadratic programming problem? Or
#
#      -eps < s_i - s_(i + 1) < eps
#
#      (-eps < s_i - s_(i + 1)) and (s_i - s_(i + 1) < eps)
#
# which is still linear programming
#
# Q: Could this method be used to detect sudden losses of skill? How do you isolate
# which specific losses represent sudden declines, and which represent a gradual
# loss of skill, and which represent a person who was higher skill showing up?

# Q: How large is this constraint problem?
# A: 1 constraint per fight for the difference in skill
#    2 constraints to express before and after skill constraints for EACH fighter
#    --- 5 constraints per fight maximum, 5*n constraints ~ 1e6 for a database of
#    200k fights, though some components are not connected

# This is a purely SAT based approach, no probability. I suppose probability comes
# in when trying to estimate how much of the variance in ability is due to factors
# beyond the fighters control?

# Note: In this method there is no upper bound on performance of undefeated fighters.
# As far as this method is concerned Jon Jones could be 1000x better than anybody
# else in his division because he has never been beaten. Maybe introduce decisions
# vs. KOs (some measure of margin of victory?).

# Idea: Only include the outcomes as requirements for SAT. Then include an
# optimization criteria that tries to smooth out differences in skill between
# fights and minimize that skill difference criteria

# Idea: Maybe also add a penalty for estimating a fighters skill to be far above
# the skill of anybody he beat?

# Idea: Skill is multidimensional, try to group fighters by strategy? Some sort of
# clustering based on who they beat?
