__author__ = "104-pianist"
__copyright__ = ""
__credits__ = ["104-pianist", "https://github.com/104-pianist/GraphAlgorithms/blob/main/shortest_path/dijkstra.py"]
__license__ = ""
__version__ = "1.0"
__maintainer__ = "Chauvin Antoine"
__email__ = "antoine.chauvin@live.fr"
__status__ = "Production"
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict


class Dijkstra:
    def __init__(self, nodes, edges) -> None:
        self.nodes = nodes
        self.edges = edges

    def shortest_path(self, start_node):
        num_node = len(self.nodes)
        parent = [None] * num_node  # Initialisation des parents à 0 pour le nombre de points
        distance = [None] * num_node  # Initialisation des distances à 0 pour le nombre de points
        edge_weight = defaultdict(lambda: None)  # Initialisation des poids à 0
        node_neighbors = defaultdict(set)  # Initialisation du dictionnaire contenant les voisins


        for (node1, node2, cost) in self.edges:
            #On ajoute le poids de chacun des liens
            edge_weight[(node1, node2)] = cost
            # On ajoute le lien dans un dictionnaire
            node_neighbors[node1].add(node2)

        # On met la distance du point d'entrée à 0
        distance[start_node] = 0

        # Pour chacun voisin provenant du point de départ
        for neighbor in node_neighbors[start_node]:
            # On met pour chaque voisin le point de départ comme parent
            parent[neighbor] = start_node
            # On met ensuite la distance entre le point de départ et son voisin
            distance[neighbor] = edge_weight[(start_node, neighbor)]
        not_visit = [node for node in range(num_node) if node != start_node]  # On met à jour les noeuds pas encore visité

        # Tant qu'on a pas visité tout les points
        while len(not_visit):
            min_w_node = not_visit[0]  # On choisis le premier point

            for node in not_visit:
                if distance[node] == None:
                    continue
                # On calcule le point possédant le poids le plus faible
                elif distance[node] < distance[min_w_node]:
                    min_w_node = node
            not_visit.remove(min_w_node)

            # On met à jour la distance la plus courte et le chemin le plus court
            for node in not_visit:
                if edge_weight[(min_w_node, node)] == None:
                    continue
                elif distance[node] == None or distance[min_w_node] + edge_weight[(min_w_node, node)] < distance[node]:
                    distance[node] = distance[min_w_node] + edge_weight[(min_w_node, node)]
                    parent[node] = min_w_node
        return parent, distance


def get_nodes_edges(parent, end_node):
    nodes, edges = [], []
    v = end_node
    nodes.append(v)

    # Tant qu'on est pas arrivé au dernier point
    while parent[end_node] != None:
        # On définis le parent du dernier point
        parent_node = parent[end_node]
        nodes.append(parent_node)
        edges.append((parent_node, v))
        end_node = parent_node
        v = parent_node

    # On inverse les liste afin d'avoir les points et les chemin dans l'ordre
    return nodes[::-1], edges[::-1]


def draw(DG, color_nodes, color_edges):
    edges = list(DG.edges)  # Créer les liens du graphique
    num_nodes = DG.number_of_nodes()  # Nombre de points sur le graphique
    num_edges = DG.number_of_edges()  # On ajoute les liens sur le graphique
    node_color = ['b'] * num_nodes  # On définis la couleur des points
    edge_color = ['b'] * num_edges  # On définis la couleur des liens

    # On change la couleur des points utlisés
    for node in color_nodes:
        node_color[node] = 'r'

    # On change la couleur des points utlisés
    for link in range(num_edges):
        node_from, node_to = edges[link][0], edges[link][1]

        # Si le lien se trouve dans la liste des liens de l'algorithme
        if (node_from, node_to) in set(color_edges):
            # Alors on lui définis une couleur différente
            edge_color[link] = 'r'

    # https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spiral_layout.html
    pos = nx.circular_layout(DG)

    # On définis un titre
    plt.title('Algorithme de Dijkstra')

    nx.draw(DG, pos, with_labels=True, node_color=node_color, edge_color=edge_color)  # On affiche les liens et les points
    edge_labels = nx.get_edge_attributes(DG, 'weight')
    nx.draw_networkx_edge_labels(DG, pos, edge_labels=edge_labels)  #On affiche les poids du graphique

    # On sauvegarde la figure puis on se contente de l'afficher
    plt.savefig('dijkstra.png', format='PNG')
    plt.show()


def main():
    # Liste des points
    nodes = [0, 1, 2, 3, 4, 5, 6]

    # (node1, node2, cost)
    edges = [(0, 1, 1),
             (0, 2, 12),
             (1, 2, 9),
             (1, 3, 3),
             (2, 4, 5),
             (2, 3, 4),
             (3, 4, 13),
             (3, 5, 15),
             (4, 5, 4)]

    start_node = 0  # On définis le point de départ

    parent, distance = Dijkstra(nodes, edges).shortest_path(start_node)
    # Parent contient la liste des points les plus court(chaque point provient de ...)
    # Distance contient les poids les plus faibles
    #POINT 1  POINT2   POINT 3  POINT 4   POINT 5   POINT 6
    #[1      ,20      , 25      , 15      , 12      , 11]

    for i in range(len(nodes)):
        if start_node != nodes[i]:
            print('{}->{}: Liens:{} | Coût:{}'.format(start_node, nodes[i], get_nodes_edges(parent, nodes[i]), distance[nodes[i]]))

    pass_nodes, pass_edges = get_nodes_edges(parent, end_node=4)

    DG = nx.DiGraph()
    DG.add_nodes_from(nodes)
    DG.add_weighted_edges_from(edges)
    draw(DG, pass_nodes, pass_edges)


if __name__ == '__main__':
    main()
