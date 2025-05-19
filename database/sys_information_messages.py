class InformationMessageConfig:
    def __init__(self, idiom="ENG"):
        self.idiom = idiom
        self.messages = {
            "ENG": {
                "message": "message",
                "wait": "Wait",
                "INF-001": "ENG INF-001: Profiles API service.",
                "INF-002": "ENG INF-002: "
            },
            "PT-BR": {
                "message": "mensagem",
                "wait": "Espere",
                "INF-001": "PT-BR INF-001: Serviço API de Perfis.",
                "INF-002": "PT-BR INF-002: "
            },
            "ESP": {
                "message": "mensaje",
                "wait": "Esperar",
                "INF-001": "ESP INF-001: Servicio API de Perfiles.",
                "INF-002": "ESP INF-002: "
            },
            "LT": {
                "message": "žinutę",
                "wait": "Palauk",
                "INF-001": "LT INF-001: Profilių API paslauga.",
                "INF-002": "LT INF-002: "
            }
        }

    def get_message(self, code):
        return self.messages[self.idiom].get(code, f"Message code {code} not found.")