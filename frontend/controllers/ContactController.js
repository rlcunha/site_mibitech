import ContactModel from '../models/ContactModel.js';

export default class ContactController {
    constructor() {
        this.model = new ContactModel();
        this.contactContainer = null;
        this.messageLog = null;
    }

    /**
     * Initialize the controller
     * @param {Object} options - Configuration options
     * @param {string} options.contactContainer - Selector for contact info container
     * @param {string} options.messageLog - Selector for message log container
     */
    init(options = {}) {
        if (options.contactContainer || options.contactsContainer) {
            this.contactContainer = document.querySelector(options.contactContainer || options.contactsContainer);
        }
        
        if (options.messageLog) {
            this.messageLog = document.querySelector(options.messageLog);
        }

        if (this.contactContainer) {
            this.loadContacts();
        }
    }

    /**
     * Load contacts from API
     */
    async loadContacts() {
        if (!this.contactContainer) {
            console.warn('Contact container not found');
            return;
        }

        try {
            console.log('Loading contacts...');
            const contacts = await this.model.fetchContacts();
            console.log('Contacts loaded:', contacts);
            this.renderContacts(contacts);
        } catch (error) {
            console.error('Error loading contacts:', error);
            this.renderContactsError(error);
        }
    }

    /**
     * Render contacts in the container
     * @param {Array} contacts - Array of contact objects
     */
    renderContacts(contacts) {
        if (!this.contactContainer) {
            console.warn('Contact container not found for rendering');
            return;
        }

        if (!contacts || contacts.length === 0) {
            console.warn('No contacts data to render');
            this.contactContainer.innerHTML = '<p class="text-gray-500">Nenhum contato disponível</p>';
            return;
        }

        console.log('Rendering contacts:', contacts);
        
        // Criar um container para todos os contatos em layout horizontal
        let contactsHTML = '<div class="flex flex-wrap gap-4 justify-center">';
        
        // Iterar sobre todos os contatos
        contacts.forEach(contact => {
            // Verificar se estamos usando os dados mapeados do modelo ou os dados brutos da API
            const local = contact.slocal || contact.local || 'Não informado';
            const telefone = contact.stelefone || contact.telefone || 'Não informado';
            const email = contact.semail || contact.email || 'Não informado';
            const titulo = contact.stipo || contact.tipo || 'Contato';
            
            // Adicionar o card de contato ao HTML com estilos modernos
            contactsHTML += `
                <div class="contact-info-card p-6 space-y-4 flex-shrink-0" style="min-width: 280px; max-width: 350px;">
                    <h3 class="text-xl font-bold text-blue-700 mb-4">${titulo}</h3>
                    <div class="flex items-start space-x-4">
                        <i class="fas fa-map-marker-alt"></i>
                        <div>
                            <h4 class="font-bold text-gray-800">Endereço</h4>
                            <p class="text-gray-600">${local}</p>
                        </div>
                    </div>
                    <div class="flex items-start space-x-4">
                        <i class="fas fa-phone-alt"></i>
                        <div>
                            <h4 class="font-bold text-gray-800">Telefone</h4>
                            <p class="text-gray-600">${telefone}</p>
                        </div>
                    </div>
                    <div class="flex items-start space-x-4">
                        <i class="fas fa-envelope"></i>
                        <div>
                            <h4 class="font-bold text-gray-800">E-mail</h4>
                            <p class="text-gray-600">${email}</p>
                        </div>
                    </div>
                </div>
            `;
        });
        
        // Fechar o container
        contactsHTML += '</div>';
        
        // Atualizar o HTML do container
        this.contactContainer.innerHTML = contactsHTML;
        console.log('Contact info rendered successfully');
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
     * Send message through API
     * @param {Object} messageData - Message data
     * @returns {Promise} Promise with the result
     */
    static async sendMessage(messageData) {
        try {
            console.log('Sending message with data:', messageData);
            const result = await ContactModel.sendMessage(messageData);
            console.log('Message sent successfully:', result);
            return result;
        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    }
}