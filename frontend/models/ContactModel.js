import FRONTEND_CONFIG from '../public/js/config.js';

export default class ContactModel {
    constructor() {
        this.contacts = [];
        this.isLoading = false;
        this.error = null;
    }

    async fetchContacts() {
        this.isLoading = true;
        this.error = null;

        try {
            console.log('Fetching contacts from API...');
            const apiUrl = window.location.hostname === 'localhost'
                ? 'http://localhost:8000/api/v1/nossocontato/'
                : '/api/v1/nossocontato/';
            console.log('Using contacts API URL:', apiUrl);
            const response = await fetch(apiUrl, {
                headers: {
                    'Accept': 'application/json'
                }
            });
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            console.log('Contacts data received:', data);
            // Mapeia os campos da API para o formato esperado pelo frontend
            this.contacts = data.map(item => ({
                slocal: item.local,
                stelefone: item.telefone,
                semail: item.email
            }));
            return data;
        } catch (error) {
            this.error = error.message;
            console.error('Error fetching contacts:', error);
            throw error;
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Get the current contacts data
     * @returns {Array|null} - The current contacts data
     */
    getContacts() {
        return this.contacts;
    }

    /**
     * Get a specific contact by ID
     * @param {number} id - The contact ID
     * @returns {Object|null} - The contact object or null if not found
     */
    getContactById(id) {
        if (!this.contacts) return null;
        return this.contacts.find(contact => contact.id === id) || null;
    }

    static async sendMessage(messageData) {
        try {
            const apiUrl = `${FRONTEND_CONFIG.API_BASE_URL}/api/v1/mensagem/`;
            console.log('Sending message to:', apiUrl);
            
            // Ensure all required fields are included
            const completeMessageData = {
                snome: messageData.snome || '',
                semail: messageData.semail,
                stelefone: messageData.stelefone,
                sassunto: messageData.sassunto,
                smensagem: messageData.smensagem
            };
            
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(completeMessageData)
            });
            
            console.log('Response status:', response.status);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('Error response:', errorText);
                throw new Error(`Erro ao enviar mensagem (${response.status})`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    }
}