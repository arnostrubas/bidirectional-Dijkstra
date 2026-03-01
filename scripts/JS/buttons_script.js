import { load_graph, cy_export, fit, copy, final_path_or_start, move, calculate, reset,
    disableVertexAdding, enableVertexAdding, enableEdgeAdding, disableEdgeAdding, 
    disableVertexRemoving, enableVertexRemoving, enableEdgeRemoving, disableEdgeRemoving } from './cytoscape_script.js'
import { create_json_of_graphs } from './JS_json.js'

const startBtn = document.getElementById('start');
const resetBtn = document.getElementById('reset');
const nextBtn = document.getElementById('next_step');
const prevBtn = document.getElementById('prev_step');
const leftCopyBtn = document.getElementById('copy_left');
const rightCopyBtn = document.getElementById('copy_right');
const leftFitBtn = document.getElementById('fit_left');
const rightFitBtn = document.getElementById('fit_right');
const leftExportBtn = document.getElementById('export_left');
const rightExportBtn = document.getElementById('export_right');

const addVertexCheckbox = document.getElementById('add_vertex');
const removeVertexCheckbox = document.getElementById('remove_vertex');
const addEdgeCheckBox = document.getElementById('add_edge');
const removeEdgeCheckbox = document.getElementById('remove_edge');

const end_strat1 = document.getElementById('end_strategy_1');
const search_strat1 = document.getElementById('search_strategy_1');
const end_strat2 = document.getElementById('end_strategy_2');
const search_strat2 = document.getElementById('search_strategy_2');
const load_graph_left = document.getElementById('load_graph_left');
const load_graph_right = document.getElementById('load_graph_right');

const move_size = document.getElementById('number_of_steps');

// =============================
//    ENABLE/DISABLE functions
// =============================

function btn_disable() 
{
    startBtn.disabled = true;
    nextBtn.disabled = false;
    prevBtn.disabled = false;
    resetBtn.disabled = false;
    rightCopyBtn.disabled = true;
    leftCopyBtn.disabled = true;

    removeVertexCheckbox.disabled = true;
    removeVertexCheckbox.checked = false;
    disableVertexRemoving();

    removeEdgeCheckbox.disabled = true;
    removeEdgeCheckbox.checked = false;
    disableEdgeRemoving();

    addEdgeCheckBox.disabled = true;
    addEdgeCheckBox.checked = false;
    disableEdgeAdding();

    addVertexCheckbox.disabled = true;
    addVertexCheckbox.checked = false;
    disableVertexAdding();

    end_strat1.disabled = true;
    end_strat2.disabled = true;
    search_strat1.disabled = true;
    search_strat2.disabled = true;
}

function btn_enable() 
{
    resetBtn.disabled = true;
    nextBtn.disabled = true;
    prevBtn.disabled = true;
    startBtn.disabled = false;
    rightCopyBtn.disabled = false;
    leftCopyBtn.disabled = false;

    removeVertexCheckbox.disabled = false;
    removeEdgeCheckbox.disabled = false;
    addEdgeCheckBox.disabled = false;
    addVertexCheckbox.disabled = false;

    end_strat1.disabled = false;
    end_strat2.disabled = false;
    search_strat1.disabled = false;
    search_strat2.disabled = false;
}

// =============================
//          BUTTONS
// =============================

startBtn.addEventListener('click', () => {
    try { 
        if (search_strat1.value === 'default' || search_strat2.value === 'default' ||
            end_strat1.value === 'default' || end_strat2.value === 'default') {
                alert("vyberte všechny strategie");
        }
        else {
            btn_disable();
            let json = create_json_of_graphs(search_strat1, search_strat2, end_strat1, end_strat2);
            calculate(json);
        }
    }
    catch (error) {
        alert(error.message);
    }
});

resetBtn.addEventListener('click', () => {
    try {
        btn_enable();
        reset();
    }
    catch (error) {
        alert(error.message);
    }
});

nextBtn.addEventListener('click', () => {
    try {
        if (move_size.value == 'one_edge') move(true);
        else final_path_or_start(true);
    }
    catch (error) {
        alert(error.message);
    }
});

prevBtn.addEventListener('click', () => {
    try {
        if (move_size.value == 'one_edge') move(false);
        else final_path_or_start(false);
    }
    catch (error) {
        alert(error.message);
    }
});

leftCopyBtn.addEventListener('click', () => {
    try {
        const confirm = window.confirm("Do you really want to copy right graph to the left container?");
        if (confirm) copy(false);
    }
    catch (error) {
        alert(error.message);
    }
});

rightCopyBtn.addEventListener('click', () => {
    try {
        const confirm = window.confirm("Do you really want to copy left graph to the right container?");
        if (confirm) copy(true);
    }
    catch (error) {
        alert(error.message);
    }
});

rightFitBtn.addEventListener('click', () => {
    try {
        fit(true);
    }
    catch (error) {
        alert(error.message);
    }
});

leftFitBtn.addEventListener('click', () => {
    try {
        fit(false);
    }
    catch (error) {
        alert(error.message);
    }
});

leftExportBtn.addEventListener('click', () => {
    try {
        cy_export(false);
    }
    catch (error) {
        alert(error.message);
    }
});

rightExportBtn.addEventListener('click', () => {
    try {
        cy_export(true);
    }
    catch (error) {
        alert(error.message);
    }
});

// =============================
//          CHECKBOXES
// =============================

addVertexCheckbox.addEventListener('click', () => {
    try {
        if (addVertexCheckbox.checked) enableVertexAdding();
        else disableVertexAdding();
    }
    catch (error) {
        alert(error.message);
    }
});

removeVertexCheckbox.addEventListener('click', () => {
    try {
        if (removeVertexCheckbox.checked) enableVertexRemoving();
        else disableVertexRemoving();
    }
    catch (error) {
        alert(error.message);
    }
});

removeEdgeCheckbox.addEventListener('click', () => {
    try {
        if (removeEdgeCheckbox.checked) enableEdgeRemoving();
        else disableEdgeRemoving();
    }
    catch (error) {
        alert(error.message);
    }
});

addEdgeCheckBox.addEventListener('click', () => {
    try {
        if (addEdgeCheckBox.checked) {
            enableEdgeAdding();
        } else {
            disableEdgeAdding();
        }
    }
    catch (error) {
        alert(error.message);
    }
});

load_graph_left.addEventListener('change', () => {
    try {
        load_graph(load_graph_left.value, false);
    }
    catch (error) {
        alert(error.message);
    }
});

load_graph_right.addEventListener('change', () => {
    try {
        load_graph(load_graph_right.value, true);
    }
    catch (error) {
        alert(error.message);
    }
});