import { copy, final_path_or_start, move, calculate, disableVertexAdding, enableVertexAdding, enableEdgeAdding, disableEdgeAdding, disableVertexRemoving, enableVertexRemoving, enableEdgeRemoving, disableEdgeRemoving, reset } from './cytoscape_script.js'
import { create_json_of_graphs } from './JS_json.js'

const startBtn = document.getElementById('start');
const resetBtn = document.getElementById('reset');
const nextBtn = document.getElementById('next_step');
const prevBtn = document.getElementById('prev_step');
const leftCopyBtn = document.getElementById('copy_left');
const rightCopyBtn = document.getElementById('copy_right');

const addVertexCheckbox = document.getElementById('add_vertex');
const removeVertexCheckbox = document.getElementById('remove_vertex');
const addEdgeCheckBox = document.getElementById('add_edge');
const removeEdgeCheckbox = document.getElementById('remove_edge');

const end_strat1 = document.getElementById('end_strategy_1');
const search_strat1 = document.getElementById('search_strategy_1');
const end_strat2 = document.getElementById('end_strategy_2');
const search_strat2 = document.getElementById('search_strategy_2');

const move_size = document.getElementById('number_of_steps');

// =============================
//    ENABLE/DISABLE functions
// =============================

function add_remove_disable() 
{
    removeVertexCheckbox.disabled = true;
    removeEdgeCheckbox.disabled = true;

    addEdgeCheckBox.disabled = true;
    addEdgeCheckBox.checked = false;
    disableEdgeAdding();

    addVertexCheckbox.disabled = true;
    addVertexCheckbox.checked = false;
    disableVertexAdding();

    rightCopyBtn.disabled = true;
    leftCopyBtn.disabled = true;
}

function add_remove_enable() 
{
    removeVertexCheckbox.disabled = false;
    removeEdgeCheckbox.disabled = false;
    addEdgeCheckBox.disabled = false;
    addVertexCheckbox.disabled = false;
    rightCopyBtn.disabled = false;
    leftCopyBtn.disabled = false;
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
            startBtn.disabled = true;
            nextBtn.disabled = false;
            prevBtn.disabled = false;
            resetBtn.disabled = false;
            add_remove_disable();
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
        resetBtn.disabled = true;
        nextBtn.disabled = true;
        prevBtn.disabled = true;
        startBtn.disabled = false;
        add_remove_enable();
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
        copy(true);
    }
    catch (error) {
        alert(error.message);
    }
});

rightCopyBtn.addEventListener('click', () => {
    try {
        copy(false);
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
