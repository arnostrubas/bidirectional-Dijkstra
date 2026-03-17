import cytoscape from 'https://esm.sh/cytoscape@3.28.1';
import edgehandles from 'https://esm.sh/cytoscape-edgehandles@4.0.1';
cytoscape.use(edgehandles);
import popper from 'https://esm.sh/cytoscape-popper@2.0.0';
cytoscape.use(popper);
import { show_popper } from './popper_script.js';
import { layout, style } from './cy_style_script.js';
import { reset_text_containers, update_text_containers } from './queue_text_script.js'
import { set_graph_select_to_default } from './buttons_script.js'
import * as data_func from './cytoscape_data_script.js'

const container1 = document.getElementById('graph_container1');
const container2 = document.getElementById('graph_container2');

let running_visualisation = false;

let cy_left = cytoscape({
    container: container1,
    layout: layout,
    style: style,
    wheelSensitivity: 0.3,
    minZoom: 0.3,
    maxZoom: 3.0,
});
let eh_left = cy_left.edgehandles();
cy_left.on('ehcomplete', (event, sourceNode, targetNode, addedEdge) => add_edge(addedEdge, cy_left));
cy_left.on('add remove', (event) => set_graph_select_to_default(false));
cy_left.on('cxttap', 'node', (event) => show_popper(event, cy_left, running_visualisation));
// Lists where graph, queue and steps explanation data are stored + current position in these lists
let left_list = [];
let left_n = 0;
let left_q_f = [];
let left_q_b = [];
let left_text = [];

let cy_right = cytoscape({
    container: container2,
    layout: layout,
    style: style,
    wheelSensitivity: 0.3,
    minZoom: 0.3,
    maxZoom: 3.0,
});
let eh_right = cy_right.edgehandles();
cy_right.on('ehcomplete', (event, sourceNode, targetNode, addedEdge) => add_edge(addedEdge, cy_right));
cy_right.on('add remove', (event) => set_graph_select_to_default(true));
cy_right.on('cxttap', 'node', (event) => show_popper(event, cy_right, running_visualisation));
// Lists where graph, queue and steps explanation data are stored + current position in these lists
let right_list = [];
let right_n = 0;
let right_q_f = [];
let right_q_b = [];
let right_text = [];

/* 
==================================================================================
                            HELP FUNCTIONS
==================================================================================
*/

/**
 * Finds lowest positive number that can be used as vertex id
 * @param {cytoscape.Core} cy - cytoscape for which the new id is to be found
 * @returns {int} - lowest positive number that isnt used as vertex id
 */
function find_new_vertex_id(cy) 
{
    const sortedVertexes = cy.nodes().sort((a, b) => {
        return a.id().localeCompare(b.id(), undefined, {numeric: true, sensitivity: 'base'});
    });
    let new_index = -1;
    sortedVertexes.forEach(v => {
        if (v.id() != new_index) return new_index;
        new_index++;
    });
    return new_index;
}

/**
 * Unselects all selected nodes and edges
 */
function unselect()
{
    cy_left.nodes().unselect();
    cy_right.nodes().unselect();
    cy_left.edges().unselect();
    cy_right.edges().unselect();
}

/**
 * Extends edgehandles. Adds weight (inputed by user) to {@link addedEdge}. Prevents multigraph creation
 * @param {cytoscape.EdgeSingular} addedEdge - edge added by edgehandles
 * @param {cytoscape.Core} cy - cytoscape in which the edge was added
 */
function add_edge(addedEdge, cy) 
{
    let input = prompt("Zadej váhu hrany (číslo mezi 1 a 1000 včetně):", "1");
    if (input !== null) {
        let weight = Number(input);
        if (!isNaN(weight) && weight >= 1 && weight <= 1000) {
            if (cy.edges(`edge[source = "${addedEdge.source().id()}"][target = "${addedEdge.target().id()}"]`).length > 1) {
                alert("Cannot create a multigraph");
                addedEdge.remove();
            }
            addedEdge.data('weight', weight);
        } else {
            alert("Not a valid number");
            addedEdge.remove();
        }
    }
    else {
        addedEdge.remove();
    }
}

/**
 * Add vertex to cytoscape in which {@link event} (click) occured
 * @param {cytoscape.EventObject} event - click event
 */
function add_vertex(event)
{  
    const cy = event.cy;
    if (event.target === cy) {
        let pos = event.position;
        let new_index = find_new_vertex_id(cy);
        cy.add({
            group: 'nodes',
            data: { 
                id: new_index,
                label: new_index.toString(),
            },
            position: { x: pos.x, y: pos.y }
        });
    }
}

