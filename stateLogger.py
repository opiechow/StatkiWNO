class StateLogger:
    def __init__(self):
        self._stateLog = []
        self._currentIndex = 0
        pass

    def log_turn(self, state):
        self._stateLog.append(state)

    def is_present(self):
        return self._currentIndex == 0

    def get_prev_state(self):
        print self._currentIndex
        print self._stateLog
        self._currentIndex -= 1
        state = self._stateLog[self._currentIndex]
        state.set_logger(self)
        return state

    def get_next_state(self):
        self._currentIndex += 1
        assert self._currentIndex <= 0
        state = self._stateLog[self._currentIndex]
        state.set_logger(self)
        return state