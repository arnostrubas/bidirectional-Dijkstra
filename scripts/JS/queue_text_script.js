/**
 * Copyright (c) 2026, Arnošt Rubáš
 * All rights reserved.
 *
 * This source code is licensed under the BSD 3-Clause License.
 * The full text of the license can be found in the LICENSE file 
 * in the root directory of this project.
 */

/**
 * Sets text of element with id {@link id} to {@link value} 
 * @param {string} id - hmtl id of element to have its text changed
 * @param {string} value - string to set the element to 
 */
function setText(id, value) {
    const element = document.getElementById(id);
    if (element) element.innerText = value;
}

/**
 * Converts {@link num} into upper index
 * @param {int} num 
 * @returns upper index of {@link num}
 */
export function toUper(num) {
    const uper = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
    };
    return num.toString().split('').map(char => uper[char] || char).join('');
}

/**
 * Converts queue into string
 * @param {Object} Q - queue 
 * @returns text represenatiton of {@link Q}
 */
export function queue_to_text(Q)
{
    let text = "";
    if (Q) {
        Q.queue.sort((x, y) => x[0] - y[0]).forEach(tuple => {
            let [priority, id] = tuple;
            let label = id.toString();
            if (id == -1) label = 'START';
            if (id == 0) label = 'TARGET';
            let priorityTxt = toUper(priority);
            text += label + priorityTxt + "   "
        });
    }
    return text
}

/**
 * Updates queue and explain text containers
 * @param {Object} Qf1 - queue
 * @param {Object} Qb1 - queue
 * @param {Object} Qf2 - queue
 * @param {Object} Qb2 - queue
 * @param {string} text1 
 * @param {string} text2 
 */
export function update_text_containers(Qf1, Qb1, Qf2, Qb2, text1="", text2="")
{
    setText('Qf1_text', queue_to_text(Qf1));
    setText('Qb1_text', queue_to_text(Qb1));

    setText('Qf2_text', queue_to_text(Qf2));
    setText('Qb2_text', queue_to_text(Qb2));

    setText('explain_text1', text1);
    setText('explain_text2', text2);
}

export function reset_text_containers()
{
    setText('Qf1_text', "");
    setText('Qb1_text', "");
    setText('Qf2_text', "");
    setText('Qb2_text', "");
    setText('explain_text1', "");
    setText('explain_text2', "");
}

