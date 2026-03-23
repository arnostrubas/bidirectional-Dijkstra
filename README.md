# Bidirectional Dijkstra visualisation

This is a README for a web app that is part my bachelor thesis.

The web app is for visualising the different versions of a bidirectional Dijkstra algorithm.

If you encounter any errors during the usage of the app or you have any ideas for improving the app, reach out to me via email: arnost.rubas@gmail.com

## Web app screenshot
![screenshot of the app](/figures/app_screenshot.png)

## Sections description
## 1 - Graphs

Main section in which two graphs are shown. Each graph is separete, change in one graph won't affect the other. You can rearange the vertexes by dragging them around the container. 

When you right click the vertex, small pop-up window with vertex data shows up. The pop-up window looks like this:

![vertex pop-up window](/figures/pop-up.png)

You can see all the atributes of the vertex. Note, that when the visualisation isn't running, these values have no real meaning. There are also two buttons, `Set as START` and `Set as TARGET`. These buttons allow you to change the START and TARGET vertex. You can only do this before the start of the visualisation, when the visualisation is running, these buttons are disabled.

The color of the vertex indicates the state of the vertex (so you dont have to view the pop-up window every time you want to see the state). Left side of the vertex indicates the vertex state in forward search, right side in the backward search.
#### Color meaning
`Gray` - UNVISITED \
`Yellow` - OPEN in forward search \
`Red` - CLOSED in forward search \
`Light blue` - OPEN in backward search \
`Blue` - CLOSED in backward search \
`Green` - Showed only at the end of the algorithm, highlights the shortest path

### 2 - Queues
Two sets of priority queues, two priority queues for each graph. The elements in this queue are the vertex labels. Each element has and upper index, which indicates the priority of the vertex.

### 3 - Explanation of last step
Text field, in which the last step is shortly explained. Sometimes the format of the explanation can be a bit complicated, in that case the format is explained above the container (after the Step explanation label). When the shortest path is found, the lenght of this path is shown here.

### 4 - Visualisation buttons
Main buttons used for visualisation. \
`START` button inicialises the visualisation. Calculates the steps and enables showing them. Also disables some buttons/selects/checkboxes, which shouldn't work during visualisation (for example you cannot remove a vertex during the visualisation).\
`RESET` button stops the visualisation, which can be stopped at any point. After reset, the visualisation is lost (and then calculated at the next START press).
`Previous step` and `Next step` buttons allows user to view the steps of the visualisation 
`Select number of steps` in default shows visualisation after each step, but when Show only shortest path option is selected, the next step button shows the last step of the algorithm (shortest path if it has been found), the previous step button shows the first step of the algorithm (inicialisation).

### 5 - Search and End strategy selectors
### 6 - Additional buttons
### 7 - Checkboxes for vertex/edge adding/removing



5 - buttons and checkboxex that allow user to change the graph

    allowed only before starting the calculation

    checkbox add to both graphs - !!!NOT IMPLEMENTED!!!!

    Vertex adding - when checked, user can click at a free space inside the graph and new vertex will be generated

    Edge adding - when checked, user can add edges from two nodes by holding from a source vertex and the draging to end node

    when either of these two is selected, moving the graph/nodes around may not work

    Delete selected vertex - when user selects a node (by clicking on it and it being highligted in blue) he can remove this node (and all edges leading from/to this node) by clicking this button

    Delete selected edge - similar to vertex deleting

    python ready - since the webapp uses python for calculations, it is necessary to wait for the python script to load. Turns green when python is succesfully loaded. Start is enabled after python is loaded

