import logging
MIN_PLAYERS = 1

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.DEBUG)

class Game():

    def __init__(self):
        self.players = {}
        self.started = False
        self.rounds = 0
        self.turn_generator = None

    @staticmethod
    def init(self, dict_path):
        pass

    def add_player(self, player):
        if player.id in self.players:
            return False
        self.players[player.id] = player.username
        return True

    def generate_turns(self, rounds):
        logging.debug("call generate_turns()")
        assert(self.started)
        people = list(self.players.items())
        # XXX temp
        for pair in [(people[0], people[-1]), (people[-1], people[0])]:
            yield pair
        """
        n = len(people)
        for _ in range(rounds):
            for j in range(1, n):
                for i in range(n):
                    yield (people[i], people[(i + j) % n])
        """


    def next_turn(self):
        return next(self.turn_generator)

    def log_explained(self, explainer, guesser, word):
        pass

    def log_skipped(self, explainer, word):
        pass

    def next_word(self, player):
        return "КРОКОДИЛ"

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
        self.turn_generator = self.generate_turns(self.rounds)

    def finish(self):
        self.started = False
        stats = {}
        return stats
