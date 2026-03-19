# Start Graph
Screenshot of the graph:

![Picture of graph](/figures/start_graph.jpg)

This is a "basic" graph that is shown when loading the application. 

### What to look for
Every single version of bidirectional Dijkstra algorithm explores less vertexes and terminates sooner than the normal Dijkstra algorithm. 

Search strategy `after one edge` is a bit more efficient (in terms of explored vertexes and number of steps before termination) than strategy `after one vertex`.

Search strategy `less open vertexes` explores less vertexes than any other strategy.

Ending strategy `first encounter` works in this case.