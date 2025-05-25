class ShortCuts:
    def __init__(self, jogos):
        self.jogos = jogos
    def mandante(self):
        return self.jogos[3]
    def visitante(self):
        return self.jogos[5]
    def golVisitante(self):
        return self.jogos[6]
    def golMandante(self):
        return self.jogos[7]
    def siglaMandante(self):
        return self.jogos[2]
    def siglaVisitante(self):
        return self.jogos[4]