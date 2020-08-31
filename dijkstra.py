from collections import deque, namedtuple

inf = float('inf')
Arista = namedtuple('Arista', 'inicio, fin, costo')


def crear_arista(inicio, fin, costo=1):
  return Arista(inicio, fin, costo)


class Graph:
    def __init__(self, aristas):
        # let's check that the data is right
        aristas_no = [i for i in aristas if len(i) not in [2, 3]]
        if aristas_no:
            raise ValueError('Wrong edges data: {}'.format(aristas_no))

        self.aristas = [crear_arista(*arista) for arista in aristas]

    @property
    def vertices(self):
        return set(
            sum(
                ([arista.inicio, arista.fin] for arista in self.aristas), []
            )
        )

    def get_parejas(self, n1, n2, ambos=True):
        if ambos:
            parejas = [[n1, n2], [n2, n1]]
        else:
            parejas = [[n1, n2]]
        return parejas

    def quitar_arista(self, n1, n2, ambos=True):
        parejas = self.get_parejas(n1, n2, ambos)
        aristas = self.aristas[:]
        for arista in aristas:
            if [arista.inicio, arista.fin] in parejas:
                self.aristas.remove(arista)

    def agregar_arista(self, n1, n2, costo=1, ambos=True):
        parejas = self.get_parejas(n1, n2, ambos)
        for arista in self.aristas:
            if [arista.inicio, arista.fin] in parejas:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.aristas.append(Arista(inicio=n1, fin=n2, costo=cost))
        if ambos:
            self.aristas.append(Arista(inicio=n2, fin=n1, costo=cost))

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for arista in self.aristas:
            neighbours[arista.inicio].add((arista.fin, arista.costo))

        return neighbours

    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return path

"""
graph = Graph([
    ("a", "b", 7),  ("a", "c", 9),  ("a", "f", 14), ("b", "c", 10),
    ("b", "d", 15), ("c", "d", 11), ("c", "f", 2),  ("d", "e", 6),
    ("e", "f", 9)])

temp = [("h", "f", 4), ("f", "g", 3), ("f", "d", 1), ("f", "b", 2),
    ("d", "i", 6), ("d", "c", 5), ("a","i", 1), ("a", "c", 7),
    ("a", "b", 7), ("d", "e", 1), ("e", "d", 1), ("e", "g", 4)]

temp.append(("c","a",7))
graph = Graph(temp)

print(graph.dijkstra("h", "b"))
"""
    