// Auto-dismiss flash messages after 5 seconds
setTimeout(function() {
    var flashMessage = document.getElementById('flash-message');
    if (flashMessage) {
        flashMessage.style.transition = 'opacity 0.5s ease-in-out';
        flashMessage.style.opacity = '0';
        setTimeout(function() {
            flashMessage.remove();
        }, 500);
    }
}, 3000);


// Ensure all buttons are disabled by default and re-enable them when input is detected
document.querySelectorAll('.goal-input').forEach((input) => {
    const buttonId = input.id.replace('goal-', 'update-btn-');
    const button = document.getElementById(buttonId);

    // Disable button on load if no value
    if (!input.value) {
        button.disabled = true;
    }

    // Enable/disable button based on input value
    input.addEventListener('input', function () {
        button.disabled = !input.value.trim();
    });
});

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
            console.log('Update total response:', data); // Debugging statement
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
            console.log('Get Total response:', data); // Debugging statement
            const totalElement = document.getElementById('total');
            if (totalElement) {
                totalElement.textContent = `Total: £${data.total}`;
            }

            // Determine the number of buttons to disable based on the total saved
            const totalSaved = data.total;
            const months = [
                'january', 'february', 'march', 'april',
                'may', 'june', 'july', 'august',
                'september', 'october', 'november', 'december'
            ];
            const buttonsToDisable = totalSaved / 5;

            for (let i = 0; i < buttonsToDisable; i++) {
                const button = document.getElementById(months[i]);
                button.disabled = true;
                button.classList.remove('btn-primary');
                button.classList.add('btn-secondary');
            }
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
            console.log('Reset total response:', data); // Debugging statement
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
