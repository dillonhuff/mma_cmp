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
    
