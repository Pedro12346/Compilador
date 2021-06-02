class QuadManager:
    quads = []
    insertIndex = 0

    operTable ={
        0 : "+",
        1 : "-",
        2 : "*",
        3 : "/",
        4 : "<",
        5 : "<=",
        6 : ">",
        7 : ">=",
        8 : "!=",
        9 : "==",
        10 : "&",
        11 : "|",
        12 : "=",
        13 :"goto",
        14 :"gotof",
        15 :"escribir",
        16 :"leer",
        17 :"verificar",
        18 :"ERA",
        19 :"parameter",
        20 :"gosub",
        21 :"retorno",
        22 :"endfunc",
        23 :"linea",
        24 :"circulo",
        25 :"arco",
        26 :"punto",
        27 :"penDown",
        28 :"penUp",
        29 :"color",
        30 :"grosor",
        31 :"limpiar",
        32 :"ri",
        33 :"rd"
    }

    def add(self, quad):
        self.quads.append(quad)
        self.insertIndex = self.insertIndex + 1

    def print(self):
        pos = 0
        for quad in self.quads:
            print(pos, ". ", "(", self.operTable[quad[0]], ", ", quad[1], ", ", quad[2], ", ", quad[3], ")")
            pos = pos + 1

    def last(self):
        if len(self.quads) == 0:
            print("quad list is empty")
        return self.quads[-1]

    def modify(self, index, pos, value):
        l = list(self.quads[index])
        l[pos] = value
        t = tuple(l)
        self.quads[index] = t

    def next(self):
        return self.insertIndex
