
let currentData = null;

function fetchLink() {
    const urlValue = document.getElementById('link').value;
    const titleDisp = document.getElementById('title');
    const container = document.getElementById('options-container');

    if (!urlValue) return alert("Paste a link!");

    titleDisp.innerText = "Raven Service: Searching...";
    container.innerHTML = "";

    fetch('/get_info', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: urlValue })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            currentData = data;
            titleDisp.innerText = data.title;
            renderButtons(data.formats);
        } else {
            alert(data.message);
            titleDisp.innerText = "Try another link";
        }
    })
    .catch(err => alert("Server Down! Check Termux."));
}

function renderButtons(formats) {
    const container = document.getElementById('options-container');
    container.innerHTML = "";
    
    formats.forEach(f => {
        const btn = document.createElement('button');
        btn.className = "btn-dl";
        btn.innerHTML = `🎬 ${f.res} <span>(${f.size})</span>`;
        btn.onclick = () => alert("Downloading ID: " + f.id); 
        container.appendChild(btn);
    });
}