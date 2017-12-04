import random
import networkx
import matplotlib.pyplot as plt


def distribution(d):
    s = 0
    lst = []
    for key, val in d.items():
        s += val
        lst.append((key, s))
    r = random.uniform(0, s)
    for key, val in lst:
        if r < val:
            return key
    return key


class Dungeon:

    def __init__(self, num_rooms=None):
        num_rooms = num_rooms or (7, 14)
        if isinstance(num_rooms, (list, tuple)):
            self.num_rooms = random.randint(*num_rooms)
        else:
            self.num_rooms = num_rooms
        self.labels = {}
        self.graph = None
        while not self.fully_connected():
            self.create()

    def create(self):
        self.graph = networkx.Graph()
        self.labels[0] = 'E'
        self.graph.add_node(0)
        for i in range(1, self.num_rooms):
            self.graph.add_node(i)
            self.labels[i] = '{}'.format(i)
        self.edges = set()
        self.secret_edges = set()
        rooms = list(range(self.num_rooms))
        for i in range(self.num_rooms):
            num = distribution({1: 85, 2: 14, 3: 1})
            choices = rooms[:]
            choices.remove(i)
            for j in range(num):
                if not choices:
                    break
                e = random.choice(choices)
                choices.remove(e)
                edge = tuple(sorted([i, e]))
                if edge in self.edges:
                    continue
                self.edges.add(edge)
                if random.uniform(0, 1) < 0.05:
                    print('SECRET {} to {}'.format(*edge))
                    self.secret_edges.add(edge)
                print('connecting {} to {}'.format(*edge))
                self.graph.add_edge(*edge)

    def fully_connected(self):
        if self.graph is None:
            return False
        for i in range(1, self.num_rooms):
            try:
                path = networkx.shortest_path_length(
                    self.graph, source=0, target=i,
                )
            except networkx.NetworkXNoPath:
                print('Graph isnt fully connected! Regenerating.')
                return False
        return True

    def save(self, path='out.png'):
        import networkx
        import matplotlib.pyplot as plt
        pos = networkx.spring_layout(self.graph, iterations=500)
        # pos = networkx.spectral_layout(self.graph)
        # pos = networkx.shell_layout(self.graph)
        # pos = networkx.fruchterman_reingold_layout(self.graph)
        nodelist = list(range(self.num_rooms))
        networkx.draw_networkx_nodes(self.graph, pos, nodelist=nodelist)
        edgelist = sorted(self.edges - self.secret_edges)
        secret = sorted(self.secret_edges)
        networkx.draw_networkx_edges(self.graph, pos, edgelist=edgelist,
                                     edge_color='k')
        networkx.draw_networkx_edges(self.graph, pos, edgelist=secret,
                                     edge_color='r')
        networkx.draw_networkx_labels(self.graph, pos, self.labels)
        plt.savefig(path)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--rooms', '-r', type=int, default=None)
    parser.add_argument('--output', '-o', default='out.png')
    args = parser.parse_args()
    dung = Dungeon(num_rooms=args.rooms)
    dung.save(path=args.output)


if __name__ == '__main__':
    main()
