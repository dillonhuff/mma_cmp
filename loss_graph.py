class LossGraph:

    def __init__(self):
        self.fightersToLosses = {}
        self.fightersToWins = {}

    def addFight(self, winner, loser):
        if not (winner in self.fightersToWins):
            self.fightersToWins[winner] = []

        if not (loser in self.fightersToLosses):
            self.fightersToLosses[loser] = []

        self.fightersToWins[winner].append(loser)
        self.fightersToLosses[loser].append(winner)
        
    def fighter_wins(self, fighter):
        return self.fightersToWins[fighter]

    def fighter_losses(self, fighter):
        return self.fightersToLosses[fighter]
    
