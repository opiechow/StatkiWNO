class GameState:
    def __init__(self):
        self.in_progress = False
        self.my_turn = False
        self.my_ships = {1:0,2:0,3:0,4:0}

    def reset_ships(self):
        for key in self.my_ships:
            self.my_ships[key] = 0

    def add_ship(self, key):
        self.my_ships[key] += 1

    def get_ship(self, key):
        return self.my_ships[key]