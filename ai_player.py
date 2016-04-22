import msgParser
import random
import statek
from hex import Hex

class AiPlayer:
    def __init__(self):
        self.__state_actions = {"friendly":self._friendly_shoot,"angry":self._angry_shoot,"scared":self._run}
        self._mood = "friendly"
        self.enemy_ships = None
        self.move_message = ""
        self.ship_to_destroy = None
        pass

    def make_cheater(self, shiplist):
        self.enemy_ships = shiplist

    def init_ai_positions(self, shiplist):
        pass

    def _shoot(self,sel):
        self.move_message = msgParser.Parser.get_shoot_message(sel)

    def _friendly_shoot(self):
        # wybor losowego statku
        spotted = random.choice(self.enemy_ships)
        self.ship_to_destroy = spotted;
        #wybor losowego pola
        assert isinstance(spotted,statek.Statek)
        pole = random.choice(spotted.get_pola())
        assert isinstance(pole,statek.PoleStatku)
        wspPole = pole.get_key()
        hexPole = Hex(wspPole[0],wspPole[1])
        sasiedzi = hexPole.get_neighbours()
        # spudluj w sasiada lub traf w pole
        if random.randint(0,100) > 50:
            self._shoot(random.choice(sasiedzi))
        else:
            self._shoot(wspPole)
            self._mood = "angry"

    def _angry_shoot(self):
        s = self.ship_to_destroy
        assert isinstance(s,statek.Statek)
        if s.is_zatopiony():
            self.ship_to_destroy = None
            self._mood = "friendly"
            self.do_action()
        else:
            while True:
                pole_do_ustrzelenia = random.choice(s.get_pola())
                assert isinstance(pole_do_ustrzelenia,statek.PoleStatku)
                if not pole_do_ustrzelenia.is_shot():
                    self._shoot(pole_do_ustrzelenia.get_key())
                    break

    def do_action(self):
        action = self.__state_actions[self._mood]
        action()

    def _angry_shoot(self):
        pass

    def _run(self):
        pass

    def get_move(self):
        pass
