class ErrorMessageConfig:
    def __init__(self, idiom="ENG"):
        self.idiom = idiom
        self.messages = {
            "ENG": {
                "HTTPException-400": "ENG HTTPException-400: The API Key is missing.",
                "HTTPException-403": "ENG HTTPException-403: The API Key supplied is invalid.",
                "HTTPException-429": "ENG HTTPException-429: Rate limit exceeded. Too many requests.",
                "ERR-001": "ENG ERR-001: Access information provided is incorrect.",
                "ERR-002": "ENG ERR-002: User information provided is incorrect.",
                "ERR-003": "ENG ERR-003: Request has no client information."
            },
            "PT-BR": {
                "HTTPException-400": "PT-BR HTTPException-400: A chave API não foi fornecida.",
                "HTTPException-403": "PT-BR HTTPException-403: A chave API fornecida é inválida.",
                "HTTPException-429": "PT-BR HTTPException-429: Limite de acesso excedido. Muitas requisições efetuadas.",
                "ERR-001": "PT-BR ERR-001: Informação de acesso fornecida é incorreta.",
                "ERR-002": "PT-BR ERR-002: Informação de usuário fornecida é incorreta.",
                "ERR-003": "PT-BR ERR-003: Requisição não contem informações do cliente."
            },
            "ESP": {
                "HTTPException-400": "ESP HTTPException-400: Falta la clave API.",
                "HTTPException-403": "ESP HTTPException-403: La clave API proporcionada no es válida.",
                "HTTPException-429": "ESP HTTPException-429: Límite de acceso excedido.",
                "ERR-001": "ESP ERR-001: La información de acceso proporcionada es incorrecta.",
                "ERR-002": "ESP ERR-002: La información del usuario proporcionada es incorrecta.",
                "ERR-003": "ESP ERR-003: La solicitud no tiene información del cliente."
            },
            "LT": {
                "HTTPException-400": "LT HTTPException-400: Trūksta API rakto.",
                "HTTPException-403": "LT HTTPException-403: Pateiktas API raktas neteisingas.",
                "HTTPException-429": "LT HTTPException-504: Viršytas prieigos limitas.",
                "ERR-001": "LT ERR-001: Pateikta prieigos informacija yra neteisinga.",
                "ERR-002": "LT ERR-002: Pateikta vartotojo informacija yra neteisinga.",
                "ERR-003": "LT ERR-003: Prašyme nėra jokios kliento informacijos."
            }
        }

    def get_message(self, code):
        return self.messages[self.idiom].get(code, f"Message code {code} not found.")