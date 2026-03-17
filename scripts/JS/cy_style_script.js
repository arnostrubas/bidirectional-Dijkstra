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
            'width': '55px',
            'height': '55px',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-family': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
            'font-size': '12px',
            'border-width': 1.5,
            'border-color': '#646464',
            'background-opacity': 0.5,
            'background-fill': 'linear-gradient',
            'background-gradient-stop-colors': '#b4b4b4 #909090', 
            'background-gradient-stop-positions': '50% 50%',
            'background-gradient-direction': 'to-right',
            'transition-property': 'background-color',
            'transition-duration': '600ms'
        }
    },
    {
        selector: '.highlighted',
        style: {
            'background-color': '#ff0000', 
            'border-width': 3,
            'border-color': '#ff0000'
        }
    },
    {
        selector: 'node[state_f = "PATH"][state_b = "PATH"]',
        style: {
            'background-gradient-stop-colors': '#018803 #018803',
        }
    },
    {
        selector: 'node[state_f = "UNVISITED"][state_b = "OPEN"]',
        style: {
            'background-gradient-stop-colors': '#b4b4b4 #31c8fa', 
        }
    },
    {
        selector: 'node[state_f = "UNVISITED"][state_b = "CLOSED"]',
        style: {
            'background-gradient-stop-colors': '#b4b4b4 #0006a5', 
        }
    },
    {
        selector: 'node[state_f = "OPEN"][state_b = "UNVISITED"]',
        style: {
            'background-gradient-stop-colors': 'orange #909090', 
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
            'background-gradient-stop-colors': 'red #909090', 
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
        selector: 'node[label = "START"], node[label = "TARGET"]',
        style: {
            'font-weight': 'bold',
            'color': '#9f4848',
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
            'font-family': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", 
            'font-size': '20px',
            'color': '#555',
            'text-background-color': 'white',
            'text-background-opacity': 0.8
        }
    },
    {
        selector: 'edge[state = "PATH"]',
        style: {
            'line-color': '#007502',      
            'target-arrow-color': '#007502', 
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
