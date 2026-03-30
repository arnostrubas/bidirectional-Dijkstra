/**
 * Copyright (c) 2026, Arnošt Rubáš
 * All rights reserved.
 *
 * This source code is licensed under the BSD 3-Clause License.
 * The full text of the license can be found in the LICENSE file 
 * in the root directory of this project.
 */

/**
 * Switches ids of two vertexes. Also reroutes all edge leading in/from these vertexes so only the ids are changed
 * @param {cytoscape.Core} cy - cytoscape in which vertexes should be switched  
 * @param {*} old_id - id of first vertex
 * @param {*} new_id - id of second vertex
 */
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

/**
 * Shows popper of node that has been clicked in {@link event}
 * @param {*} evt 
 * @param {cytoscape.Core} cy - cytoscape in which to show popper 
 * @param {boolen} running_visualisation - whether cis is running, if true, buttons in popper are disabled
 */
export function show_popper(evt, cy, running_visualisation)
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
            Vertex: ${node.data('label')}
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
        <div id="popper_btns">
            <button class="popper_btn" id="start_change_btn">Set as START</button>
            <button class="popper_btn" id="target_change_btn">Set as TARGET</button>
        <div>
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
