from statek import Statek,PoleStatku

class GameState:
    def __init__(self, stateLogger, update_ui):
        """
        stateLogger:param
            Stan gry, przechowuje:
            turn_no      int:  numer tury
            in_progress -  0:  gra sie toczy
                           1:  gra wygrana
                          -1:  gra przegrana
            my_turn -   bool:  czy moja kolej
            my_ships[list]:    moje statki
            sunk_ships[list]:  zatopione statki wroga
            ship_count[dict]:  liczba moich statkow
        """
        self._stateLogger = stateLogger
        self._turn_no = 0
        self._in_progress = 0
        self._my_turn = False
        self._my_ships = []
        self._sunk_ships = []
        self._enemy_count = {1: 4, 2: 3, 3: 2, 4: 1}
        self._ship_count = {1: 0, 2: 0, 3: 0, 4: 0}
        self._update_ui = update_ui

    def next_turn(self):
        self._turn_no += 1

    def add_my_ship(self, selection):
        lista_pol = []
        for wsp in selection:
            lista_pol.append(PoleStatku(wsp, False))
        new_ship = Statek(lista_pol)
        assert self.is_ship_allowed(new_ship.get_size())
        self._my_ships.append(new_ship)
        self.increment_ship_count(new_ship.get_size())
        self._update_ui()

    def reset_ship_count(self):
        for key in self._my_ships:
            self._ship_count[key] = 0

    def increment_ship_count(self, key):
        self._ship_count[key] += 1

    def decrement_ship_count(self, key):
        self._enemy_count[key] += 1

    def get_ship_count(self, key):
        return self._ship_count[key]

    def is_ship_allowed(self, key):
        return self.get_ship_count(key) < 5 - key

    def get_enemy_ship_count(self, key):
        return self._enemy_count[key]

    def get_my_ships(self):
        return self._my_ships;

    def get_enemy_ships(self):
        return self._sunk_ships

    def ready_for_battle(self):
        return self._enemy_count == self._ship_count
