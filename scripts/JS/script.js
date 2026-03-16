import './buttons_script.js';
import { graphs_init } from './cytoscape_script.js'

graphs_init();

/**
 * enables start button when python is ready
 */
window.python_ready = function () 
{
    document.getElementById('start').disabled = false;
}
