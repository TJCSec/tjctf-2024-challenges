import re
import dataclasses
import functools
import time
import pygtrie
from collections import deque
from pyrage import passphrase


@dataclasses.dataclass(eq=True, frozen=True)
class Node:
    letter: str
    id: int


@dataclasses.dataclass(eq=True, frozen=True)
class Edge:
    a: Node
    b: Node


@dataclasses.dataclass
class Graph:
    nodes: list[Node]
    edges: list[Edge]


class PathChecker:
    def __init__(self, words):
        self.trie = pygtrie.CharTrie()
        for word in words:
            self.trie[word] = True

    @functools.lru_cache
    def check_path(self, path):
        for i in range(1, len(path) + 1):
            sofar = path[:i]
            if self.trie.has_key(sofar):
                if self.check_path(path[i:]):
                    return True
            if not self.trie.has_subtrie(sofar):
                return False
        return True


def build_graph():
    data = open("hint.txt").read()
    nodedata = re.findall(r"(\d+) \[(\w)\];", data)
    edgedata = re.findall(r"(\d+) -- (\d+);", data)
    nodes = [Node(x[1], int(x[0])) for x in nodedata]
    edges = []
    for a, b in edgedata:
        n_a = [node for node in nodes if node.id == int(a)][0]
        n_b = [node for node in nodes if node.id == int(b)][0]
        edges.append(Edge(n_b, n_a))
    return Graph(nodes, edges)


def get_word_list(letters):
    with open("amontillado.txt") as f:
        text = f.read()
    wordlst = list(set(re.sub("[^a-z]", " ", text.lower()).split()))
    return [
        word
        for word in wordlst
        if all(letters.count(ch) >= word.count(ch) for ch in word)
    ]


def print_info(iters, starttime, r=False):
    if not iters % 100 or r:
        print(
            f"Time: {time.time() - starttime:.5g}s    Iterations: {iters}      ",
            end="\r" if not r else "\n",
        )


def find_hamiltonians(graph: Graph):
    edge_lookup = {node: set() for node in graph.nodes}
    for edge in graph.edges:
        edge_lookup[edge.a].add(edge.b)

    pc = PathChecker(get_word_list([node.letter for node in graph.nodes]))
    flagdata = open("secret.txt", "rb").read()

    iters = 0
    starttime = time.time()

    queue = deque()
    for node in graph.nodes:
        if pc.check_path(f"{node.letter}"):
            queue.append((node, {node}, f"{node.letter}"))

    while queue:
        node, seen, path = queue.pop()
        if len(path) == len(graph.nodes):
            print(path + (" " * 50) + "\n")

            try:
                data = passphrase.decrypt(flagdata, path)
                print(data)
                break
            except:
                continue

        for othernode in edge_lookup[node] - seen:
            if pc.check_path(path + othernode.letter):
                queue.append((othernode, seen | {othernode}, path + othernode.letter))

        iters += 1
        print_info(iters, starttime)
    print_info(iters, starttime, True)


def main():
    graph = build_graph()
    find_hamiltonians(graph)


if __name__ == "__main__":
    main()
