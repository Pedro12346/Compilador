class CuboSemantico:
    #[operador][left_op][right_op]
    cuboSemantico = [
         #left-op        #entero                               #flotante                        #char
                     [["entero", "flotante", "error"], ["flotante", "flotante", "error"], ["error", "error", "error"]], #+
                     [["entero", "flotante", "error"], ["flotante", "flotante", "error"], ["error", "error", "error"]], #-
                     [["entero", "flotante", "error"], ["flotante", "flotante", "error"], ["error", "error", "error"]], #*
                     [["entero", "flotante", "error"], ["flotante", "flotante", "error"], ["error", "error", "error"]],#/
                     [["entero", "entero", "error"], ["entero", "entero", "error"], ["error", "error", "entero"]], #<
                     [["entero", "entero", "error"], ["entero", "entero", "error"], ["error", "error", "entero"]], #<=
                     [["entero", "entero", "error"], ["entero", "entero", "error"], ["error", "error", "entero"]], #>
                     [["entero", "entero", "error"], ["entero", "entero", "error"], ["error", "error", "entero"]], #>=
                     [["entero", "entero", "error"], ["entero", "entero", "error"], ["error", "error", "entero"]], #!=
                     [["entero", "entero", "error"], ["entero", "entero", "error"], ["error", "error", "entero"]], #==
                     [["entero", "entero", "error"], ["entero", "entero", "error"], ["error", "error", "entero"]], #&
                     [["entero", "entero", "error"], ["entero", "entero", "error"], ["error", "error", "entero"]], #|
                     [["entero", "entero", "error"], ["flotante", "flotante", "error"], ["error", "error", "char"]], # =
                     ];

    def getResultType(self, operation, left_op, right_op):
        oper = leftIndex = rightIndex = -1;

        if left_op == "entero":
            leftIndex = 0
        elif left_op == "flotante":
            leftIndex = 1
        else:
            leftIndex = 2

        if right_op == "entero":
            rightIndex = 0
        elif right_op == "flotante":
            rightIndex = 1
        else:
            rightIndex = 2

        if operation == "+":
            oper = 0
        elif operation == "-":
            oper = 1
        elif operation == "*":
            oper = 2
        elif operation == "/":
            oper = 3
        elif operation == "<":
            oper = 4
        elif operation == "<=":
            oper = 5
        elif operation == ">":
            oper = 6
        elif operation == ">=":
            oper = 7
        elif operation == "!=":
            oper = 8
        elif operation == "==":
            oper = 9
        elif operation == "&":
            oper = 10
        elif operation == "|":
            oper = 11
        elif operation == "=":
            oper = 12
        return self.cuboSemantico[oper][leftIndex][rightIndex]
