export let layout = {
    name: 'breadthfirst',
    animate: false,
    padding: 10,
};
export let style = [
    {
        selector: 'node',
        style: {
            'label': 'data(label)',
            'width': '50px',
            'height': '50px',
            'text-valign': 'center',
            'text-halign': 'center',
            'color': '#333',
            'font-size': '12px',
            'border-width': 2,
            'border-color': '#555'
        }
    },
    {
        selector: 'node[state = "UNVISITED"]',
        style: {
            'background-color': '#e0e0e0', 
        }
    },
    {
        selector: 'node[state = "OPEN"]',
        style: {
            'background-color': '#ffc107',
            'border-color': '#d39e00'
        }
    },
    {
        selector: 'node[state = "CLOSED"]',
        style: {
            'background-color': '#28a745',
            'color': 'white',
            'border-color': '#1e7e34'
        }
    },
    {
        selector: 'edge',
        style: {
            'curve-style': 'bezier',
            'width': '3px',
            'line-color': '#999',
            'target-arrow-shape': 'triangle',
            'target-arrow-color': '#999',
            'label': 'data(weight)', 
            'font-size': '20px',
            'color': '#555',
            'text-background-color': 'white',
            'text-background-opacity': 0.8
        }
    },
    {
        selector: 'edge:selected',
        style: {
            'line-color': '#FF0000',      
            'target-arrow-color': '#FF0000', 
            'width': 4,                    
            'opacity': 1                   
        }
    },
    {
        selector: '.eh-handle',
        style: {
            'background-color': 'red',
            'width': 20,
            'height': 20,
            'shape': 'ellipse',
            'overlay-opacity': 0,
            'border-width': 12, 
            'border-opacity': 0
            }
        },
        {
            selector: '.eh-hover',
            style: {
            'background-color': 'red'
            }
        },
        {
            selector: '.eh-source',
            style: {
            'border-width': 2,
            'border-color': 'red'
            }
        },
        {
            selector: '.eh-target',
            style: {
                'border-width': 2,
                'border-color': 'red'
            }
        },
        {
            selector: '.eh-preview, .eh-ghost-edge',
            style: {
                'background-color': 'red',
                'line-color': 'red',
                'target-arrow-color': 'red',
                'source-arrow-color': 'red'
            }
        },
        {
            selector: '.eh-ghost-edge.eh-preview-active',
            style: {
            'opacity': 0
            }
        }
];
