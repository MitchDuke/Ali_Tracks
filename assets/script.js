
async function addAmount(month) {
    const button = document.getElementById(month);
    if (button.disabled) return; // If button is disabled, do nothing

    const response = await fetch('/update_total', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ month: month})
    });

    if (response.ok) {
        const data = await response.json();
        document.getElementById('total').textContent = `Total: £${data.total}`;
        button.disabled = true; // Disable the button after it's clicked
        button.classList.remove('btn-primary');
        button.classList.add('btn-secondary'); // Change button color or style to indicate it has been clicked

    }  else {
        console.error('Failed to update total');
    }
}

window.onload = async function() {
    const response = await fetch('/get_total');
    if (response.ok) {
        const data = await response.json();
        document.getElementById('total').textContent = data.total;
    } else {
        console.error('Failed to fetch total');
    }
};