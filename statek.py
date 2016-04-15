class PoleStatku:
    def __init__(self, wsp, zatopione):
        self._wsp = wsp;
        self._zatopione = zatopione;

    def get_key(self):
        return self._wsp

    def is_shot(self):
        return self._zatopione

    def kill_pole(self):
        self._zatopione = True

class Statek:
    def __init__(self, pola):
        self._pola = pola;
        self._rozmiar = len(pola)
        names = {1:"OW CIENIAS",2:"OW LEPSZY",3:"OW AS",4:"OW WYBRANIEC"}
        self._name = names[self._rozmiar]

    def get_pola(self):
        return list(self._pola)

    def get_size(self):
        return self._rozmiar

    def shout(self):
        print ":".join([self._name," We got them fields covered, commander."])

    def is_zatopiony(self):
        zatopiony = True
        for pole in self.get_pola():
            assert isinstance(pole,PoleStatku)
            if not pole.is_shot():
                zatopiony = False
        return zatopiony
