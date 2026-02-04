import cytoscape from 'cytoscape';
import edgehandles from 'cytoscape-edgehandles';
cytoscape.use(edgehandles);
import { layout, style } from './cy_style_script.js';
import * as graphs from './graphs.js';
import { setText } from './other_functions_script.js'

const container1 = document.getElementById('graph_container1');
const container2 = document.getElementById('graph_container2');

let cy1 = cytoscape({
    container: container1,
    layout: layout,
    style: style,
    wheelSensitivity: 0.1
});
let eh1 = cy1.edgehandles();
let first_graph = null;
let first_graph_list = [];
let first_graph_n = 0;
let first_graph_q_f = [];
let first_graph_q_b = [];


let cy2 = cytoscape({
    container: container2,
    layout: layout,
    style: style,
    wheelSensitivity: 0.1
});
let eh2 = cy2.edgehandles();
let second_graph = null;
let second_graph_list = [];
let second_graph_n = 0;
let second_graph_q_f = [];
let second_graph_q_b = [];

/* 
==================================================================================
                            HELP FUNCTIONS
==================================================================================
*/

function add_edge(addedEdge) 
{
    let input = prompt("Zadej váhu hrany (číslo mezi 1 a 999999 včetně):", "1");
    if (input !== null) {
        let weight = Number(input);

        if (!isNaN(weight) && weight >= 1 && weight <= 999999) {
            addedEdge.data('weight', weight);
        } else {
            alert("To není platné číslo!");
            addedEdge.remove();
        }
    }
    else {
        addedEdge.remove();
    }
}

cy1.on('ehcomplete', (event, sourceNode, targetNode, addedEdge) => add_edge(addedEdge));
cy2.on('ehcomplete', (event, sourceNode, targetNode, addedEdge) => add_edge(addedEdge));

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

function remove_from_selected_vertexes(cy)
{
    cy.forEach(v => {
        if (v.id() === '0' || v.id() === '-1') alert("Nelze odstranit počáteční/koncový vrchol");
        else {
            v.remove();
        }
    });
}

function remove_from_selected_edges(cy)
{
    cy.forEach(e => {
        e.remove();
    });
}

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

