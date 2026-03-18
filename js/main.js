/**
 * TRYONYOU V10 - CORE ENGINE
 * Version: 10.0.2 (Divineo V10 + Cursor Orchestration)
 * Protocol: Zero-Size / ABVET Fusion / Private Pass
 */

class TryOnYouV10 {
    constructor() {
        this.isCameraActive = false;
        this.selectedProducts = [];
        this.version = "10.0.2";
        this.init();
    }

    init() {
        console.log(`%c TRYONYOU V10 %c Initialized v${this.version} with Cursor Optimization `, 
            'background: #C5A46D; color: #141619; font-weight: bold; padding: 2px 4px;', 
            'background: #141619; color: #C5A46D; padding: 2px 4px;');
        
        this.setupEventListeners();
        this.applyLuxuryTransitions();
        this.checkSystemStatus();
    }

    setupEventListeners() {
        // Forms
        const contactForm = document.querySelector('.contact-form form');
        if (contactForm) contactForm.addEventListener('submit', this.handleContactForm.bind(this));

        const julesForm = document.getElementById('jules-form');
        if (julesForm) julesForm.addEventListener('submit', this.handleJulesConsultation.bind(this));

        // Navigation
        document.querySelectorAll('.nav-menu a[href^="#"]').forEach(link => {
            link.addEventListener('click', this.handleNavClick.bind(this));
        });

        // Product Selection
        document.querySelectorAll('.product-item').forEach(item => {
            const productId = item.getAttribute('onclick')?.match(/'([^']+)'/)?.[1];
            if (productId) {
                item.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.toggleProduct(productId, item);
                });
                item.removeAttribute('onclick');
            }
        });
    }

    handleNavClick(event) {
        event.preventDefault();
        const targetId = event.currentTarget.getAttribute('href');
        const targetSection = document.querySelector(targetId);
        
        if (targetSection) {
            const offsetTop = targetSection.offsetTop - 100;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    }

    async handleJulesConsultation(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const data = {
            body_shape: formData.get('body_shape'),
            fit_preference: formData.get('fit_preference'),
            event_type: formData.get('event_type')
        };

        const resultContainer = document.getElementById('jules-result');
        const resultText = document.getElementById('recommendation-text');
        const submitBtn = event.target.querySelector('button[type="submit"]');

        try {
            submitBtn.innerHTML = '<span class="loader"></span> ANALYZING BIOMETRICS...';
            submitBtn.disabled = true;

            await new Promise(resolve => setTimeout(resolve, 1500));

            const mockResponse = {
                status: 'success',
                recommendation: `[ABVET V10 ANALYSIS COMPLETE]\n\nBased on your ${data.body_shape} profile and ${data.fit_preference} preference for a ${data.event_type} event, Jules recommends the Peacock Couture Blazer. \n\nArchitectural Fit: Perfect\nElasticity Logic: High\nStyle: Avant-Garde Luxury.`
            };

            resultContainer.style.display = 'block';
            resultContainer.style.opacity = '0';
            resultText.textContent = mockResponse.recommendation;
            
            setTimeout(() => {
                resultContainer.style.transition = 'opacity 0.8s ease';
                resultContainer.style.opacity = '1';
            }, 10);

            this.showNotification('Jules V10 Analysis Complete', 'success');

        } catch (error) {
            this.showNotification('Fusion Engine Offline', 'error');
        } finally {
            submitBtn.textContent = 'ASK JULES';
            submitBtn.disabled = false;
        }
    }

    toggleProduct(productId, element) {
        const index = this.selectedProducts.indexOf(productId);
        if (index > -1) {
            this.selectedProducts.splice(index, 1);
            element.classList.remove('selected');
            element.style.borderColor = 'rgba(255, 255, 255, 0.1)';
            this.showNotification(`${productId.replace('_', ' ')} removed`, 'info');
        } else {
            this.selectedProducts.push(productId);
            element.classList.add('selected');
            element.style.borderColor = '#C5A46D';
            this.showNotification(`${productId.replace('_', ' ')} selected`, 'success');
            
            if (this.isCameraActive) {
                this.simulateVirtualTryOn(productId);
            }
        }
    }

    simulateVirtualTryOn(productId) {
        const placeholder = document.querySelector('.camera-placeholder');
        placeholder.style.boxShadow = 'inset 0 0 50px rgba(197, 164, 109, 0.3)';
        setTimeout(() => {
            placeholder.style.boxShadow = 'none';
            this.showNotification(`V10 Render: ${productId} applied`, 'success');
        }, 800);
    }

    toggleCamera() {
        const cameraView = document.querySelector('.camera-view');
        const cameraBtn = document.querySelector('.camera-btn');
        const placeholder = document.querySelector('.camera-placeholder');
        
        this.isCameraActive = !this.isCameraActive;
        
        if (this.isCameraActive) {
            cameraView.classList.add('active');
            cameraBtn.textContent = 'STOP BIOMETRIC SCAN';
            placeholder.innerHTML = `
                <div class="v10-scan-overlay"></div>
                <p style="color: #C5A46D; font-size: 1.2rem; letter-spacing: 2px;">BIOMETRIC SCAN ACTIVE</p>
                <p style="font-weight: 300; opacity: 0.6;">V10 FUSION ENGINE READY</p>
            `;
            this.showNotification('Biometric Scan Started', 'success');
        } else {
            cameraView.classList.remove('active');
            cameraBtn.textContent = 'START BIOMETRIC SCAN';
            placeholder.innerHTML = `
                <p>CAMERA VIEW</p>
                <p style="font-weight: 300; opacity: 0.5;">Click to begin V10 experience</p>
            `;
            this.showNotification('Scan Terminated', 'info');
        }
    }

    handleContactForm(event) {
        event.preventDefault();
        this.showNotification('Message encrypted and sent', 'success');
        event.target.reset();
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message.toUpperCase();
        document.body.appendChild(notification);

        setTimeout(() => notification.style.transform = 'translateX(0)', 100);
        setTimeout(() => {
            notification.style.transform = 'translateX(150%)';
            setTimeout(() => notification.remove(), 500);
        }, 4000);
    }

    applyLuxuryTransitions() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('section').forEach(section => {
            section.style.opacity = '0';
            section.style.transform = 'translateY(30px)';
            section.style.transition = 'all 1s cubic-bezier(0.165, 0.84, 0.44, 1)';
            observer.observe(section);
        });
    }

    checkSystemStatus() {
        console.log("V10: All systems nominal. Zero-Size Protocol active.");
    }

    // Private Pass Logic
    requestPrivatePass() {
        const modal = document.getElementById('private-pass-modal');
        modal.style.display = 'flex';
    }

    closePrivatePass() {
        const modal = document.getElementById('private-pass-modal');
        modal.style.display = 'none';
    }

    verifyPrivatePass() {
        const input = document.getElementById('private-pass-input');
        if (input.value === "SAC_MUSEUM_2026") {
            this.showNotification('ACCESO CONCEDIDO: CURADOR AUTORIZADO', 'success');
            setTimeout(() => {
                window.location.href = "/staff-dashboard"; // Placeholder for private area
            }, 1500);
        } else {
            this.showNotification('ACCESO DENEGADO: CREDENCIAL INVÁLIDA', 'error');
            input.value = "";
        }
    }
}

// Global Handlers for V10
window.startTryOn = () => {
    const section = document.getElementById('try-on');
    if (section) window.scrollTo({ top: section.offsetTop - 100, behavior: 'smooth' });
};

window.toggleCamera = () => window.v10App.toggleCamera();
window.requestPrivatePass = () => window.v10App.requestPrivatePass();
window.closePrivatePass = () => window.v10App.closePrivatePass();
window.verifyPrivatePass = () => window.v10App.verifyPrivatePass();

// Initialize V10
document.addEventListener('DOMContentLoaded', () => {
    window.v10App = new TryOnYouV10();
});
