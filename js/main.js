// TryOnYou Main JavaScript File

class TryOnYouApp {
    constructor() {
        this.isCamera = false;
        this.selectedProducts = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupSmoothScrolling();
        console.log('TryOnYou App initialized');
    }

    setupEventListeners() {
        // Contact form submission
        const contactForm = document.querySelector('.contact-form form');
        if (contactForm) {
            contactForm.addEventListener('submit', this.handleContactForm.bind(this));
        }

        // Jules Consultation form
        const julesForm = document.getElementById('jules-form');
        if (julesForm) {
            julesForm.addEventListener('submit', this.handleJulesConsultation.bind(this));
        }

        // Navigation smooth scrolling
        document.querySelectorAll('.nav-menu a[href^="#"]').forEach(link => {
            link.addEventListener('click', this.handleNavClick.bind(this));
        });
    }

    setupSmoothScrolling() {
        // Add smooth scrolling behavior
        document.documentElement.style.scrollBehavior = 'smooth';
    }

    handleNavClick(event) {
        event.preventDefault();
        const targetId = event.target.getAttribute('href');
        const targetSection = document.querySelector(targetId);
        
        if (targetSection) {
            const offsetTop = targetSection.offsetTop - 80; // Account for fixed header
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    }

    handleContactForm(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const name = formData.get('name') || event.target.querySelector('input[type="text"]').value;
        const email = formData.get('email') || event.target.querySelector('input[type="email"]').value;
        const message = formData.get('message') || event.target.querySelector('textarea').value;

        // Simple validation
        if (!name || !email || !message) {
            this.showNotification('Please fill in all fields', 'error');
            return;
        }

        // Simulate form submission
        this.showNotification('Message sent successfully!', 'success');
        event.target.reset();
    }

    async handleJulesConsultation(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const data = {
            height: parseFloat(formData.get('height')),
            weight: parseFloat(formData.get('weight')),
            event_type: formData.get('event_type')
        };

        const resultContainer = document.getElementById('jules-result');
        const resultText = document.getElementById('recommendation-text');
        const submitBtn = event.target.querySelector('button[type="submit"]');

        try {
            submitBtn.textContent = 'Consulting Jules...';
            submitBtn.disabled = true;

            // Call Backend
            // Assuming backend is running on localhost:8000
            const response = await fetch('http://localhost:8000/api/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error('Jules is currently unavailable.');
            }

            const result = await response.json();

            if (result.status === 'success') {
                resultContainer.style.display = 'block';
                resultText.textContent = result.recommendation;
                this.showNotification('Jules has a recommendation for you!', 'success');
            } else {
                throw new Error('Could not get recommendation.');
            }

        } catch (error) {
            console.error(error);
            this.showNotification('Error consulting Jules. Backend offline?', 'error');
            resultContainer.style.display = 'block';
            resultText.textContent = "Desolé. Jules is currently offline. Please ensure the backend server is running on port 8000.";
        } finally {
            submitBtn.textContent = 'Ask Jules';
            submitBtn.disabled = false;
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        Object.assign(notification.style, {
            position: 'fixed',
            top: '100px',
            right: '20px',
            padding: '15px 20px',
            borderRadius: '5px',
            color: 'white',
            fontWeight: '600',
            zIndex: '10000',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease'
        });

        // Set background color based on type
        const colors = {
            success: '#4CAF50',
            error: '#f44336',
            info: '#2196F3'
        };
        notification.style.backgroundColor = colors[type] || colors.info;

        // Add to page
        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
}

// Global functions for HTML onclick handlers
function startTryOn() {
    const tryOnSection = document.getElementById('try-on');
    if (tryOnSection) {
        const offsetTop = tryOnSection.offsetTop - 80;
        window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
        });
    }
    
    // Show notification
    if (window.app) {
        window.app.showNotification('Welcome to the Try-On Studio!', 'info');
    }
}

function toggleCamera() {
    const cameraView = document.querySelector('.camera-view');
    const cameraBtn = document.querySelector('.camera-btn');
    const cameraPlaceholder = document.querySelector('.camera-placeholder');
    
    if (!window.app) return;

    if (!window.app.isCameraActive) {
        // Start camera simulation
        window.app.isCameraActive = true;
        cameraView.classList.add('active');
        cameraBtn.textContent = 'Stop Camera';
        cameraPlaceholder.innerHTML = '<p>📹 Camera Active</p><p>Virtual try-on ready!</p>';
        window.app.showNotification('Camera activated! Select products to try on.', 'success');
    } else {
        // Stop camera
        window.app.isCameraActive = false;
        cameraView.classList.remove('active');
        cameraBtn.textContent = 'Start Camera';
        cameraPlaceholder.innerHTML = '<p>Camera View</p><p>Click "Start Camera" to begin</p>';
        window.app.showNotification('Camera stopped.', 'info');
    }
}

function selectProduct(productId) {
    if (!window.app) return;

    const productItem = document.querySelector(`[onclick="selectProduct('${productId}')"]`);
    
    if (productItem.classList.contains('selected')) {
        // Deselect product
        productItem.classList.remove('selected');
        const index = window.app.selectedProducts.indexOf(productId);
        if (index > -1) {
            window.app.selectedProducts.splice(index, 1);
        }
        window.app.showNotification(`${productId} removed from try-on`, 'info');
    } else {
        // Select product
        productItem.classList.add('selected');
        window.app.selectedProducts.push(productId);
        window.app.showNotification(`${productId} added to try-on!`, 'success');
        
        // If camera is active, simulate try-on
        if (window.app.isCameraActive) {
            setTimeout(() => {
                window.app.showNotification(`Virtual try-on: ${productId} applied!`, 'success');
            }, 1000);
        }
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TryOnYouApp();
});

// Add some interactive animations
document.addEventListener('DOMContentLoaded', () => {
    // Animate feature cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe feature cards
    document.querySelectorAll('.feature-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
});

// Export for potential module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TryOnYouApp;
}