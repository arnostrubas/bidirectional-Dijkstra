import cytoscape from 'https://esm.sh/cytoscape@3.28.1';
import edgehandles from 'https://esm.sh/cytoscape-edgehandles@4.0.1';
cytoscape.use(edgehandles);
import popper from 'https://esm.sh/cytoscape-popper@2.0.0';
cytoscape.use(popper);
import { layout, style } from './cy_style_script.js';
import * as graphs from './graphs.js';
import { setText, update_text_containers } from './queue_text_script.js'
import { set_graph_select_to_default } from './buttons_script.js'
import { export_as_jpg, export_as_txt, import_txt } from './cytoscape_im-export.js'

const container1 = document.getElementById('graph_container1');
const container2 = document.getElementById('graph_container2');

let running_visualisation = false;

function show_popper(evt, cy)
{
    const getLabel = (id) => {
        if (!id) return '-';
        const n = cy.getElementById(id);
        return n.length > 0 ? n.data('label') : '-';
    };
    const node = evt.target;

    const div = document.createElement('div');
    div.classList.add('popper');
    div.innerHTML = `
        <div style="font-weight: bold; margin-bottom: 5px; border-bottom: 1px solid #ccc;">
            Uzel: ${node.data('label')}
        </div>
        <table style="border-spacing: 10px 2px; margin-left: -10px;">
            <tr>
                <td><strong>d<sub>f</sub>:</strong> ${node.data('d_f') === 999999999 ? '∞' : node.data('d_f')}</td>
                <td><strong>d<sub>b</sub>:</strong> ${node.data('d_b') === 999999999 ? '∞' : node.data('d_b')}</td>
            </tr>
            <tr>
                <td><strong>&pi;<sub>f</sub>:</strong> ${getLabel(node.data('pi_f'))}</td>
                <td><strong>&pi;<sub>b</sub>:</strong> ${getLabel(node.data('pi_b'))}</td>
            </tr>
            <tr>
                <td><strong>s<sub>f</sub>:</strong> ${node.data('state_f')}</td>
                <td><strong>s<sub>b</sub>:</strong> ${node.data('state_b')}</td>
            </tr>
        </table>
        <button class="popper_btn" id="start_change_btn">Nastavit jako START</button>
        <button class="popper_btn" id="target_change_btn">Nastavit jako TARGET</button>
    `;
    document.body.appendChild(div);

    if (running_visualisation || node.data('id') == -1) div.querySelector('#start_change_btn').disabled = true;
    if (running_visualisation || node.data('id') == 0) div.querySelector('#target_change_btn').disabled = true;

    div.querySelector('#start_change_btn').addEventListener('click', () => {
        switch_vertexes(cy, -1, node.data('id'));
        hide(); 
    });
    div.querySelector('#target_change_btn').addEventListener('click', () => {
        switch_vertexes(cy, 0, node.data('id'));
        hide(); 
    });

    const popper = node.popper({
        content: div,
        popper: { placement: 'top' }
    });

    const hide = () => {
        div.remove();
    };

    cy.on('tap pan zoom cxttap add remove data', hide);
    node.on('position', hide);
}

let cy_left = cytoscape({
    container: container1,
    layout: layout,
    style: style,
    wheelSensitivity: 0.1,
    minZoom: 0.3,
    maxZoom: 3.0,
});
let eh1 = cy_left.edgehandles();
cy_left.on('ehcomplete', (event, sourceNode, targetNode, addedEdge) => add_edge(addedEdge, cy_left));
cy_left.on('add remove', (event) => set_graph_select_to_default(false));
cy_left.on('cxttap', 'node', (event) => show_popper(event, cy_left));
let first_graph_list = [];
let first_graph_n = 0;
let first_graph_q_f = [];
let first_graph_q_b = [];
let first_graph_text = [];

let cy_right = cytoscape({
    container: container2,
    layout: layout,
    style: style,
    wheelSensitivity: 0.1,
    minZoom: 0.3,
    maxZoom: 3.0,
});
let eh2 = cy_right.edgehandles();
cy_right.on('ehcomplete', (event, sourceNode, targetNode, addedEdge) => add_edge(addedEdge, cy_right));
cy_right.on('add remove', (event) => set_graph_select_to_default(true));
cy_right.on('cxttap', 'node', (event) => show_popper(event, cy_right));
let second_graph_list = [];
let second_graph_n = 0;
let second_graph_q_f = [];
let second_graph_q_b = [];
let second_graph_text = [];

