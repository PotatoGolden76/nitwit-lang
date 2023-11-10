class ProgramInternalForm:
    def __init__(self):
        self.data = []

    def __str__(self):
        s = ""
        for p in self.data:
            s += f"{p[0]} \t\t\t {p[1]}\n"
        return s

    def add(self, identifier, constant):
        self.data.append((identifier, constant))
