/**
 * MibiTech Website JavaScript
 * This file contains all the interactive functionality for the MibiTech website
 */

// Import controllers
import CompanyController from '../../controllers/CompanyController.js';
import ContactController from '../../controllers/ContactController.js';

document.addEventListener('DOMContentLoaded', function() {
    console.log("MibiTech application initialized");
    // Initialize all components
    initializeNavigation();
    initializeAnimations();
    initializePortfolioFilter();
    initializeFAQAccordion();
    initializeContactForm();
    initializeScrollToTop();
    initializeMobileMenu();
    initializeCompanyInfo();
    initializeContactInfo();
});

/**
 * Initialize company information from API
 */
function initializeCompanyInfo() {
    console.log("Initializing company information");
    try {
        const companyController = new CompanyController();
        companyController.init({
            socialMediaContainer: '.social-media-container',
            footerSocialContainer: '.footer-social-container'
        });
    } catch (error) {
        console.error("Error initializing company information:", error);
    }
}

/**
 * Initialize contact information from API
 */
function initializeContactInfo() {
    console.log("Initializing contact information");
    try {
        const contactController = new ContactController();
        contactController.init({
            contactsContainer: '.contact-info-container'
        });
    } catch (error) {
        console.error("Error initializing contact information:", error);
    }
}

/**
 * Navigation functionality
 * Handles sticky header and active link highlighting
 */
function initializeNavigation() {
    const header = document.querySelector('header');
    const navLinks = document.querySelectorAll('nav a');
    
    // Sticky header on scroll
    if (header) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 100) {
                header.classList.add('bg-white', 'shadow-md', 'py-2');
                header.classList.remove('py-3');
            } else {
                header.classList.remove('bg-white', 'shadow-md', 'py-2');
                header.classList.add('py-3');
            }
        });
    }
    
    // Add active class to current page link
    if (navLinks.length > 0) {
        const currentPage = window.location.pathname.split('/').pop();
        
        navLinks.forEach(link => {
            const linkPage = link.getAttribute('href');
            if (linkPage === currentPage) {
                link.classList.add('text-blue-600', 'border-b-2', 'border-blue-600');
                link.classList.remove('text-gray-600');
            }
        });
    }
}

/**
 * Animation functionality
 * Adds scroll-triggered animations to elements
 */
function initializeAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    if (animatedElements.length > 0) {
        // Create intersection observer
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    const animation = element.dataset.animation || 'fade-in';
                    element.classList.add(animation);
                    observer.unobserve(element);
                }
            });
        }, {
            threshold: 0.1
        });
        
        // Observe all elements with animation classes
        animatedElements.forEach(element => {
            observer.observe(element);
        });
    }
}

/**
 * Portfolio filter functionality
 * Handles filtering of portfolio items by category
 */
function initializePortfolioFilter() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    
    if (filterButtons.length > 0 && portfolioItems.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Remove active class from all buttons
                filterButtons.forEach(btn => {
                    btn.classList.remove('active', 'bg-blue-600', 'text-white');
                    btn.classList.add('bg-gray-200', 'text-gray-700');
                });
                
                // Add active class to clicked button
                this.classList.add('active', 'bg-blue-600', 'text-white');
                this.classList.remove('bg-gray-200', 'text-gray-700');
                
                const filterValue = this.getAttribute('data-filter');
                
                // Show/hide portfolio items based on filter
                portfolioItems.forEach(item => {
                    if (filterValue === 'all' || item.getAttribute('data-category') === filterValue) {
                        item.style.display = 'block';
                        setTimeout(() => {
                            item.style.opacity = '1';
                            item.style.transform = 'scale(1)';
                        }, 50);
                    } else {
                        item.style.opacity = '0';
                        item.style.transform = 'scale(0.95)';
                        setTimeout(() => {
                            item.style.display = 'none';
                        }, 300);
                    }
                });
            });
        });
    }
}

/**
 * FAQ Accordion functionality
 * Handles expanding/collapsing of FAQ items
 */
