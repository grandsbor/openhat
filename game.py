class Game():
    def __init__(self):
        self.players = set()

    def add_player(self, player_id):
        if player_id in self.players:
            return False
        self.players.add(player_id)
        return True
