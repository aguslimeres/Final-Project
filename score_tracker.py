"""
score_tracker.py

Contains the ScoreTracker class, which records and computes the
player's running score from multiple rounds.

Scoring rules:
  - +100 points for a win
  - Bonus points for remaining guesses: +10 x remaining_guesses
  - No points (and no penalty) for a loss
  - Win streaks multiply the win bonus: streak x 100

"""

class ScoreTracker:
    """
    Keeps a running tally of wins, losses, streak, and total score.

    Has-a: integer counters for wins, losses, streak, and total score.

    Attributes:
        wins (int): Total rounds won.
        losses (int): Total rounds lost.
        streak (int): Current consecutive-win streak.
        best_streak (int): Highest streak reached this session.
        total_score (int): Cumulative score across all rounds.
    """

    WIN_BASE = 100       # base points for winning a round
    GUESS_BONUS = 10     # extra points per remaining guess on a win

    def __init__(self):
        #Create a fresh ScoreTracker with all counters at zero.
        self.wins: int = 0
        self.losses: int = 0
        self.streak: int = 0
        self.best_streak: int = 0
        self.total_score: int = 0

    #Recording results
    def record_win(self, remaining_guesses: int) -> int:
        """
        Record a won round and return the points earned this round.

        Points = (WIN_BASE × streak_multiplier) + (GUESS_BONUS × remaining_guesses)
        The streak multiplier is max(1, current_streak) before incrementing.

        Args:
            remaining_guesses (int): Wrong guesses still available when won.

        Returns:
            int: Points awarded for this round.
        """
        self.wins += 1
        self.streak += 1
        if self.streak > self.best_streak:
            self.best_streak = self.streak

        multiplier = self.streak  # streak already incremented
        points = (self.WIN_BASE * multiplier) + (self.GUESS_BONUS * remaining_guesses)
        self.total_score += points
        return points

    def record_loss(self) -> int:
        """
        Record a lost round. Resets the streak and returns 0 points.

        Returns:
            int: Always 0 (no points awarded for a loss).
        """
        self.losses += 1
        self.streak = 0
        return 0

    #Display helpers
    def rounds_played(self) -> int:
        #Return the total number of rounds played so far.
        return self.wins + self.losses

    def win_rate(self) -> float:
        #Return the win rate as a value between 0.0 and 1.0.
        #Returns 0.0 if no rounds have been played yet.
        total = self.rounds_played()
        return self.wins / total if total > 0 else 0.0

    def summary(self) -> dict:
        """
        Return a dictionary summarising all score statistics.

        Returns:
            dict with keys: wins, losses, streak, best_streak,
                            total_score, rounds_played, win_rate.
        """
        return {
            "wins": self.wins,
            "losses": self.losses,
            "streak": self.streak,
            "best_streak": self.best_streak,
            "total_score": self.total_score,
            "rounds_played": self.rounds_played(),
            "win_rate": self.win_rate(),
        }