function initializeFAQAccordion() {
    const faqToggles = document.querySelectorAll('.faq-toggle');
    
    if (faqToggles.length > 0) {
        faqToggles.forEach(toggle => {
            toggle.addEventListener('click', function() {
                const content = this.nextElementSibling;
                const icon = this.querySelector('i');
                
                // Toggle aria-expanded attribute
                const expanded = this.getAttribute('aria-expanded') === 'true' || false;
                this.setAttribute('aria-expanded', !expanded);
                
                // Toggle content visibility
                if (content.style.maxHeight) {
                    content.style.maxHeight = null;
                    content.classList.add('hidden');
                    icon.classList.remove('transform', 'rotate-180');
                } else {
                    content.classList.remove('hidden');
                    content.style.maxHeight = content.scrollHeight + 'px';
                    icon.classList.add('transform', 'rotate-180');
                }
            });
        });
    }
}

/**
 * Contact Form functionality
 * Handles form validation and submission with enhanced user feedback
 */
function initializeContactForm() {
    const contactForm = document.getElementById('contactForm');
    const formInputs = contactForm ? contactForm.querySelectorAll('input, textarea') : [];
    
    // Add input validation and visual feedback
    formInputs.forEach(input => {
        // Add focus and blur events for visual feedback
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('ring-2', 'ring-blue-200', 'ring-opacity-50');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('ring-2', 'ring-blue-200', 'ring-opacity-50');
            validateInput(this);
        });
        
        // Add input event for real-time validation
        input.addEventListener('input', function() {
            if (this.classList.contains('error')) {
                validateInput(this);
            }
        });
    });
    
    // Validate individual input
    function validateInput(input) {
        const errorClass = 'error';
        let isValid = true;
        
        // Remove existing error message
        const existingError = input.parentElement.nextElementSibling;
        if (existingError && existingError.classList.contains('text-red-500')) {
            existingError.remove();
        }
        
        // Check validation based on input type
        if (input.required && !input.value.trim()) {
            isValid = false;
            showError(input, 'Este campo é obrigatório');
        } else if (input.type === 'email' && input.value.trim()) {
            if (!isValidEmail(input.value.trim())) {
                isValid = false;
                showError(input, 'Por favor, insira um e-mail válido');
            }
        }
    }
    
    // Show error message for input
    function showError(input, message) {
        input.classList.add('error', 'border-red-500');
        
        // Create error message element
        const errorElement = document.createElement('p');
        errorElement.className = 'text-red-500 text-sm mt-1';
        errorElement.textContent = message;
        
        // Add error message after input's parent element
        input.parentElement.after(errorElement);
    }
    
    const messageLog = document.getElementById('messageLog');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Basic form validation
            let isValid = true;
            const requiredFields = contactForm.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('border-red-500');
                    
                    // Add error message if it doesn't exist
                    let errorMessage = field.nextElementSibling;
                    if (!errorMessage || !errorMessage.classList.contains('error-message')) {
                        errorMessage = document.createElement('p');
                        errorMessage.classList.add('error-message', 'text-red-500', 'text-sm', 'mt-1');
                        errorMessage.textContent = 'Este campo é obrigatório';
                        field.parentNode.insertBefore(errorMessage, field.nextSibling);
                    }
                } else {
                    field.classList.remove('border-red-500');
                    
                    // Remove error message if it exists
                    const errorMessage = field.nextElementSibling;
                    if (errorMessage && errorMessage.classList.contains('error-message')) {
                        errorMessage.remove();
                    }
                    
                    // Email validation
                    if (field.type === 'email' && !isValidEmail(field.value)) {
                        isValid = false;
                        field.classList.add('border-red-500');
                        
                        let errorMessage = field.nextElementSibling;
                        if (!errorMessage || !errorMessage.classList.contains('error-message')) {
                            errorMessage = document.createElement('p');
                            errorMessage.classList.add('error-message', 'text-red-500', 'text-sm', 'mt-1');
                            errorMessage.textContent = 'Por favor, insira um e-mail válido';
                            field.parentNode.insertBefore(errorMessage, field.nextSibling);
                        }
                    }
                }
            });
            
            if (isValid) {
                // Prepare form data for API
                const messageData = {
                    snome: contactForm.querySelector('#name').value,
                    semail: contactForm.querySelector('#email').value,
                    stelefone: contactForm.querySelector('#phone').value,
                    sassunto: contactForm.querySelector('#subject').value,
                    smensagem: contactForm.querySelector('#message').value
                };
                
                // Get submit button and change its state
                const submitButton = contactForm.querySelector('button[type="submit"]');
                const originalText = submitButton.textContent;
                
                submitButton.disabled = true;
                submitButton.textContent = 'Enviando...';
                
                // Send message using ContactController
                ContactController.sendMessage(messageData)
                    .then(response => {
                        console.log('Mensagem enviada com sucesso:', response);
                        
                        // Reset form
                        contactForm.reset();
                        
                        // Show success message
                        if (messageLog) {
                            messageLog.innerHTML = '';
                            const successMsg = document.createElement('div');
                            successMsg.className = 'bg-green-100 border border-green-400 text-green-700 p-4 rounded';
                            successMsg.innerHTML = `
                                <strong class="font-bold">✓ Mensagem enviada com sucesso!</strong>
                                <p class="text-sm mt-2">Agradecemos seu contato. Retornaremos em breve.</p>
                            `;
                            messageLog.appendChild(successMsg);
                        }
                    })
                    .catch(error => {
                        console.error('Erro ao enviar mensagem:', error);
                        
                        // Show error message
                        if (messageLog) {
                            messageLog.innerHTML = '';
                            const errorMsg = document.createElement('div');
                            errorMsg.className = 'bg-red-100 border border-red-400 text-red-700 p-4 rounded';
                            errorMsg.innerHTML = `
                                <strong class="font-bold">Erro ao enviar mensagem</strong>
                                <p class="text-sm mt-2">${error.message || 'Ocorreu um erro ao processar sua solicitação. Por favor, tente novamente mais tarde.'}</p>
                            `;
                            messageLog.appendChild(errorMsg);
                        }
                    })
                    .finally(() => {
                        // Re-enable button
                        submitButton.disabled = false;
                        submitButton.textContent = originalText;
                    });
            }
        });
        
        // Remove validation styling on input
        const formInputs = contactForm.querySelectorAll('input, textarea');
        formInputs.forEach(input => {
            input.addEventListener('input', function() {
                this.classList.remove('border-red-500');
                
                // Remove error message if it exists
                const errorMessage = this.nextElementSibling;
                if (errorMessage && errorMessage.classList.contains('error-message')) {
                    errorMessage.remove();
                }
            });
        });
    }
}

