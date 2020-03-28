import logging
MIN_PLAYERS = 1

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.DEBUG)

class Game():

    def __init__(self):
        self.players = {}
        self.started = False
        self.rounds = 0

    @staticmethod
    def init(self, dict_path):
        pass

    def add_player(self, player):
        if player.id in self.players:
            return False
        self.players[player.id] = player.username
        return True

    def next_turn(self):
        assert(self.started)
        people = list(self.players.items())
        return [(people[0], people[-1])]  # XXX temp
        """
        n = len(people)
        for j in range(1, n):
            for i in range(n):
                yield (people[i], people[(i + j) % n])
        """

    def next_word(self, player):
        return ""

    def start(self, args):
        if self.started:
            raise Exception("Игра уже началась")
        if len(self.players) < MIN_PLAYERS:
            raise Exception("Слишком мало игроков")
        try:
            self.rounds = int(args[0])
            assert(self.rounds > 0)
        except Exception as e:
            raise Exception("Укажите число кругов, например так: /go 2")
        self.started = True

    def finish(self):
        self.started = False
        stats = {}
        return stats
