document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const sidebar = document.querySelector('.dashboard-sidebar');
    const mobileOverlay = document.querySelector('.mobile-overlay');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            sidebar.classList.toggle('show');
            mobileOverlay.classList.toggle('show');
        });
    }
    
    if (mobileOverlay) {
        mobileOverlay.addEventListener('click', function() {
            sidebar.classList.remove('show');
            mobileOverlay.classList.remove('show');
        });
    }
    
    // User dropdown functionality
    const userDropdown = document.querySelector('.nav-user');
    if (userDropdown) {
        userDropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function() {
            // Dropdown closes automatically with CSS hover, but this prevents issues
        });
    }
    
    // Notification functionality
    const notificationBtn = document.querySelector('.nav-notifications');
    if (notificationBtn) {
        notificationBtn.addEventListener('click', function() {
            // Add notification dropdown functionality here
            console.log('Notifications clicked');
        });
    }
    
    // Table row click functionality
    const tableRows = document.querySelectorAll('.data-table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('click', function(e) {
            // Don't trigger if clicking on action buttons
            if (!e.target.closest('.action-buttons')) {
                // Add row selection or navigation functionality
                console.log('Row clicked:', this);
            }
        });
    });
    
    // Animate stats on page load
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Add loading states for buttons
    const actionButtons = document.querySelectorAll('.btn-action, .btn-primary, .btn-secondary');
    actionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (this.getAttribute('href') === '#' || this.type === 'button') {
                e.preventDefault();
                
                // Add loading state
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
                this.disabled = true;
                
                // Remove loading state after 1 second (replace with actual functionality)
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.disabled = false;
                }, 1000);
            }
        });
    });
    
    // Search functionality
    const searchInputs = document.querySelectorAll('input[type="search"]');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const table = this.closest('.content-section').querySelector('.data-table tbody');
            
            if (table) {
                const rows = table.querySelectorAll('tr');
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(searchTerm) ? '' : 'none';
                });
            }
        });
    });
    
    // Status filter functionality
    const statusSelects = document.querySelectorAll('select');
    statusSelects.forEach(select => {
        select.addEventListener('change', function() {
            const filterValue = this.value.toLowerCase();
            const table = this.closest('.section-header').nextElementSibling.querySelector('.data-table tbody');
            
            if (table && filterValue !== 'all status' && filterValue !== '') {
                const rows = table.querySelectorAll('tr');
                rows.forEach(row => {
                    const statusBadge = row.querySelector('.status-badge');
                    if (statusBadge) {
                        const status = statusBadge.textContent.toLowerCase();
                        row.style.display = status.includes(filterValue) ? '' : 'none';
                    }
                });
            } else if (table) {
                // Show all rows
                const rows = table.querySelectorAll('tr');
                rows.forEach(row => {
                    row.style.display = '';
                });
            }
        });
    });
    
    // Add responsive behavior
    function handleResize() {
        const sidebar = document.querySelector('.dashboard-sidebar');
        const overlay = document.querySelector('.mobile-overlay');
        
        if (window.innerWidth > 1024) {
            sidebar.classList.remove('show');
            overlay.classList.remove('show');
        }
    }
    
    window.addEventListener('resize', handleResize);
});

// Utility functions for dashboard
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Hide notification after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-QA', {
        style: 'currency',
       currency: 'QAR',
       minimumFractionDigits: 0,
       maximumFractionDigits: 0
   }).format(amount);
}

function formatDate(date) {
   return new Intl.DateTimeFormat('en-QA', {
       year: 'numeric',
       month: 'short',
       day: 'numeric'
   }).format(new Date(date));
}

// Chart placeholder functionality
function initializePlaceholderCharts() {
   const chartContainers = document.querySelectorAll('.chart-container .chart-placeholder');
   
   chartContainers.forEach(container => {
       if (container.textContent.includes('chart will be displayed')) {
           container.innerHTML = `
               <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: var(--gray-500);">
                   <i class="fas fa-chart-line" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                   <p style="margin: 0; font-style: italic;">Chart visualization coming soon</p>
                   <p style="margin: 0.5rem 0 0 0; font-size: 0.875rem;">Connect your data source to view analytics</p>
               </div>
           `;
       }
   });
}

// Call chart initialization
initializePlaceholderCharts();