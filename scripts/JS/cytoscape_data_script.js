/**
 * Copyright (c) 2026, Arnošt Rubáš
 * All rights reserved.
 *
 * This source code is licensed under the BSD 3-Clause License.
 * The full text of the license can be found in the LICENSE file 
 * in the root directory of this project.
 */

import * as graphs from './graphs.js';

/*
====================================================================
                    GETTING DATA FROM CY
====================================================================
*/
/**
 * Returns only relevant data (nodes, edges,...) from {@link cy} 
 * @param {cytoscape.Core} cy 
 * @returns relevant data 
 */
export function clean_data(cy)
{
    let nodes = cy.nodes().map(node => {
        return {
            label: node.data('label'),
            id: node.id(),
            x: node.position().x,
            y: node.position().y
        }
    });
    let edges = cy.edges().map(edge => {
        return {
            id: edge.id(),
            source: edge.source().id(),
            target: edge.target().id(),
            weight: edge.data('weight')
        };
    });
    let graph = {
        nodes: nodes,
        edges: edges
    };
    return graph;
}

/*
====================================================================
                    DATA EXPORT AND IMPORT
====================================================================
*/

/**
 * Exports data
 * @param {Object} data - data to be exported
 * @param {string} file_name - name of the export file
 */
function generic_export(data, file_name)
{
    const downloadLink = document.createElement('a');
    downloadLink.href = data;
    downloadLink.download = file_name;

    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

export function export_as_jpg(cy)
{
    let jpgData = cy.jpg({
            full: true,
            quality: 0.9 
    });
    generic_export(jpgData, 'graph_export.jpg');
}

export function export_as_txt(cy)
{
    const jsonString = JSON.stringify(clean_data(cy), null, 4);
    const blob = new Blob([jsonString], {type: 'text/plans'});
    const url = URL.createObjectURL(blob);
    generic_export(url, 'graph_data_export.txt')
}

/**
 * Import selected text file into {@link cy}
 * @param {*} event 
 * @param {cytoscape.Core} cy - cytoscape in which to import data 
 */
export function import_txt(event, cy)
{
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const content = e.target.result;
            const data = JSON.parse(content);
            cy.batch(() => {
                cy.elements().remove(); 

                data.nodes.forEach(n => {
                    cy.add({
                        group: 'nodes',
                        data: { id: n.id, label: n.label },
                        position: { x: n.x, y: n.y }
                    });
                });

                data.edges.forEach(e => {
                    cy.add({
                        group: 'edges',
                        data: { id: e.id, source: e.source, target: e.target, weight: e.weight }
                    });
                });
            });
        };

        reader.readAsText(file);

        event.target.value = '';
    }
}

/*
========================================================================
                    GRAPH LOADING 
========================================================================
*/

/**
 * Loads premade graph into cytoscape container
 * @param {cytoscape.Core} cy - cytoscape in which to load the graph
 * @param {string} graph_to_load - name of the graph to be loaded
 */
export function load_premade_graph(cy, graph_to_load)
{
    let graph = null;
    switch (graph_to_load) {
        case "start_graph":
            graph = JSON.parse(JSON.stringify(graphs.start_graph));
            break; 
        case "first_encounter":
            graph = JSON.parse(JSON.stringify(graphs.first_encounter));
            break;
        case "path":
            graph = JSON.parse(JSON.stringify(graphs.path));
            break;
        case "dijkstra_faster":
            graph = JSON.parse(JSON.stringify(graphs.dijkstra_faster));
            break;
        case "huge_graph":
            graph = JSON.parse(JSON.stringify(graphs.huge_graph));
            break;
        case "empty_graph":
            graph = JSON.parse(JSON.stringify(graphs.empty_graph));
            break;
        case "same_vertex_closed":
            graph = JSON.parse(JSON.stringify(graphs.same_vertex_closed_example));
            break;
        case "less_open_vertexes_example":
            graph = JSON.parse(JSON.stringify(graphs.less_open_vertexes_example));
            break;
        default:
            break;
    }

    if (graph != null) {
        cy.remove(cy.elements());
        cy.add(graph);
        cy.fit(15);
    }
}

/**
 * Loads start graph into {@link cy}
 * @param {cytoscape.Core} cy - cytoscape in which to load the start graph 
 */
export function load_start_graph(cy)
{
    cy.add(JSON.parse(JSON.stringify(graphs.start_graph)));
    cy.fit(15);
}