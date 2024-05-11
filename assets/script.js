
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
        button.classList.add('btn-secondary'); // Change button color or style to indicate it has been clicked

    }  else {
        console.error('Failed to update total');
    }
}