"""

Code example from _Computational_Modeling_
http://greenteapress.com/compmod

Copyright 2008 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.

"""

class Vertex(object):
    """a Vertex is a node in a graph."""

    def __init__(self, label=''):
        self.label = label

    def __repr__(self):
        """return a string representation of this object that can
        be evaluated as a Python expression"""
        return 'Vertex(%s)' % repr(self.label)

    __str__ = __repr__
    """the str and repr forms of this object are the same"""


class Edge(tuple):
    """an Edge is a list of two vertices"""

    def __new__(cls, *vs):
        """the Edge constructor takes two vertices as parameters"""
        if len(vs) != 2:
            raise ValueError, 'Edges must connect exactly two vertices.'
        return tuple.__new__(cls, vs)

    def __repr__(self):
        """return a string representation of this object that can
        be evaluated as a Python expression"""
        return 'Edge(%s, %s)' % (repr(self[0]), repr(self[1]))

    __str__ = __repr__
    """the str and repr forms of this object are the same"""


class Graph(dict):
    """a Graph is a dictionary of dictionaries.  The outer
    dictionary maps from a vertex to an inner dictionary.
    The inner dictionary maps from other vertices to edges.
    
    For vertices a and b, graph[a][b] maps
    to the edge that connects a->b, if it exists."""

    def __init__(self, vs=[], es=[]):
        """create a new graph.  (vs) is a list of vertices;
        (es) is a list of edges."""
        for v in vs:
            self.add_vertex(v)
            
        for e in es:
            self.add_edge(e)

    def add_vertex(self, v):
        """add (v) to the graph"""
        self[v] = {}

    def add_edge(self, e):
        """add (e) to the graph by adding an entry in both directions.

        If there is already an edge connecting these Vertices, the
        new edge replaces it.
        """
        v, w = e
        self[v][w] = e
        self[w][v] = e

def main(script, *args):
    v = Vertex('v')
    print v
    w = Vertex('w')
    print w
    e = Edge(v, w)
    print e
    g = Graph([v,w], [e])
    print g


if __name__ == '__main__':
    import sys
    main(*sys.argv)


