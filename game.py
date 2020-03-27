MIN_PLAYERS = 1

class Game():

    def __init__(self):
        self.players = {}
        self.started = False
        self.rounds = 0

    def add_player(self, player):
        if player.id in self.players:
            return False
        self.players[player.id] = player.username
        return True

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
