class TagNotFound(Exception):
    def __init__(self, tag):
        self.tag = tag
        message = f"Tag ({tag}) no encontrado, o no existe"
        super().__init__(message)