class Score:
    def __init__(self):
        self.score = 0

    def calculate(self, lives, remaining_time):
        """
        Calcule le score en fonction des cœurs restants et du temps restant.
        """
        # Points pour les cœurs restants
        if lives == 3:
            self.score += 3000
        elif lives == 2:
            self.score += 2000
        elif lives == 1:
            self.score += 1000

        # Points pour le temps restant
        seconds_left = remaining_time
        self.score += max(0, 6000 - (60 - seconds_left) * 100)  # Perte de 100 points par seconde écoulée

    def get_score(self):
        return self.score
