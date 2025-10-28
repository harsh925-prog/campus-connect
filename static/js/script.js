// Campus Connect JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Processing...';
            }
        });
    });

    // Dynamic date handling for events
    const eventDateInput = document.getElementById('event_date');
    if (eventDateInput) {
        // Set minimum date to today
        const today = new Date().toISOString().slice(0, 16);
        eventDateInput.min = today;
    }

    // Skills input enhancement
    const skillsInput = document.getElementById('skills');
    if (skillsInput) {
        skillsInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                // You could add tag-like functionality here
            }
        });
    }
});

// Utility functions
function showToast(message, type = 'success') {
    // Simple toast notification implementation
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 1050; min-width: 300px;';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// API functions for future enhancements
const CampusConnectAPI = {
    async searchGroups(query) {
        // Implementation for AJAX group search
        console.log('Searching groups for:', query);
    },
    
    async getGroupMembers(groupId) {
        // Implementation for fetching group members
        console.log('Fetching members for group:', groupId);
    }
};