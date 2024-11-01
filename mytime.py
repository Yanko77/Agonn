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

    TIME_RATIO = 60  # 1h in-game correspond à TIME_RATIO nanosecondes en temps réel.

    def __init__(self):
        self.clock = Clock(self, time_ratio=self.TIME_RATIO)

        self.value = 0  # Valeur de temps. Nombre de nanosecondes écoulées ingame.

    def update(self):
        self.clock.tick()

    def get(self):
        return ns_to_s(self.value)

    @property
    def day(self) -> int:
        """
        Renvoie le jour de jeu courant.
        """
        return self.get() // (self.TIME_RATIO * 24)

    @property
    def hour(self) -> Hour:
        """
        Renvoie l'heure de jeu courante sous la forme d'un objet Hour.
        """

        current_day_time_value = self.get() - self.day * self.TIME_RATIO * 24
        hours = current_day_time_value // self.TIME_RATIO

        current_hour_time_value = current_day_time_value - hours * self.TIME_RATIO
        minutes = current_hour_time_value * 60 // self.TIME_RATIO

        return Hour(hours, minutes)

    @property
    def now(self) -> Date:
        return Date(self.day, self.hour)


class Clock:

    def __init__(self,
                 time_manager: Time,
                 time_ratio: int):
        self.manager = time_manager

        self.time_ratio = time_ratio
        self.speed = 100

        self.initial_time = time.perf_counter_ns()
        self._previous_elapsed_time = self.initial_time

    @property
    def elapsed_time(self) -> int:
        """ Renvoie le temps réel en nanosecondes écoulé depuis le début du jeu. """
        return time.perf_counter_ns() - self.initial_time

    def tick(self):
        """ Met à jour l'horloge """

        # On récupère la valeur de temps écoulé de l'itération de boucle du jeu précédente.
        elapsed_time = self.elapsed_time

        # On détermine l'incrément attendu et celui réellement appliqué, modifié par la vitesse de jeu.
        expected_increment = elapsed_time - self._previous_elapsed_time
        increment = int(expected_increment * self.speed / 100)

        # On incrémente.
        self.manager.value += increment

        # On stocke la valeur de temps écoulé de l'itération courante, pour l'utiliser lors de l'itération suivante.
        self._previous_elapsed_time = elapsed_time


def ns_to_s(value_in_ns) -> int:
    """
    Convertit une valeur initialement en nanosecondes en secondes.
    Renvoie la partie entière.
    """
    return int(value_in_ns * 10 ** -9)


def s_to_ns(value_in_s) -> int:
    """
    Convertit une valeur initialement en secondes en nanosecondes.
    Renvoie la partie entière.
    """
    return int(value_in_s * 10 ** 9)


if __name__ == '__main__':
    t = Time()

    while True:
        t.update()
        # print(t.value)
        print(t.now)
