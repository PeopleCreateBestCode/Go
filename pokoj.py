class Pokoj: 
    def __init__(self, id, gra, czarny):
        self.id = id
        self.gra = gra
        self.czarny = czarny  
        self.bialy = None

    def status(self):
        if self.bialy is None:
            return "czeka"
        if self.gra.faza == "gra":
            return "trwa"
        return self.gra.faza

    def kolor_gracza(self, id_gracza):
        if id_gracza == self.czarny["id"]:
            return "czarne"
        if self.bialy is not None and id_gracza == self.bialy["id"]:
            return "biale"
        return None
