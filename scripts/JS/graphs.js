export let basic_graph = [
    { data: { id: '-1', label: 'S' }, position: { x: 0, y: 0 } },
    { data: { id: '1', label: '1' }, position: { x: 0, y: 0 } },
    { data: { id: '2', label: '2' }, position: { x: 0, y: 0 } },
    { data: { id: '3', label: '3' }, position: { x: 0, y: 0 } },
    { data: { id: '4', label: '4' }, position: { x: 0, y: 0 } },
    { data: { id: '5', label: '5' }, position: { x: 0, y: 0 } },
    { data: { id: '6', label: '6' }, position: { x: 0, y: 0 } },
    { data: { id: '0', label: 'T' }, position: { x: 0, y: 0 } },

    { data: { id: 'e1', source: '-1', target: '1', weight: 5 } },
    { data: { id: 'e2', source: '-1', target: '2', weight: 4 } },
    { data: { id: 'e3', source: '1', target: '3', weight: 2 } },
    { data: { id: 'e4', source: '2', target: '3', weight: 4 } },
    { data: { id: 'e5', source: '2', target: '4', weight: 1 } },
    { data: { id: 'e6', source: '3', target: '4', weight: 3 } },
    { data: { id: 'e7', source: '4', target: '5', weight: 1 } },
    { data: { id: 'e8', source: '5', target: '3', weight: 8 } },
    { data: { id: 'e9', source: '3', target: '0', weight: 3 } },
    { data: { id: 'e10', source: '4', target: '6', weight: 2 } },
    { data: { id: 'e11', source: '0', target: '6', weight: 4 } },
    { data: { id: 'e12', source: '-1', target: '0', weight: 10000}}
];