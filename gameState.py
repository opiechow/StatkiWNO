from statek import Statek,PoleStatku
from stateLogger import StateLogger,LoggedState

class GameState:
    def __init__(self, stateLogger, hit_sound):
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
        self._state_logger = stateLogger
        self._turn_no = 0
        self._in_progress = 0
        self._my_turn = False
        self._my_ships = []
        self._my_sunk_ships = []
        self._sunk_ships = []
        self._enemy_count = {1: 4, 2: 3, 3: 2, 4: 1}
        self._ship_count = {1: 0, 2: 0, 3: 0, 4: 0}
        self._state_changed = False
        self._hit_sound = hit_sound

    def set_logged_state(self,log):
        assert isinstance(log,LoggedState)
        self._ship_count = log.ship_count;
        self._enemy_count = log.enemy_count;
        self._my_ships = list(log.sunk_ships);
        self._my_sunk_ships = list(log.my_sunk_ships);
        self._sunk_ships = list(log.sunk_ships)
        self._turn_no = log.turn_no
        self._my_turn = log.my_turn
        self._state_change()

    def next_state(self):
        assert isinstance(self._state_logger,StateLogger)
        self = self._state_logger.get_next_state()

    def prev_state(self):
        assert isinstance(self._state_logger, StateLogger)
        self = self._state_logger.get_prev_state()

    def set_logger(self,logger):
        self._state_logger = logger

    def _state_change(self):
        self._state_changed = True

    def get_state_change(self):
        tmp = self._state_changed
        self._state_changed = False
        return tmp

    def start_game(self):
        self._state_logger.log_turn(self)
        self._turn_no = 1
        self._state_change()

    def add_my_ship(self, selection):
        lista_pol = []
        for wsp in selection:
            lista_pol.append(PoleStatku(wsp, False))
        new_ship = Statek(lista_pol)
        assert self.is_ship_allowed(new_ship.get_size())
        self._my_ships.append(new_ship)
        self.increment_ship_count(new_ship.get_size())
        self._state_change()

    def sink_my_ship(self, ship):
        self._my_sunk_ships.append(ship)
        self.decrement_ship_count(ship.get_size())

    def del_my_ship(self, ship):
        self.decrement_ship_count(ship.get_size())
        self._my_ships.remove(ship)

    def reset_ship_count(self):
        for key in self._my_ships:
            self._ship_count[key] = 0

    def increment_ship_count(self, key):
        self._ship_count[key] += 1

    def decrement_ship_count(self, key):
        self._ship_count[key] -= 1

    def decrement_enemy_count(self, key):
        self._enemy_count[key] -= 1

    def is_ship_allowed(self, key):
        return self.get_ship_count(key) < 5 - key

    def get_ship_count(self, key):
        return self._ship_count[key]

    def get_enemy_ship_count(self, key):
        return self._enemy_count[key]

    def get_my_ships(self):
        return self._my_ships;

    def get_enemy_ships(self):
        return self._sunk_ships

    def get_sunk_ships(self):
        return self._my_sunk_ships

    def ready_for_battle(self):
        return self._enemy_count == self._ship_count

    def get_turn_no(self):
        return self._turn_no

    def is_my_turn(self):
        return self._my_turn

    def next_turn(self):
        self._state_logger.log_turn(self)
        self._turn_no += 1
        self._my_turn = not self._my_turn
        self._state_change()

    def s_my_turn(self, my_turn):
        self._my_turn = my_turn

    def they_shoot_at_us(self,wsp):
        msg = "Miss"
        for statek in self._my_ships:
            for pole in statek.get_pola():
                assert isinstance(pole,PoleStatku)
                if pole.get_key() == wsp:
                    pole.kill_pole()
                    msg = "Trafiony"
            if statek.is_zatopiony() and not statek in self._my_sunk_ships:
                wspolrzedne = []
                for pole in statek.get_pola():
                    wsp = pole.get_key()
                    c,r = wsp;
                    wspolrzedne.append(",".join([str(c),str(r)]))
                wspolrzedne.insert(0,"Zatopiony")
                msg = " ".join(wspolrzedne)
                self.sink_my_ship(statek)
        self.play_hit_sound(not msg == "Miss")
        self._state_change()
        return msg

    def we_shot_them_down(self,klucze):
        Pola = []
        for klucz in klucze:
            Pola.append(PoleStatku(klucz,True))
        zatopiony = Statek(Pola)
        self._sunk_ships.append(zatopiony)
        self.decrement_enemy_count(zatopiony.get_size())
        self._state_change()

    def play_hit_sound(self,hit):
        self._hit_sound(hit)



