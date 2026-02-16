export function setText(id, value) {
    const element = document.getElementById(id);
    if (element) element.innerText = value;
}

export function toUper(num) {
    const uper = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
    };
    return num.toString().split('').map(char => uper[char] || char).join('');
}


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

export function update_queues(Qf1, Qb1, Qf2, Qb2)
{
    setText('Qf1_text', queue_to_text(Qf1));
    setText('Qb1_text', queue_to_text(Qb1));

    setText('Qf2_text', queue_to_text(Qf2));
    setText('Qb2_text', queue_to_text(Qb2));
}

