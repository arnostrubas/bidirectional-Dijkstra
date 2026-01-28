import { remove_vertex, reset, add_vertex } from './cytoscape_script.js'

const startBtn = document.getElementById('start');
const resetBtn = document.getElementById('reset');
const nextBtn = document.getElementById('next_step');
const addVertexBtn = document.getElementById('add_vertex');
const removeVertexBtn = document.getElementById('remove_vertex');
const addEdgeBtn = document.getElementById('add_edge');
const removeEdgeBtn = document.getElementById('remove_edge');
const left_graph_checkbox = document.getElementById('left_graph_enabled');
const right_graph_checkbox = document.getElementById('right_graph_enabled');

startBtn.addEventListener('click', () => {
    try {
        startBtn.disabled = true;
        nextBtn.disabled = false;
        resetBtn.disabled = false;
    }
    catch (error) {
        alert(error.message)
    }
});

resetBtn.addEventListener('click', () => {
    try {
        resetBtn.disabled = true;
        nextBtn.disabled = true;
        startBtn.disabled = false;
        reset();
    }
    catch (error) {
        alert(error.message)
    }
});

addVertexBtn.addEventListener('click', () => {
    try {
        add_vertex(left_graph_checkbox.checked, right_graph_checkbox.checked);
    }
    catch (error) {
        alert(error.message)
    }
});

removeVertexBtn.addEventListener('click', () => {
    try {
        if (left_graph_checkbox.checked || right_graph_checkbox.checked) {
            remove_vertex(left_graph_checkbox.checked, right_graph_checkbox.checked);
        }
    }
    catch (error) {
        alert(error.message)
    }
});

function add_remove_disable() 
{
    addVertexBtn.disabled = true;
    removeVertexBtn.disabled = true;
    addEdgeBtn.disabled = true;
    removeEdgeBtn.disabled = true;
}

function add_remove_enable() 
{
    addVertexBtn.disabled = false;
    removeVertexBtn.disabled = false;
    addEdgeBtn.disabled = false;
    removeEdgeBtn.disabled = false;
}

left_graph_checkbox.addEventListener('click', () => {
    try {
        if (!left_graph_checkbox.checked && !right_graph_checkbox.checked) {
            add_remove_disable();
        } else {
            add_remove_enable();
        }
    }
    catch (error) {
        alert(error.message)
    }
});

right_graph_checkbox.addEventListener('click', () => {
    try {
        if (!left_graph_checkbox.checked && !right_graph_checkbox.checked) {
            add_remove_disable();
        } else {
            add_remove_enable();
        }
    }
    catch (error) {
        alert(error.message)
    }
});