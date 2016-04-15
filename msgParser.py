from gameState import GameState


class Parser:
    def __init__(self,game_state):
        self.game_state = game_state;
        pass

    @staticmethod
    def get_shoot_message(sel):
        c,r = sel
        assert c in range(10) and r in range(10)
        msg = " ".join(["Strzel",str(c),str(r)])
        return msg

    def get_moved_message(self):
        return "Ruch"
        pass

    def parse(self,msg):
        print msg
        assert isinstance(self.game_state, GameState)
        words = msg.split(" ")
        if words[0] == "Strzel":
            self.game_state.next_turn()
            wsp = int(words[1]),int(words[2])
            new_msg = self.game_state.they_shoot_at_us(wsp)
            print new_msg
            return new_msg
        elif words[0] == "Ruch":
            self.game_state.next_turn()
        elif words[0] == "Miss":
            self.game_state.play_hit_sound(False)
        elif words[0] == "Trafiony":
            self.game_state.play_hit_sound(True)
        elif words[0] == "Zatopiony":
            self.game_state.play_hit_sound(True)
            lista_wsp = []
            for wsp in words[1:]:
                c,r = wsp.split(",")
                lista_wsp.append((int(c),int(r)))
            self.game_state.we_shot_them_down(lista_wsp)






    # def parse_legacy(self, data):
    #     wsp = {}
    #     lista = data.split(" ")
    #     if len(lista) > 3 and lista[0] in ('strzel', 'rusz'):
    #         for el in lista[1:4]:
    #             try:
    #                 if int(el) > 0 and int(el) < 11:
    #                     wsp['x'] = int(el) - 1
    #             except ValueError:
    #                 pass
    #             try:
    #                 if (el.upper() >= 'A' and el.upper() <= 'J'):
    #                     wsp['y'] = ord(el.upper()) - ord('A')
    #                 elif (el.upper() >= 'Q' and el.upper() <= 'Z'):
    #                     wsp['z'] = ord(el.upper()) - ord('Q')
    #             except TypeError:
    #                 pass
    #     self.main_window_update("strzal_poszedu")
    #     return wsp