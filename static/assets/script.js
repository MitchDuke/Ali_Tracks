async function addAmount(month) {
    const button = document.getElementById(month);
    if (button.disabled) return; // If button is disabled, do nothing

    try {
        const response = await fetch('/update_total', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ month: month })
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('total').textContent = `Total: £${data.total}`;
            button.disabled = true; // Disable the button after it's clicked
            button.classList.remove('btn-primary');
            button.classList.add('btn-secondary'); // Change button color or style to indicate it has been clicked
        } else {
            console.error('Failed to update total');
        }
    } catch (error) {
        console.error('Error updating total:', error);
    }
}

window.onload = async function() {
    try {
        const response = await fetch('/get_total');
        if (response.ok) {
            const data = await response.json();
            document.getElementById('total').textContent = `Total: £${data.total}`;
        } else {
            console.error('Failed to fetch total');
        }
    } catch (error) {
        console.error('Error fetching total:', error);
    }
};

async function resetTotal() {
    try {
        const response = await fetch('/reset_total', {
            method: 'POST'
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('total').textContent = `Total: £${data.total}`;

            // Enable all buttons and reset their styles
            const buttons = document.getElementsByClassName('month-button');
            for (let button of buttons) {
                button.disabled = false;
                button.classList.remove('btn-secondary');
                button.classList.add('btn-primary');
            }
        } else {
            console.error('Failed to reset total');
        }
    } catch (error) {
        console.error('Error resetting total:', error);
    }
}
