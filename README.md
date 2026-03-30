## License
This project is licensed under the **BSD 3-Clause License**. See the [LICENSE](LICENSE) file for the full license text.

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
Here you can select Search and End strategies to be visualised at each side. If you select `Dijkstra` as one of the strategies, normal Dijkstra algorithm is used. 

### 6 - Additional buttons
Here you can find useful buttons and select. Their function is following: \
`Export image` - Exports the graph as a jpg \
`Export data` - Exports the graph's data as a txt. Useful when u want to save the graph before closing the app and then using it easily again when opening the app again. \
`Import data` - Imports the graph's data, provided as txt. Import only the data that u exported earlier.\
`Fit to container` - Adjusts the graph's position, so it can be seen in the container. Doesnt change vertex positions.
`Copy from left/right` - Allows you to copy graph from one side to another. Useful when you want to compare two different strategies on custom graph, thanks to this you dont have to create the graph twice. Asks for confirmation to prevent accidental click.
`Select premade graph` - Allows you to load a premade graph that showcase some interesting things about the different strategies. Each graph is explained at the link provided (or in folder graphs in this repository).

### 7 - Checkboxes for vertex/edge adding/removing
Vertexes that allow you to change the graph. Each graph is change separetely. If you wanna add to both graphs, either click to both, or use the `Copy` buttons mentioned earlier. There are 4 checkboxes:\
`Add vertex` - allows you to add vertex by clicking at empty space of the container\
`Remove vertex` - allows you to remove vertex by clicking on the vertex you want to remove. All edges comming into/from this vertex are also removed\
`Add edge` - allows you to add edge, by holding and dragging from source vertex to the vertex where the edge should end. You are then asked to set the edge's weight. The action is rejected if you enter wrong weight or if you try to create multigraph.\
`Remove edge` - Allows you to remove edge, by clicking on the edge you want to remove.\



## Acknowledgments / Third-party libraries
This project uses the following open-source libraries:
* [Cytoscape.js](https://js.cytoscape.org/) 
* [NetworkX](https://networkx.org/)
* [PyScript](https://pyscript.net/)
