/**
 * ContactController.js
 * Controller for handling contact form interactions
 */

import ContactModel from '../models/ContactModel.js';

class ContactController {
    constructor() {
        this.model = new ContactModel();
        this.form = null;
        this.formElements = {};
        this.submitButton = null;
        this.formContainer = null;
        this.successMessage = null;
        this.errorMessage = null;
        
        // Bind methods to this instance
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleInput = this.handleInput.bind(this);
    }

    /**
     * Initialize the controller
     * @param {string} formId - The ID of the contact form
     */
    init(formId = 'contactForm') {
        // Get form elements
        this.form = document.getElementById(formId);
        
        if (!this.form) {
            console.error(`Contact form with ID "${formId}" not found.`);
            return;
        }
        
        this.formContainer = this.form.parentElement;
        
        // Get form input elements
        this.formElements = {
            name: this.form.querySelector('#name'),
            email: this.form.querySelector('#email'),
            phone: this.form.querySelector('#phone'),
            company: this.form.querySelector('#company'),
            subject: this.form.querySelector('#subject'),
            message: this.form.querySelector('#message'),
            privacy: this.form.querySelector('#privacy')
        };
        
        this.submitButton = this.form.querySelector('button[type="submit"]');
        
        // Create success and error message elements
        this.createMessageElements();
        
        // Add event listeners
        this.form.addEventListener('submit', this.handleSubmit);
        
        // Add input event listeners to form elements
        Object.entries(this.formElements).forEach(([field, element]) => {
            if (element) {
                if (field === 'privacy') {
                    element.addEventListener('change', () => this.handleInput(field, element.checked));
                } else {
                    element.addEventListener('input', () => this.handleInput(field, element.value));
                }
            }
        });
    }

    /**
     * Create success and error message elements
     */
    createMessageElements() {
        // Create success message element
        this.successMessage = document.createElement('div');
        this.successMessage.className = 'bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative mb-6 hidden';
        this.successMessage.setAttribute('role', 'alert');
        this.successMessage.innerHTML = `
            <strong class="font-bold">Mensagem enviada com sucesso!</strong>
            <p class="block sm:inline">Agradecemos seu contato. Retornaremos em breve.</p>
        `;
        
        // Create error message element
        this.errorMessage = document.createElement('div');
        this.errorMessage.className = 'bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-6 hidden';
        this.errorMessage.setAttribute('role', 'alert');
        this.errorMessage.innerHTML = `
            <strong class="font-bold">Erro ao enviar mensagem!</strong>
            <p class="block sm:inline">Por favor, verifique os campos e tente novamente.</p>
        `;
        
        // Insert messages before the form
        this.formContainer.insertBefore(this.successMessage, this.form);
        this.formContainer.insertBefore(this.errorMessage, this.form);
    }

    /**
     * Handle form submission
     * @param {Event} event - The submit event
     */
    async handleSubmit(event) {
        event.preventDefault();
        
        // Update model with form data
        Object.entries(this.formElements).forEach(([field, element]) => {
            if (element) {
                const value = field === 'privacy' ? element.checked : element.value;
                this.model.setField(field, value);
            }
        });
        
        // Validate form
        if (!this.model.validateForm()) {
            this.displayErrors();
            this.showErrorMessage('Por favor, corrija os erros no formulário.');
            return;
        }
        
        // Disable submit button and show loading state
        this.setSubmitButtonLoading(true);
        
        try {
            // Submit form
            const result = await this.model.submitForm();
            
            if (result.success) {
                this.showSuccessMessage(result.message);
                this.resetForm();
            } else {
                this.showErrorMessage(result.message);
            }
        } catch (error) {
            this.showErrorMessage('Ocorreu um erro ao enviar sua mensagem. Por favor, tente novamente.');
            console.error('Error submitting form:', error);
        } finally {
            this.setSubmitButtonLoading(false);
        }
    }

    /**
     * Handle input changes
     * @param {string} field - The field name
     * @param {string|boolean} value - The field value
     */
    handleInput(field, value) {
        // Update model with the new value
        this.model.setField(field, value);
        
        // Clear error for this field
        this.clearFieldError(field);
        
        // Hide error message
        this.hideErrorMessage();
    }

    /**
     * Display form validation errors
     */
    displayErrors() {
        const errors = this.model.getFormErrors();
        
        Object.entries(errors).forEach(([field, errorMessage]) => {
            const element = this.formElements[field];
            
            if (element) {
                // Add error class to the element
                element.classList.add('border-red-500');
                
                // Add error message
                let errorElement = element.nextElementSibling;
                
                if (!errorElement || !errorElement.classList.contains('error-message')) {
                    errorElement = document.createElement('p');
                    errorElement.className = 'error-message text-red-500 text-sm mt-1';
                    element.parentNode.insertBefore(errorElement, element.nextSibling);
                }
                
                errorElement.textContent = errorMessage;
            }
        });
    }

    /**
     * Clear error for a specific field
     * @param {string} field - The field name
     */
    clearFieldError(field) {
        const element = this.formElements[field];
        
        if (element) {
            // Remove error class
            element.classList.remove('border-red-500');
            
            // Remove error message
            const errorElement = element.nextElementSibling;
            
            if (errorElement && errorElement.classList.contains('error-message')) {
                errorElement.remove();
            }
        }
    }

    /**
     * Show success message
     * @param {string} message - The success message
     */
    showSuccessMessage(message) {
        // Hide error message
        this.hideErrorMessage();
        
        // Update success message text if provided
        if (message) {
            const messageElement = this.successMessage.querySelector('p');
            
            if (messageElement) {
                messageElement.textContent = message;
            }
        }
        
        // Show success message
        this.successMessage.classList.remove('hidden');
        
        // Hide form
        this.form.classList.add('hidden');
        
        // Scroll to success message
        this.successMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    /**
     * Show error message
     * @param {string} message - The error message
     */
    showErrorMessage(message) {
        // Update error message text if provided
        if (message) {
            const messageElement = this.errorMessage.querySelector('p');
            
            if (messageElement) {
                messageElement.textContent = message;
            }
        }
        
        // Show error message
        this.errorMessage.classList.remove('hidden');
        
        // Scroll to error message
        this.errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    /**
     * Hide error message
     */
    hideErrorMessage() {
        this.errorMessage.classList.add('hidden');
    }

    /**
     * Set submit button loading state
     * @param {boolean} isLoading - Whether the button is in loading state
     */
    setSubmitButtonLoading(isLoading) {
        if (this.submitButton) {
            if (isLoading) {
                this.submitButton.disabled = true;
                this.submitButton.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Enviando...';
            } else {
                this.submitButton.disabled = false;
                this.submitButton.innerHTML = 'Enviar Mensagem';
            }
        }
    }

    /**
     * Reset the form
     */
    resetForm() {
        // Reset model
        this.model.resetForm();
        
        // Reset form element
        this.form.reset();
        
        // Clear all field errors
        Object.keys(this.formElements).forEach(field => {
            this.clearFieldError(field);
        });
    }
}

export default ContactController;