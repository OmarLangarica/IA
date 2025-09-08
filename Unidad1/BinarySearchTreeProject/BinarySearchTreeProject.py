class Nodo:
    # Este es el constructor del nodo del árbol
    def __init__(self, dato):  
        self.izquierda = None
        self.derecha = None
        self.dato = dato

    # Método para insertar un nuevo valor en el árbol
    def insert(self, dato):
        if dato < self.dato:  # Si el dato a ingresar es menor que el nodo actual
            if self.izquierda is None:  # Si no hay subárbol izquierdo
                self.izquierda = Nodo(dato)  # Se crea un nuevo nodo a la izquierda
            else:
                self.izquierda.insert(dato)  # Se llama recursivamente al subárbol izquierdo
        elif dato > self.dato:  # Si el dato a ingresar es mayor que el nodo actual
            if self.derecha is None:  # Si no hay subárbol derecho
                self.derecha = Nodo(dato)  # Se crea un nuevo nodo a la derecha
            else:
                self.derecha.insert(dato)  # Se llama recursivamente al subárbol derecho

    # Método para imprimir el árbol in-order
    def printTree(self): 
        if self.izquierda is not None:  # Si hay subárbol izquierdo
            self.izquierda.printTree()  # Llamamos recursivamente al subárbol izquierdo
        print(self.dato, end=' ')  # Imprimimos el valor del nodo actual               
        if self.derecha is not None:  # Si hay subárbol derecho
            self.derecha.printTree()  # Llamamos recursivamente al subárbol derecho


# Ejemplo de uso
arbol = Nodo(10)
arbol.insert(6)   
arbol.insert(4)
arbol.insert(0)
arbol.insert(8)
arbol.insert(16)

arbol.printTree()
