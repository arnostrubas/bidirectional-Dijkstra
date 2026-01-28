import cytoscape from 'https://esm.sh/cytoscape@3.28.1';
import { layout, style } from './cy_style_script.js';

const container1 = document.getElementById('graph_container1');
const container2 = document.getElementById('graph_container2');
let leftNodeCount = 5;
let rightNodeCount = 5;

let cy1 = cytoscape({
    container: container1,
    layout: layout,
    style: style,
});

let cy2 = cytoscape({
    container: container2,
    layout: layout,
    style: style,
});

let elements = [{ data: { id: 's', label: 'S' } },
    { data: { id: '1', label: '1' } },
    { data: { id: '2', label: '2' } },
    { data: { id: '3', label: '3' } },
    { data: { id: '4', label: '4' } },
    { data: { id: '5', label: '5' } },
    { data: { id: 't', label: 'T' } },

    { data: { id: 'e1', source: 's', target: '1', weight: 5 } },
    { data: { id: 'e2', source: 's', target: '2', weight: 4 } },
    { data: { id: 'e3', source: '1', target: '3', weight: 2 } },
    { data: { id: 'e4', source: '2', target: '3', weight: 4 } },
    { data: { id: 'e5', source: '2', target: '4', weight: 1 } },
    { data: { id: 'e6', source: '3', target: '4', weight: 3 } },
    { data: { id: 'e7', source: '4', target: '5', weight: 1 } },
    { data: { id: 'e8', source: '5', target: '3', weight: 8 } },
    { data: { id: 'e9', source: '3', target: 't', weight: 3 } },
];

export function graphs_init() {
    cy1.add(elements);
    cy1.layout(layout).run();
    cy1.fit();
    cy2.add(elements);
    cy2.layout(layout).run();
    cy2.fit();
}

export function add_vertex(left_enabled, right_enabled) {
    if (left_enabled) {
        const x = Math.random() * cy1.width();
        const y = Math.random() * cy1.height();
        leftNodeCount++;
        const node = {
            group: 'nodes',
            data: { id: leftNodeCount, label: leftNodeCount },
            position: {
                x: x,
                y: y
            }
        }
        cy1.add(node);
        cy1.fit();
    }
    if (right_enabled) {
        const x = Math.random() * cy2.width();
        const y = Math.random() * cy2.height();
        rightNodeCount++;
        const node = {
            group: 'nodes',
            data: { id: rightNodeCount, label: rightNodeCount },
            position: {
                x: x,
                y: y
            }
        }
        cy2.add(node);
        cy2.fit();
    }
}

export function remove_vertex(first, second) 
{
    let selected_cy1 = cy1.$('node:selected');
    if (selected_cy1 && first) {
        selected_cy1.forEach(v => {
            if (v.id() === 's' || v.id() === 't') alert("Nelze odstranit počáteční/koncový vrchol");
            else v.remove();
        });
    }
    let selected_cy2 = cy2.$('node:selected');
    if (selected_cy2 && second) {
        selected_cy2.forEach(v => {
            if (v.id() === 's' || v.id() === 't') alert("Nelze odstranit počáteční/koncový vrchol");
            else v.remove();
        });
    }
}

export function reset() {
    cy1.layout(layout).run();
    cy1.fit();
    cy2.layout(layout).run();
    cy2.fit();
}

/*
const rect1 = container1.getBoundingClientRect();
const rect2 = container2.getBoundingClientRect();

let add_vertex_menu = document.getElementById('add_vertex_menu');

cy2.on('cxttap', function(event) {
    if (event.target === cy2) {
        const position = event.position;
        
        add_vertex_menu.style.display = 'block';
        add_vertex_menu.style.left = (event.renderedPosition.x + rect2.left + window.scrollX) + 'px';
        add_vertex_menu.style.top = (event.renderedPosition.y + rect2.top + window.scrollY) + 'px';
    }
});



let selectedElement = null;
const menu = document.getElementById('popup_menu')
*/
