// MyAdmin JavaScript

// Toast notification function
function showToast(message, type = 'success', duration = 5000) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-icon">${type === 'success' ? '✓' : type === 'error' ? '✗' : 'ℹ'}</div>
        <div class="toast-message">${message}</div>
        <button class="toast-close" onclick="this.parentElement.remove()">×</button>
    `;
    document.body.appendChild(toast);
    
    if (type === 'success') {
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }
}

// Modal functions
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

// Confirm delete action
function confirmDelete(itemName, formId) {
    if (confirm(`Are you sure you want to delete "${itemName}"? This action cannot be undone.`)) {
        document.getElementById(formId).submit();
    }
}

// Bulk action confirmation
function confirmBulkAction(action) {
    const checkboxes = document.querySelectorAll('input[name="product_ids"]:checked');
    if (checkboxes.length === 0) {
        showToast('Please select at least one item.', 'warning');
        return false;
    }
    
    if (action === 'delete') {
        return confirm(`Are you sure you want to delete ${checkboxes.length} item(s)? This action cannot be undone.`);
    }
    
    return true;
}

// Image preview
function previewImage(input, previewId) {
    const preview = document.getElementById(previewId);
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('MyAdmin JS loaded');
    
    // Mobile menu functionality
    const menuToggle = document.getElementById('mobileMenuToggle');
    const sidebar = document.getElementById('adminSidebar');
    const overlay = document.getElementById('sidebarOverlay');
    
    console.log('Menu elements:', {
        menuToggle: menuToggle,
        sidebar: sidebar,
        overlay: overlay
    });
    
    if (menuToggle && sidebar && overlay) {
        console.log('Setting up mobile menu...');
        
        // Toggle menu
        menuToggle.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Menu toggle clicked');
            sidebar.classList.toggle('open');
            overlay.classList.toggle('active');
            console.log('Sidebar classes:', sidebar.className);
            console.log('Overlay classes:', overlay.className);
        });
        
        // Close menu when clicking overlay
        overlay.addEventListener('click', function() {
            console.log('Overlay clicked');
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
        });
        
        // Close menu when clicking a link (on mobile)
        const sidebarLinks = sidebar.querySelectorAll('a');
        sidebarLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth <= 768) {
                    sidebar.classList.remove('open');
                    overlay.classList.remove('active');
                }
            });
        });
    } else {
        console.error('Mobile menu elements not found!');
    }
    
    // Select all checkbox functionality
    const selectAllCheckbox = document.getElementById('selectAll');
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('input[name="product_ids"]');
            checkboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
        });
    }
});

// Close modal on overlay click
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.style.display = 'none';
    }
});

// Close modal on ESC key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal-overlay');
        modals.forEach(modal => modal.style.display = 'none');
    }
});

// Add slideOut animation to CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
