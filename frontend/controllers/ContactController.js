import ContactModel from '../models/ContactModel.js';

export default class ContactController {
    constructor() {
        this.model = new ContactModel();
        this.contactContainer = null;
        this.messageForm = null;
        this.messageLog = null;
    }

    /**
     * Initialize the controller
     * @param {Object} options - Configuration options
     * @param {string} options.contactContainer - Selector for contact info container
     * @param {string} options.messageForm - Selector for message form
     * @param {string} options.messageLog - Selector for message log container
     */
    init(options = {}) {
        console.log('ContactController.init() called with options:', options);
        
        if (options.contactContainer) {
            this.contactContainer = document.querySelector(options.contactContainer);
            console.log('Contact container found:', this.contactContainer);
            this.loadContacts();
        } else {
            console.warn('Contact container selector not provided');
        }

        if (options.messageForm) {
            this.messageForm = document.querySelector(options.messageForm);
            this.setupMessageForm();
        }

        if (options.messageLog) {
            this.messageLog = document.querySelector(options.messageLog);
        }
        
        // Ensure contacts are loaded even if init is called without options
        if (!options.contactContainer && document.querySelector('.contact-info-container')) {
            this.contactContainer = document.querySelector('.contact-info-container');
            console.log('Contact container found by default selector');
            this.loadContacts();
        }
    }

    /**
     * Load contacts from API
     */
    async loadContacts() {
        if (!this.contactContainer) {
            // Try to find container again
            this.contactContainer = document.querySelector('.contact-info-container');
            if (!this.contactContainer) {
                console.error('Contact container not found after retry');
                return;
            }
            console.log('Found contact container on retry');
        }

        console.log('Loading contacts from API...');
        try {
            const contacts = await this.model.fetchContacts();
            console.log('Contacts loaded successfully:', contacts);
            this.renderContacts(contacts);
        } catch (error) {
            console.error('Error loading contacts:', error);
            this.renderContactsError(error);
            
            // Try again after 5 seconds
            setTimeout(() => {
                console.log('Retrying contacts load...');
                this.loadContacts();
            }, 5000);
        }
    }

    /**
     * Render contacts in the container
     * @param {Array} contacts - Array of contact objects
     */
    renderContacts(contacts) {
        if (!this.contactContainer || !contacts?.length) {
            this.contactContainer.innerHTML = '<p class="text-gray-500">Nenhum contato disponível</p>';
            return;
        }

        const contactsHTML = `
            <div class="flex flex-wrap gap-4 justify-center">
                ${contacts.map(contact => `
                    <div class="contact-info-card p-6 space-y-4 flex-shrink-0" style="min-width: 280px; max-width: 350px;">
                        <h3 class="text-xl font-bold text-blue-700 mb-4">${contact.stipo || 'Contato'}</h3>
                        <div class="flex items-start space-x-4">
                            <i class="fas fa-map-marker-alt"></i>
                            <div>
                                <h4 class="font-bold text-gray-800">Endereço</h4>
                                <p class="text-gray-600">${contact.slocal || 'Não informado'}</p>
                            </div>
                        </div>
                        <div class="flex items-start space-x-4">
                            <i class="fas fa-phone-alt"></i>
                            <div>
                                <h4 class="font-bold text-gray-800">Telefone</h4>
                                <p class="text-gray-600">${contact.stelefone || 'Não informado'}</p>
                            </div>
                        </div>
                        <div class="flex items-start space-x-4">
                            <i class="fas fa-envelope"></i>
                            <div>
                                <h4 class="font-bold text-gray-800">E-mail</h4>
                                <p class="text-gray-600">${contact.semail || 'Não informado'}</p>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;

        this.contactContainer.innerHTML = contactsHTML;
    }

    /**
     * Render error message for contacts
     * @param {Error} error - Error object
     */
    renderContactsError(error) {
        if (!this.contactContainer) return;
        
        this.contactContainer.innerHTML = `
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                <p>Não foi possível carregar as informações de contato</p>
                ${error.message ? `<p class="text-sm mt-1">${error.message}</p>` : ''}
            </div>
        `;
    }

    /**
     * Setup message form submission
     */
    setupMessageForm() {
        if (!this.messageForm) return;

        this.messageForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(this.messageForm);
            const messageData = {
                snome: formData.get('name'),
                semail: formData.get('email'),
                stelefone: formData.get('phone'),
                sassunto: formData.get('subject'),
                smensagem: formData.get('message')
            };

            // Validação dos campos
            if (!messageData.snome || messageData.snome.trim() === '') {
                this.showMessageError('Por favor, preencha seu nome');
                console.error('Validation error: Nome não preenchido');
                return;
            }

            if (!messageData.semail || messageData.semail.trim() === '') {
                this.showMessageError('Por favor, preencha seu e-mail');
                console.error('Validation error: E-mail não preenchido');
                return;
            }

            if (!messageData.smensagem || messageData.smensagem.trim() === '') {
                this.showMessageError('Por favor, preencha sua mensagem');
                console.error('Validation error: Mensagem não preenchida');
                return;
            }

            console.log('Enviando mensagem com dados:', messageData);

            try {
                const result = await this.model.sendMessage(messageData);
                console.log('Mensagem enviada com sucesso:', result);
                this.showMessageSuccess('Mensagem enviada com sucesso!');
                this.messageForm.reset();
            } catch (error) {
                console.error('Erro ao enviar mensagem:', error);
                this.showMessageError('Erro ao enviar mensagem: ' + error.message);
            }
        });
    }

    /**
     * Show success message
     * @param {string} message - Success message
     */
    showMessageSuccess(message) {
        if (!this.messageLog) return;
        
        this.messageLog.innerHTML = `
            <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
                ${message}
            </div>
        `;
    }

    /**
     * Show error message
     * @param {string} message - Error message
     */
    showMessageError(message) {
        if (!this.messageLog) return;
        
        this.messageLog.innerHTML = `
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                ${message}
            </div>
        `;
    }
}