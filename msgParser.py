class Parser:
    def __init__(self):
        pass

    def parse(self, data):
        wsp = {}
        lista = data.split(" ")
        if len(lista) > 3 and lista[0] in ('strzel', 'rusz'):
            for el in lista[1:4]:
                try:
                    if int(el) > 0 and int(el) < 11:
                        wsp['x'] = int(el) - 1
                except ValueError:
                    pass
                try:
                    if (el.upper() >= 'A' and el.upper() <= 'J'):
                        wsp['y'] = ord(el.upper()) - ord('A')
                    elif (el.upper() >= 'Q' and el.upper() <= 'Z'):
                        wsp['z'] = ord(el.upper()) - ord('Q')
                except TypeError:
                    pass
        return wsp;
