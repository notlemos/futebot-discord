class ShortCuts:
    def __init__(self, jogos):
        self.jogos = jogos
    def mandante(self):
        return self.jogos["mandante"]
    def visitante(self):
        return self.jogos["visitante"]
    def golVisitante(self):
        return self.jogos["gols_visitante"]
    def golMandante(self):
        return self.jogos["gols_mandante"]
    def siglaMandante(self):
        return self.jogos["sigla_mandante"]
    def siglaVisitante(self):
        return self.jogos["sigla_visitante"]