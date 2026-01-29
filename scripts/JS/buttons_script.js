import { disableVertexAdding, enableVertexAdding, enableEdgeAdding, disableEdgeAdding, remove_edge, remove_vertex, reset } from './cytoscape_script.js'
import { create_json_of_graphs } from './JS_json.js'

const startBtn = document.getElementById('start');
const resetBtn = document.getElementById('reset');
const nextBtn = document.getElementById('next_step');
const prevBtn = document.getElementById('prev_step')

const addVertexCheckbox = document.getElementById('add_vertex');
const removeVertexBtn = document.getElementById('remove_vertex');
const addEdgeCheckBox = document.getElementById('add_edge');
const removeEdgeBtn = document.getElementById('remove_edge');

const bothGraphsCheckBox = document.getElementById('both_graphs');

const end_strat1 = document.getElementById('end_strategy_1');
const search_strat1 = document.getElementById('search_strategy_1');

const end_strat2 = document.getElementById('end_strategy_2');
const search_strat2 = document.getElementById('search_strategy_2');

function add_remove_disable() 
{
    removeVertexBtn.disabled = true;
    removeEdgeBtn.disabled = true;

    addEdgeCheckBox.disabled = true;
    addEdgeCheckBox.checked = false;
    disableEdgeAdding();

    addVertexCheckbox.disabled = true;
    addVertexCheckbox.checked = false;
    disableVertexAdding();
}

function add_remove_enable() 
{
    removeVertexBtn.disabled = false;
    removeEdgeBtn.disabled = false;
    addEdgeCheckBox.disabled = false;
    enableEdgeAdding();
    addVertexCheckbox.disabled = false;
    enableVertexAdding();
}

startBtn.addEventListener('click', () => {
    try {
        /*!!!!!!!!!!!!!!!!!!!!!!!!!REMOVE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!*/ 
        if (false && (search_strat1.value === 'default' || search_strat2.value === 'default' ||
            end_strat1.value === 'default' || end_strat2.value === 'default')) {
                alert("vyberte všechny strategie");
        }
        else {
            startBtn.disabled = true;
            nextBtn.disabled = false;
            prevBtn.disabled = false;
            resetBtn.disabled = false;
            add_remove_disable();
            create_json_of_graphs(search_strat1, search_strat2, end_strat1, end_strat2);
        }
    }
    catch (error) {
        alert(error.message)
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
        alert(error.message)
    }
});

addVertexCheckbox.addEventListener('click', () => {
    try {
        if (addVertexCheckbox.checked) enableVertexAdding();
        else disableVertexAdding();
    }
    catch (error) {
        alert(error.message)
    }
});

removeVertexBtn.addEventListener('click', () => {
    try {
        remove_vertex();
    }
    catch (error) {
        alert(error.message)
    }
});

removeEdgeBtn.addEventListener('click', () => {
    try {
        remove_edge();
    }
    catch (error) {
        alert(error.message)
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
        alert(error.message)
    }
})