/* 
==================================================================================
                            HELP FUNCTIONS
==================================================================================
*/

function add_edge(addedEdge, cy) 
{
    let input = prompt("Zadej váhu hrany (číslo mezi 1 a 999999 včetně):", "1");
    if (input !== null) {
        let weight = Number(input);
        if (!isNaN(weight) && weight >= 1 && weight <= 999999) {
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
        if (v.id() === '0' || v.id() === '-1') alert("Cannot remove START/TARGET vertex");
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

function remove_vertex() 
{
    let selected_vertex1 = cy_left.$('node:selected');
    if (selected_vertex1) remove_from_selected_vertexes(selected_vertex1);

    let selected_vertex2 = cy_right.$('node:selected');
    if (selected_vertex2) remove_from_selected_vertexes(selected_vertex2);
}

function remove_edge()
{
    let selected_edge1 = cy_left.$('edge:selected');
    if (selected_edge1) remove_from_selected_edges(selected_edge1);

    let selected_edge2 = cy_right.$('edge:selected');
    if (selected_edge2) remove_from_selected_edges(selected_edge2);
}

function clean_data(cy)
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

function reset_graphs()
{
    cy_left.nodes().forEach(n => {
        n.data("state_f","UNVISITED");
        n.data("state_b","UNVISITED");
    });
    cy_left.edges().forEach(e => {
        e.data("state", "");
    });
    first_graph_list = [];
    first_graph_q_f = [];
    first_graph_q_b = [];
    first_graph_text = [];
    first_graph_n = 0;

    cy_right.nodes().forEach(n => {
        n.data("state_f","UNVISITED");
        n.data("state_b","UNVISITED");
    });
    cy_right.edges().forEach(e => {
        e.data("state", "");
    });
    second_graph_list = [];
    second_graph_q_f = [];
    second_graph_q_b = [];
    second_graph_text = [];
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
}

function unselect()
{
    cy_left.nodes().unselect();
    cy_right.nodes().unselect();
    cy_left.edges().unselect();
    cy_right.edges().unselect();
}

function switch_vertexes(cy, old_id, new_id)
{
    let old_vertex = cy.getElementById(old_id);
    let new_vertex = cy.getElementById(new_id);
    if (old_vertex.length <= 0 || new_vertex.length <= 0) alert("Invalid input/Vertex with that index doesnt exist!")
    else {
        let temp_position = { ...old_vertex.position() };
        old_vertex.position(new_vertex.position());
        new_vertex.position(temp_position);
        cy.edges().forEach(edge => {
            let data = edge.data();
            let changing = false;
            if (edge.source().id() == old_id) {
                data.source = new_id;
                changing = true;
            } else if (edge.source().id() == new_id) {
                data.source = old_id;
                changing = true;
            } 
            if (edge.target().id() == old_id) {
                data.target = new_id;
                changing = true;
            } else if (edge.target().id() == new_id) {
                data.target = old_id;
                changing = true;
            }
            if (changing) {
                cy.remove(edge);
                cy.add( {data: data} );
            }
        });
    }
}

function update_texts()
{
    update_text_containers(first_graph_q_f[first_graph_n], first_graph_q_b[first_graph_n],
                second_graph_q_f[second_graph_n], second_graph_q_b[second_graph_n],
                first_graph_text[first_graph_n], second_graph_text[second_graph_n]);
}

/*
==================================================================================
                            EXPORT FUNCTIONS
==================================================================================
*/ 

export function graphs_init() {
    cy_left.add(JSON.parse(JSON.stringify(graphs.start_graph)));
    cy_left.layout(layout).run();
    cy_left.fit();
    cy_right.add(JSON.parse(JSON.stringify(graphs.start_graph)));
    cy_right.layout(layout).run();
    cy_right.fit();
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
    cy_left.on('select', 'node', remove_vertex);
    cy_right.on('select', 'node', remove_vertex);
}

export function disableVertexRemoving()
{
    cy_left.off('select', 'node', remove_vertex);
    cy_right.off('select', 'node', remove_vertex);
}

export function reset() {
    setText('Qf1_text', "");
    setText('Qb1_text', "");
    setText('Qf2_text', "");
    setText('Qb2_text', "");
    setText('explain_text1', "");
    setText('explain_text2', "");
    reset_graphs();
    running_visualisation = false;
}

export function enableEdgeAdding() {
    eh1.enableDrawMode();
    eh2.enableDrawMode();
}

export function disableEdgeAdding() {
    eh1.disableDrawMode();
    eh2.disableDrawMode();
}

export function enableEdgeRemoving()
{
    unselect();
    cy_left.on('select', 'edge', remove_edge);
    cy_right.on('select', 'edge', remove_edge);
}

export function disableEdgeRemoving()
{
    cy_left.off('select', 'edge', remove_edge);
    cy_right.off('select', 'edge', remove_edge);
}

export function getcyElements(getcy1) {
    if (getcy1) return clean_data(cy_left);
    else return clean_data(cy_right);
}

export function calculate(json)
{
    running_visualisation = true;
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
        
        let elements = graph.elements;
        first_graph_list.push(elements)
        first_graph_q_f.push(queue_f);
        first_graph_q_b.push(queue_b);
        first_graph_text.push(data.text);
    });
    update_graph(cy_left, first_graph_list[first_graph_n], false);

    second_graph_data.forEach(e => {
        let data = JSON.parse(e);
        let graph = JSON.parse(data.graph);
        let queue_f = JSON.parse(data.queue_f);
        let queue_b = JSON.parse(data.queue_b);
        
        let elements = graph.elements;
        second_graph_list.push(elements)
        second_graph_q_f.push(queue_f);
        second_graph_q_b.push(queue_b);
        second_graph_text.push(data.text);
    });
    update_graph(cy_right, second_graph_list[second_graph_n], false);

    update_texts();
}

export function final_path_or_start(final)
{
    if (final) {
        first_graph_n = first_graph_list.length - 1;
        second_graph_n = second_graph_list.length - 1;
        update_graph(cy_left, first_graph_list[first_graph_n], false);
        update_graph(cy_right, second_graph_list[second_graph_n], false);
        update_texts();
    } else {
        first_graph_n = 0;
        second_graph_n = 0;
        update_graph(cy_left, first_graph_list[first_graph_n], false);
        update_graph(cy_right, second_graph_list[second_graph_n], false);
        update_texts();
    }
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
                update_graph(cy_left, first_graph_list[first_graph_n], true);
            }
            if (!second_done) {
                second_graph_n++;
                update_graph(cy_right, second_graph_list[second_graph_n], true);
            }
            update_texts();
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
                update_graph(cy_left, first_graph_list[first_graph_n], false);
            }
            if (!second_start && second_graph_n >= first_graph_n + 1) {
                second_graph_n--;
                update_graph(cy_right, second_graph_list[second_graph_n], false);
            }
            update_texts();
        } catch (error) {
            alert(error)
        }
    }
}

