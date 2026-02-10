export let layout = {
    name: 'preset',
    padding: 50,
    fit: true
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
            'font-size': '12px',
            'border-width': 2,
            'border-color': '#555',
            'background-opacity': 0.5,
            'background-fill': 'linear-gradient',
            'background-gradient-stop-colors': 'gray gray', 
            'background-gradient-stop-positions': '50% 50%',
            'background-gradient-direction': 'to-right',
            'transition-property': 'background-color',
            'transition-duration': '600ms'
        }
    },
    {
        selector: '.highlighted',
        style: {
            'background-color': '#ff0000', // zlatá barva při bliknutí
            'border-width': 4,
            'border-color': '#ff0000'
        }
    },
    {
        selector: 'node[state_f = "PATH"][state_b = "PATH"]',
        style: {
            'background-gradient-stop-colors': 'green green',
        }
    },
    {
        selector: 'node[state_f = "UNVISITED"][state_b = "OPEN"]',
        style: {
            'background-gradient-stop-colors': 'gray #31c8fa', 
        }
    },
    {
        selector: 'node[state_f = "UNVISITED"][state_b = "CLOSED"]',
        style: {
            'background-gradient-stop-colors': 'gray #0006a5', 
        }
    },
    {
        selector: 'node[state_f = "OPEN"][state_b = "UNVISITED"]',
        style: {
            'background-gradient-stop-colors': 'orange gray', 
        }
    },
    {
        selector: 'node[state_f = "OPEN"][state_b = "OPEN"]',
        style: {
            'background-gradient-stop-colors': 'orange #31c8fa', 
        }
    },
    {
        selector: 'node[state_f = "OPEN"][state_b = "CLOSED"]',
        style: {
            'background-gradient-stop-colors': 'orange #0006a5', 
        }
    },
    {
        selector: 'node[state_f = "CLOSED"][state_b = "UNVISITED"]',
        style: {
            'background-gradient-stop-colors': 'red gray', 
        }
    },
    {
        selector: 'node[state_f = "CLOSED"][state_b = "OPEN"]',
        style: {
            'background-gradient-stop-colors': 'red #31c8fa', 
        }
    },
    {
        selector: 'node[state_f = "CLOSED"][state_b = "CLOSED"]',
        style: {
            'background-gradient-stop-colors': 'red #0006a5', 
        }
    },
    {
        selector: 'node:selected',
        style: {
            'border-width': 4,     
            'border-color': '#2a0ce7',
            'border-opacity': 1
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
            'line-color': '#2a0ce7',      
            'target-arrow-color': '#2a0ce7', 
            'width': 4,                    
            'opacity': 1                   
        }
    },
    {
        selector: 'edge[state = "PATH"]',
        style: {
            'line-color': 'green',      
            'target-arrow-color': 'green', 
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
