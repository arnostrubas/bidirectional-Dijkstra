export function setText(id, value) {
    const element = document.getElementById(id);
    if (element) element.innerText = value;
}