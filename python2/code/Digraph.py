"""

Code example from _Computational_Modeling_
http://greenteapress.com/compmod

Copyright 2008 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.

"""

class Digraph(Graph):
    """a Digraph is a directed Graph."""

    def __repr__(self):
        return "DiGraph(%s, %s)" % (repr(self.vertices()), 
                                    repr(self.edges()))

    __str__ = __repr__


    def add_edge(self, e):
        """add (e) to the graph.

        If there is already an edge connecting these Vertices, the
        new edge replaces it.
        """
        v, w = e
        self[v][w] = e

    def remove_edge(self, e):
        """remove (e) from the graph"""
        v, w = e
        del self[v][w]

    def in_vertices(self, v):
        """return the list of vertices that can reach v in one hop"""
        return [d[v][0] for d in self.itervalues() if v in d]

    def in_edges(self, v):
        """return the list of edges into v"""
        return [d[v] for d in self.itervalues() if v in d]


def main(script, *args):

    vs = [SingleVertex(c) for c in 'abc']
    g = Digraph(vs)



if __name__ == '__main__':
    import sys
    main(*sys.argv)