function clean_data(cy)
{
    let nodes = cy.nodes().map(node => {
        return {
            id: node.id(),
        }
    });
    let edges = cy.edges().map(edge => {
        return {
            id: edge.data('id'),
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

function createGraph(cy, elements) 
{ 
    let nodes = JSON.parse(elements.nodes);
    let edges = JSON.parse(elements.edges);
    
    cy.remove(cy.elements());
    cy.add(nodes);
    cy.add(edges);
    cy.layout(layout).run();
    cy.fit();
    
    update_queues();
}

function toUper(num) {
    const uper = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
    };
    return num.toString().split('').map(char => uper[char] || char).join('');
}

function queue_to_text(Q)
{
    let text = "";
    if (Q) {
        Q.queue.sort((x, y) => x[0] - y[0]).forEach(tuple => {
            let [priority, id] = tuple;
            let label = id.toString();
            if (id == -1) label = 'S';
            if (id == 0) label = 'T';
            let priorityTxt = toUper(priority);
            text += label + priorityTxt + "   "
        });
    }
    return text
}

function update_queues()
{
    setText('Qf1_text', queue_to_text(first_graph_q_f[first_graph_n]));
    setText('Qb1_text', queue_to_text(first_graph_q_b[first_graph_n]));

    setText('Qf2_text', queue_to_text(second_graph_q_f[second_graph_n]));
    setText('Qb2_text', queue_to_text(second_graph_q_b[second_graph_n]));
}

function reset_graphs()
{
    first_graph_list = [];
    first_graph_q_f = [];
    first_graph_q_b = [];
    first_graph_n = 0;

    second_graph_list = [];
    second_graph_q_f = [];
    second_graph_q_b = [];
    second_graph_n = 0;
}

function update_graph(cy, elements, animate)
{
    let nodes = JSON.parse(elements.nodes);
    let edges = JSON.parse(elements.edges);
    
    nodes.forEach(node => {
        let changed_node = cy.$('#' + node.data.id);
        let new_data = changed_node.data();
        let old_data = node.data
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
    update_queues();
}

/*
==================================================================================
                            EXPORT FUNCTIONS
==================================================================================
*/ 

export function graphs_init() {
    cy1.add(JSON.parse(JSON.stringify(graphs.basic_graph)));
    cy1.layout(layout).run();
    cy1.fit();
    cy2.add(JSON.parse(JSON.stringify(graphs.basic_graph)));
    cy2.layout(layout).run();
    cy2.fit();
}

export function enableVertexAdding()
{
    cy1.on('tap', add_vertex);
    cy2.on('tap', add_vertex);
}

export function disableVertexAdding()
{
    cy1.off('tap', add_vertex);
    cy2.off('tap', add_vertex);
}

export function remove_vertex() 
{
    let selected_vertex1 = cy1.$('node:selected');
    if (selected_vertex1) remove_from_selected_vertexes(selected_vertex1);

    let selected_vertex2 = cy2.$('node:selected');
    if (selected_vertex2) remove_from_selected_vertexes(selected_vertex2);
}

export function remove_edge()
{
    let selected_edge1 = cy1.$('edge:selected');
    if (selected_edge1) remove_from_selected_edges(selected_edge1);

    let selected_edge2 = cy2.$('edge:selected');
    if (selected_edge2) remove_from_selected_edges(selected_edge2);
}

export function reset() {
    setText('Qf1_text', "");
    setText('Qb1_text', "");
    cy1.remove(cy1.elements());
    cy1.add(first_graph);
    cy1.fit();

    setText('Qf2_text', "");
    setText('Qb2_text', "");
    cy2.remove(cy2.elements());
    cy2.add(second_graph);
    cy2.fit();
    reset_graphs();
}

export function enableEdgeAdding() {
    eh1.enableDrawMode();
    eh2.enableDrawMode();
}

export function disableEdgeAdding() {
    eh1.disableDrawMode();
    eh2.disableDrawMode();
}

export function getcy1Elements() {
    return clean_data(cy1);
}

export function getcy2Elements() {
    return clean_data(cy2);
}

export function calculate(json)
{
    first_graph = cy1.elements().clone();
    second_graph = cy2.elements().clone();

    let result = window.run(json);
    const data = JSON.parse(result);

    const first_part = data.part_one;
    const first_steps = JSON.parse(first_part.steps);
    const first_graph_data = first_steps.data;

    const second_part = data.part_two;
    const second_steps = JSON.parse(second_part.steps);
    const second_graph_data = second_steps.data;

    first_graph_data.forEach(e => {
        let data = JSON.parse(e);
        let graph = JSON.parse(data.graph);
        let queue_f = JSON.parse(data.queue_f);
        let queue_b = JSON.parse(data.queue_b);
        let mu = JSON.parse(data.mu);
        
        let elements = graph.elements;
        first_graph_list.push(elements)
        first_graph_q_f.push(queue_f);
        first_graph_q_b.push(queue_b);
    });
    update_graph(cy1, first_graph_list[first_graph_n], false);

    second_graph_data.forEach(e => {
        let data = JSON.parse(e);
        let graph = JSON.parse(data.graph);
        let queue_f = JSON.parse(data.queue_f);
        let queue_b = JSON.parse(data.queue_b);
        let mu = JSON.parse(data.mu);
        
        let elements = graph.elements;
        second_graph_list.push(elements)
        second_graph_q_f.push(queue_f);
        second_graph_q_b.push(queue_b);
    });
    update_graph(cy2, second_graph_list[second_graph_n], false);
}

export function move(next)
{
    if (next) {
        try {
            const first_done = first_graph_n + 1 == first_graph_list.length;
            const second_done = second_graph_n + 1 == second_graph_list.length;

            if (first_done && second_done) {
                throw "End of both algorithms"
            };
            if (!first_done) {
                first_graph_n++;
                update_graph(cy1, first_graph_list[first_graph_n], true);
            }
            if (!second_done) {
                second_graph_n++;
                update_graph(cy2, second_graph_list[second_graph_n], true);
            }
            update_queues();
        } catch (error) {
            alert(error)
        }
    } 
    else {
        try {
            const first_start = first_graph_n == 0;
            const second_start = second_graph_n == 0;
            if (first_start && second_start) throw "At the start of both algorithms";
            if (!first_start && first_graph_n >= second_graph_n) {
                first_graph_n--;
                update_graph(cy1, first_graph_list[first_graph_n], false);
            }
            if (!second_start && second_graph_n >= first_graph_n + 1) {
                second_graph_n--;
                update_graph(cy2, second_graph_list[second_graph_n], false);
            }
            update_queues();
        } catch (error) {
            alert(error)
        }
    }
}
