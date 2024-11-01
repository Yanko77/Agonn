import time


class Date:

    def __init__(self,
                 days: int,
                 hour,
                 ):
        self.days = days
        self.hour = hour

    def is_between(self, other1, other2):
        if other1 == other2:
            return self == other1
        elif other1 < other2:
            return other1 <= self < other2
        else:
            return other1 <= self or self < other2

    def __str__(self):
        return f'{self.days} {self.hour.hours}:{self.hour.minutes}'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Date):
            raise TypeError('Can only compare two Date objects')

        return self.days == other.days and self.hour == other.hour

    def __lt__(self, other) -> bool:
        if not isinstance(other, Date):
            raise TypeError('Can only compare two Date objects')

        return self.days == other.days and self.hour < other.hour or self.days < other.days

    def __le__(self, other) -> bool:
        if not isinstance(other, Date):
            raise TypeError('Can only compare two Date objects')

        return self == other or self < other


class Hour:

    def __init__(self,
                 hours: int,
                 minutes: int):
        self.hours = hours
        self.minutes = minutes

    def is_between(self, other1, other2):
        if other1 == other2:
            return self == other1
        elif other1 < other2:
            return other1 <= self < other2
        else:
            return other1 <= self or self < other2

    def __eq__(self, other) -> bool:
        if not isinstance(other, Hour):
            raise TypeError('Can only compare two Hour objects')

        return self.hours == other.hours and self.minutes == other.minutes

    def __lt__(self, other) -> bool:
        if not isinstance(other, Hour):
            raise TypeError('Can only compare two Hour objects')

        return self.hours == other.hours and self.minutes < other.minutes or self.hours < other.hours

    def __le__(self, other) -> bool:
        if not isinstance(other, Hour):
            raise TypeError('Can only compare two Hour objects')

        return self == other or self < other


class Time:
    """
    Classe qui gère le temps dans le jeu
    """

    TIME_RATIO = 60  # 1h in-game correspond à TIME_RATIO secondes en temps réel.

    def __init__(self):
        self.INITIAL_TIME = time.perf_counter_ns()

    @property
    def _get_all(self) -> int:
        """
        Renvoie le temps écoulé (arrondi à l'entier inférieur) en seconde depuis le début du jeu.
        """
        return int((time.perf_counter_ns() - self.INITIAL_TIME) * 10 ** -9)

    @property
    def day(self) -> int:
        """
        Renvoie le jour de jeu courant.
        """
        return self._get_all // (self.TIME_RATIO * 24)

    @property
    def hour(self) -> Hour:
        """
        Renvoie l'heure de jeu courante : (heure, minutes)
        """

        hours = (self._get_all - self.day*self.TIME_RATIO*24) // self.TIME_RATIO
        minutes = (self._get_all - self.day*self.TIME_RATIO*24 - hours*self.TIME_RATIO) * 60 // self.TIME_RATIO
        return Hour(hours, minutes)

    @property
    def now(self) -> Date:
        return Date(self.day, self.hour)


if __name__ == '__main__':
    t = Time()