/**
 * Removes vertex selected in {@link cy}
 * @param {cytoscape.Core} cy 
 */
function remove_vertex(cy) 
{
    let selected_vertex = cy.$('node:selected');
    if (selected_vertex) selected_vertex.remove();
}

/**
 * Removes edge selected in {@link cy}
 * @param {cytoscape.Core} cy 
 */
function remove_edge(cy)
{
    let selected_edge = cy.$('edge:selected');
    if (selected_edge) selected_edge.remove();
}

/**
 * Resets graph in {@link cy} and all its lists
 * @param {cytoscape.Core} cy 
 * @param {*} list - graph data list
 * @param {*} q_f - fwd queue list
 * @param {*} q_b - bwd queue list
 * @param {*} text - step expl list
 * @param {*} n - current position in lists
 */
function reset_graph(cy, list, q_f, q_b, text)
{
    cy.nodes().forEach(n => {
        n.data("state_f","UNVISITED");
        n.data("state_b","UNVISITED");
    });
    cy.edges().forEach(e => {
        e.data("state", "");
    });
    list.length = 0;
    q_f.length = 0;
    q_b.length = 0;
    text.length = 0;
}

/**
 * Resets both graphs
 */
function reset_graphs()
{
    reset_graph(cy_left, left_list, left_q_f, left_q_b, left_text);
    reset_graph(cy_right, right_list, right_q_f, right_q_b, right_text);
    left_n = 0;
    right_n = 0;
}

/**
 * Updates {@link cy} graph with data stored in {@link elements}
 * @param {cytoscape.Core} cy - cytoscape to change
 * @param {Object} elements - object containing data as JSON
 * @param {boolean} animate - wheter to animate the updates 
 */
function update_graph(cy, elements, animate)
{
    let nodes = JSON.parse(elements.nodes);
    let edges = JSON.parse(elements.edges);
    
    nodes.forEach(node => {
        let changed_node = cy.$('#' + node.data.id);
        let new_data = changed_node.data();
        let old_data = node.data;
        if (new_data.state_f != old_data.state_f ||
                new_data.state_b != old_data.state_b ||
                new_data.d_f != old_data.d_f ||
                new_data.d_b != old_data.d_b) {
            changed_node.data(node.data);
            if (animate) {
                changed_node.addClass('highlighted');
                
                setTimeout(() => {
                    changed_node.removeClass('highlighted');
                }, 600);
            }
        }
    });
    edges.forEach(edge => {
        let changed_edge = cy.$('#' + edge.data.id);
        if (changed_edge.data.state != edge.data.state) changed_edge.data(edge.data);
    });
}

/**
 * Updates both graphs and all text containers
 * @param {boolean} animate - whether to animate changes made to graph 
 */
function update_graphs_and_texts(animate)
{
    update_graph(cy_left, left_list[left_n], animate);
    update_graph(cy_right, right_list[right_n], animate);
    update_text_containers(left_q_f[left_n], left_q_b[left_n],
                right_q_f[right_n], right_q_b[right_n],
                left_text[left_n], right_text[right_n]);
}
/**
 * Loads data from JSON {@link part} into lists
 * @param {Object} part - object with stored data
 * @param {*} list - will contain graph data
 * @param {*} q_f - will contain fwd queue data
 * @param {*} q_b - will contain bwd queue data
 * @param {*} text - will contain step expl data
 */
function load_from_py(part, list, q_f, q_b, text)
{
    const steps = JSON.parse(part.steps);
    const graph_data = steps.data;
    
    graph_data.forEach(e => {
        let data = JSON.parse(e);
        let graph = JSON.parse(data.graph);
        let queue_f = JSON.parse(data.queue_f);
        let queue_b = JSON.parse(data.queue_b);
        
        let elements = graph.elements;
        list.push(elements)
        q_f.push(queue_f);
        q_b.push(queue_b);
        text.push(data.text);
    });
}

/*
==================================================================================
                            EXPORT FUNCTIONS
==================================================================================
*/ 

/**
 * Initialises both graphs with starting graph
 */
export function graphs_init() {
    data_func.load_start_graph(cy_left);
    data_func.load_start_graph(cy_right);
}

/**
 * Resets both graphs and all text containers
 */
export function reset() {
    reset_text_containers();
    reset_graphs();
    running_visualisation = false;
}

export function enableVertexAdding()
{
    cy_left.on('tap', add_vertex);
    cy_right.on('tap', add_vertex);
}

