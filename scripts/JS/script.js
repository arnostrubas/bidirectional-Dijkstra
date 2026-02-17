import './buttons_script.js';
import { graphs_init } from './cytoscape_script.js'

graphs_init();

window.python_ready = function () 
{
    document.getElementById('start').disabled = false;
}
