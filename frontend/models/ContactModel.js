/**
 * ContactModel.js
 * Model for handling contact form data and submissions
 */

import DataModel from './DataModel.js';

class ContactModel extends DataModel {
    constructor() {
        super();
        this.formData = {
            name: '',
            email: '',
            phone: '',
            company: '',
            subject: '',
            message: '',
            privacy: false
        };
        this.formErrors = {};
        this.submitStatus = null; // 'success', 'error', or null
    }

    /**
     * Set a form field value
     * @param {string} field - The field name
     * @param {string|boolean} value - The field value
     */
    setField(field, value) {
        if (field in this.formData) {
            this.formData[field] = value;
        }
    }

    /**
     * Get the current form data
     * @returns {Object} - The current form data
     */
    getFormData() {
        return this.formData;
    }

    /**
     * Validate the form data
     * @returns {boolean} - True if valid, false otherwise
     */
    validateForm() {
        this.formErrors = {};
        let isValid = true;

        // Validate name
        if (!this.formData.name.trim()) {
            this.formErrors.name = 'Nome é obrigatório';
            isValid = false;
        }

        // Validate email
        if (!this.formData.email.trim()) {
            this.formErrors.email = 'E-mail é obrigatório';
            isValid = false;
        } else if (!this.isValidEmail(this.formData.email)) {
            this.formErrors.email = 'E-mail inválido';
            isValid = false;
        }

        // Validate subject
        if (!this.formData.subject.trim()) {
            this.formErrors.subject = 'Assunto é obrigatório';
            isValid = false;
        }

        // Validate message
        if (!this.formData.message.trim()) {
            this.formErrors.message = 'Mensagem é obrigatória';
            isValid = false;
        }

        // Validate privacy checkbox
        if (!this.formData.privacy) {
            this.formErrors.privacy = 'Você deve concordar com a política de privacidade';
            isValid = false;
        }

        return isValid;
    }

    /**
     * Get the current form errors
     * @returns {Object} - The current form errors
     */
    getFormErrors() {
        return this.formErrors;
    }

    /**
     * Submit the contact form
     * @returns {Promise} - Promise resolving to the submission result
     */
    async submitForm() {
        if (!this.validateForm()) {
            this.submitStatus = 'error';
            return { success: false, errors: this.formErrors };
        }

        try {
            // Use the API endpoint
            const response = await this.postData('https://apirest.mibitech.com.br/api/submit-contact/', this.formData);
            
            this.submitStatus = 'success';
            return response;
        } catch (error) {
            this.submitStatus = 'error';
            return {
                success: false,
                message: 'Ocorreu um erro ao enviar sua mensagem. Por favor, tente novamente.'
            };
        }
    }

    /**
     * Get the current submission status
     * @returns {string|null} - The current submission status
     */
    getSubmitStatus() {
        return this.submitStatus;
    }

    /**
     * Reset the form data and errors
     */
    resetForm() {
        this.formData = {
            name: '',
            email: '',
            phone: '',
            company: '',
            subject: '',
            message: '',
            privacy: false
        };
        this.formErrors = {};
        this.submitStatus = null;
    }

    /**
     * Helper method to validate email format
     * @param {string} email - The email to validate
     * @returns {boolean} - True if valid, false otherwise
     */
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
}

export default ContactModel;