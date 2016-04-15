import xml.dom.minidom as x

class LoggedState:
    def __init__(self, state):
        self.turn_no = state.get_turn_no()
        self.my_turn = state.is_my_turn()
        self.my_ships = tuple(state.get_my_ships())
        self.my_sunk_ships = tuple(state.get_sunk_ships())
        self.sunk_ships = tuple(state.get_enemy_ships())
        self.enemy_count = {}
        for i in range(4):
            self.enemy_count[i+1] = state.get_enemy_ship_count(i+1)
        self.ship_count = {}
        for i in range(4):
            self.ship_count[i+1] = state.get_ship_count(i+1)
        print self.ship_count;
        print self.enemy_count;

class StateLogger:
    def __init__(self):
        self._stateLog = []
        self._currentIndex = 0
        self._maxIndex = 0
        pass

    def log_turn(self, state):
        self._stateLog.append(LoggedState(state))
        print self._stateLog
        self._currentIndex += 1
        self._maxIndex += 1;

    def is_present(self):
        return self._currentIndex == 0

    def get_prev_state(self):
        print self._currentIndex
        print self._stateLog
        self._currentIndex -= 1
        state = self._stateLog[self._currentIndex]
        return state

    def get_next_state(self):
        self._currentIndex += 1
        assert self._currentIndex <= self._maxIndex
        state = self._stateLog[self._currentIndex]
        return state

    def save_logger(self, file):
        doc = x.Document()
        root = doc.createElement("log")
        doc.appendChild(root)
        for logged_state in self._stateLog:
            assert isinstance(logged_state,LoggedState)
            st = doc.createElement("state")
            st.setAttribute("nr",str(logged_state.turn_no))
            root.appendChild(st)
        pass
        f = open(file,'w')
        doc.writexml(f)
        f.close()
