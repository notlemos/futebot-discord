class ShortCuts:
    def __init__(self, jogos):
        self.jogos = jogos
    def mandante(self):
        return self.jogos[2]
    def visitante(self):
        return self.jogos[3]
    def golVisitante(self):
        return self.jogos[4]
    def golMandante(self):
        return self.jogos[5]