export function copy(copy_left_to_right) {
    let cy = copy_left_to_right ? cy_right : cy_left;
    let cy_other = copy_left_to_right ? cy_left : cy_right;
    cy.remove(cy.elements());
    cy.add(cy_other.elements());
    cy.fit();
    
}

export function fit(fit_right) {
    if (fit_right) cy_right.fit();
    else cy_left.fit();
}

export function load_graph(graph_to_load, load_right) {
    cy_left.off('add remove');
    cy_right.off('add remove');
    
    let cy = load_right ? cy_right : cy_left;
    let graph = null;
    if (graph_to_load == 'start_graph') {
        graph = JSON.parse(JSON.stringify(graphs.start_graph));
    } else if (graph_to_load == 'first_encounter') {
        graph = JSON.parse(JSON.stringify(graphs.first_encounter));
    } else if (graph_to_load == 'path') {
        graph = JSON.parse(JSON.stringify(graphs.path));
    } else if (graph_to_load == 'dijkstra_faster') {
        graph = JSON.parse(JSON.stringify(graphs.dijkstra_faster));
    } else if (graph_to_load == 'huge_graph') {
        graph = JSON.parse(JSON.stringify(graphs.huge_graph));
    }
    if (graph != null) {
        cy.remove(cy.elements());
        cy.add(graph);
        cy.fit();
    }
    cy_left.on('add remove', (event) => set_graph_select_to_default(false));
    cy_right.on('add remove', (event) => set_graph_select_to_default(true));
}

export function export_image(export_right)
{
    export_as_jpg(export_right ? cy_right : cy_left);
}

export function export_data(export_right)
{
    export_as_txt(export_right ? cy_right : cy_left);
}

export function import_data(event, import_right)
{
    import_txt(event, import_right ? cy_right : cy_left);
}