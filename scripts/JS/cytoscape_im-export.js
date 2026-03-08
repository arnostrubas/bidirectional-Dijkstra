function generic_export(data, file_name)
{
    const downloadLink = document.createElement('a');
    downloadLink.href = data;
    downloadLink.download = file_name;

    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}


export function export_as_jpg(cy)
{
    let jpgData = cy.jpg({
            full: true,
            quality: 0.9 
    });
    generic_export(jpgData, 'graph_export.jpg');
}

export function export_as_txt(cy)
{
    const jsonString = JSON.stringify(clean_data(cy), null, 4);
    const blob = new Blob([jsonString], {type: 'text/plans'});
    const url = URL.createObjectURL(blob);
    generic_export(url, 'graph_data_export.txt')
}

export function import_txt(event, cy)
{
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const content = e.target.result;
            const data = JSON.parse(content);
            cy.batch(() => {
                cy.elements().remove(); 

                data.nodes.forEach(n => {
                    cy.add({
                        group: 'nodes',
                        data: { id: n.id, label: n.label },
                        position: { x: n.x, y: n.y }
                    });
                });

                data.edges.forEach(e => {
                    cy.add({
                        group: 'edges',
                        data: { id: e.id, source: e.source, target: e.target, weight: e.weight }
                    });
                });
            });
        };

        reader.readAsText(file);

        event.target.value = '';
    }
}