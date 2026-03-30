/**
 * Copyright (c) 2026, Arnošt Rubáš
 * All rights reserved.
 *
 * This source code is licensed under the BSD 3-Clause License.
 * The full text of the license can be found in the LICENSE file 
 * in the root directory of this project.
 */

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