/**
 * Scroll to Top functionality
 * Adds a button to scroll back to the top of the page
 */
function initializeScrollToTop() {
    // Create scroll to top button if it doesn't exist
    let scrollToTopBtn = document.getElementById('scrollToTopBtn');
    
    if (!scrollToTopBtn) {
        scrollToTopBtn = document.createElement('button');
        scrollToTopBtn.id = 'scrollToTopBtn';
        scrollToTopBtn.className = 'fixed bottom-6 right-6 bg-blue-600 text-white rounded-full p-3 shadow-lg opacity-0 transition-opacity duration-300 hover:bg-blue-700 focus:outline-none';
        scrollToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
        scrollToTopBtn.setAttribute('aria-label', 'Voltar ao topo');
        document.body.appendChild(scrollToTopBtn);
        
        // Show/hide button based on scroll position
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                scrollToTopBtn.classList.remove('opacity-0');
                scrollToTopBtn.classList.add('opacity-100');
            } else {
                scrollToTopBtn.classList.remove('opacity-100');
                scrollToTopBtn.classList.add('opacity-0');
            }
        });
        
        // Scroll to top when button is clicked
        scrollToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

/**
 * Mobile Menu functionality
 * Handles toggling of mobile navigation menu
 */
function initializeMobileMenu() {
    // Check if mobile menu toggle exists
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
            
            // Toggle aria-expanded attribute
            const expanded = mobileMenuToggle.getAttribute('aria-expanded') === 'true' || false;
            mobileMenuToggle.setAttribute('aria-expanded', !expanded);
            
            // Toggle icon
            const icon = mobileMenuToggle.querySelector('i');
            if (icon) {
                if (expanded) {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                } else {
                    icon.classList.remove('fa-bars');
                    icon.classList.add('fa-times');
                }
            }
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!mobileMenu.contains(event.target) && !mobileMenuToggle.contains(event.target) && !mobileMenu.classList.contains('hidden')) {
                mobileMenu.classList.add('hidden');
                mobileMenuToggle.setAttribute('aria-expanded', 'false');
                
                // Reset icon
                const icon = mobileMenuToggle.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });
    }
}

/**
 * Helper function to validate email format
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Helper function to format date
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', options);
}

/**
 * Helper function to truncate text
 */
function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
}

/**
 * Helper function to generate random ID
 */
function generateId(prefix = 'id') {
    return `${prefix}-${Math.random().toString(36).substr(2, 9)}`;
}