export function disableVertexAdding()
{
    cy_left.off('tap', add_vertex);
    cy_right.off('tap', add_vertex);
}

export function enableVertexRemoving()
{
    unselect();
    cy_left.on('select', 'node', _ => remove_vertex(cy_left));
    cy_right.on('select', 'node',  _ => remove_vertex(cy_right));
}

export function disableVertexRemoving()
{
    cy_left.off('select', 'node');
    cy_right.off('select', 'node');
}

export function enableEdgeAdding() {
    eh_left.enableDrawMode();
    eh_right.enableDrawMode();
}

export function disableEdgeAdding() {
    eh_left.disableDrawMode();
    eh_right.disableDrawMode();
}

export function enableEdgeRemoving()
{
    unselect();
    cy_left.on('select', 'edge', _ => remove_edge(cy_left));
    cy_right.on('select', 'edge', _ => remove_edge(cy_right));
}

export function disableEdgeRemoving()
{
    cy_left.off('select', 'edge');
    cy_right.off('select', 'edge');
}

/**
 * Returns data of requested cytoscape
 * @param {boolean} get_cy_right - true for right cytoscape data, false for left cytoscape data
 * @returns cytoscape elements data
 */
export function getcyElements(get_cy_right) {
    if (get_cy_right) return data_func.clean_data(cy_right);
    else return data_func.clean_data(cy_left);
}

/**
 * Runs python script with parameters from {@link json} and loads data returned by it
 * @param {Object} json - json containing data set by user
 */
export function start_visualisation(json)
{
    running_visualisation = true;
    let result = window.run(json);
    const data = JSON.parse(result);

    load_from_py(data.part_one, left_list, left_q_f, left_q_b, left_text, cy_left);
    load_from_py(data.part_two, right_list, right_q_f, right_q_b, right_text, cy_right);

    update_graphs_and_texts(false);
}

/**
 * Shows new step of the algorithm
 * @param {boolean} next - true to show next step of algorithm, false for previous step 
 */
export function move(next)
{
    try {
        if (next) {
            const first_done = left_n + 1 == left_list.length;
            const second_done = right_n + 1 == right_list.length;

            if (first_done && second_done) throw "End of both algorithms";
            if (!first_done) left_n++;
            if (!second_done) right_n++;
        } 
        else {
            const first_start = left_n == 0;
            const second_start = right_n == 0;

            if (first_start && second_start) throw "At the start of both algorithms";
            if (!first_start && left_n >= right_n) left_n--;
            if (!second_start && right_n >= left_n + 1) right_n--;
        }
        update_graphs_and_texts(next); 
    } catch (error) {
        alert(error);
    }
}

/**
 * Version of move function that shows only the final path
 * @param {boolean} final - true to show final path, false to show init step of algortihm 
 */
export function move_final_path_or_start(final)
{
    if (final) {
        left_n = left_list.length - 1;
        right_n = right_list.length - 1;
    } else {
        left_n = 0;
        right_n = 0;
    }
    update_graphs_and_texts(false);
}

/**
 * Copies data from one graph to the other
 * @param {boolean} copy_left_to_right - true to copy FROM left TO right, false to copy FROM right TO left
 */
export function copy(copy_left_to_right) {
    let cy = copy_left_to_right ? cy_right : cy_left;
    let cy_other = copy_left_to_right ? cy_left : cy_right;
    cy.remove(cy.elements());
    cy.add(cy_other.elements());
    cy.fit();
}

/**
 * Fits desired graph into container
 * @param {boolen} fit_right - true to fit right graph, false to copy left graph
 */
export function fit(fit_right) {
    if (fit_right) cy_right.fit(15);
    else cy_left.fit(15);
}

/**
 * Loads premade graph set by {@link graph_to_load}
 * @param {string} graph_to_load - name of thegraph to load 
 * @param {boolen} load_right - true to load into right graph, false to load into left graph
 */
export function load_graph(graph_to_load, load_right) {
    cy_left.off('add remove');
    cy_right.off('add remove');
    
    data_func.load_premade_graph(load_right ? cy_right : cy_left, graph_to_load)
    
    cy_left.on('add remove', (event) => set_graph_select_to_default(false));
    cy_right.on('add remove', (event) => set_graph_select_to_default(true));
}

export function export_image(export_right)
{
    data_func.export_as_jpg(export_right ? cy_right : cy_left);
}

export function export_data(export_right)
{
    data_func.export_as_txt(export_right ? cy_right : cy_left);
}

export function import_data(event, import_right)
{
    data_func.import_txt(event, import_right ? cy_right : cy_left);
}