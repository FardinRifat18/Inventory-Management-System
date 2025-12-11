// Inventory Management System JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirmations for destructive actions
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm');
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Dynamic form handling for purchase orders
    const productSelect = document.getElementById('id_product');
    if (productSelect) {
        productSelect.addEventListener('change', function() {
            const productId = this.value;
            if (productId) {
                fetch(`/api/product/${productId}/`)
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('id_unit_cost').value = data.cost_price;
                    })
                    .catch(error => console.error('Error:', error));
            }
        });
    }

    // Stock level indicators
    const stockLevels = document.querySelectorAll('.stock-level');
    stockLevels.forEach(level => {
        const current = parseInt(level.getAttribute('data-current'));
        const min = parseInt(level.getAttribute('data-min'));
        
        if (current === 0) {
            level.classList.add('stock-out');
        } else if (current <= min) {
            level.classList.add('stock-low');
        } else {
            level.classList.add('stock-ok');
        }
    });
});

// Utility functions
const InventoryUtils = {
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    },
    
    formatDate: function(dateString) {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },
    
    calculateProfit: function(cost, selling) {
        return ((selling - cost) / cost * 100).toFixed(2);
    }
};