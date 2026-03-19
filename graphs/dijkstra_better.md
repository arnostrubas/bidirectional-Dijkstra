# Dijkstra better
Screenshot of the graph:

![Picture of graph](/figures/dijkstra_better.jpg)

This is a graph that shows that bidirectional Dijkstra is not always more efficient (in terms of vertexes explored and number of steps before termination)

### What to look for
`Dijkstra` algorithm is significantly more efficient that any variant of `bidirectional Dijkstra` algorithm. 

Ending strategy `first encounter` does not fins the shortest path in combination with any search strategy

The most efficient search strategy in this case is `less open vertexes`, because it prioritises the forward search more (since branching from TARGET is bigger)