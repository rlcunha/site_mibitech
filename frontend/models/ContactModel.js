import DataModel from './DataModel.js';

export default class ContactModel extends DataModel {
    constructor() {
        super();
        this.contacts = [];
    }

    async fetchContacts() {
        this.isLoading = true;
        this.error = null;

        try {
            console.log('Fetching contacts from API...');
            const data = await this.fetchData('api/v1/nossocontato');
            console.log('API response:', data);
            
            if (!Array.isArray(data)) {
                console.error('Invalid API response format - expected array');
                throw new Error('Invalid response format from API');
            }

            // Mapeia os campos da API para o formato esperado pelo frontend
            this.contacts = data.map(item => ({
                id: item.id,
                stipo: item.tipo || 'Contato',
                slocal: item.local || 'Não informado',
                stelefone: item.telefone || 'Não informado',
                semail: item.email || 'Não informado',
                created_at: item.created_at,
                updated_at: item.updated_at
            }));

            console.log('Mapped contacts:', this.contacts);
            return this.contacts;
        } catch (error) {
            this.error = error.message;
            console.error('Error fetching contacts:', error);
            throw error;
        } finally {
            this.isLoading = false;
        }
    }

    getContacts() {
        return this.contacts;
    }

    getContactById(id) {
        if (!this.contacts) return null;
        return this.contacts.find(contact => contact.id === id) || null;
    }

    async sendMessage(messageData) {
        this.isLoading = true;
        this.error = null;

        try {
            const completeMessageData = {
                snome: messageData.snome || '',
                semail: messageData.semail,
                stelefone: messageData.stelefone,
                sassunto: messageData.sassunto,
                smensagem: messageData.smensagem
            };
            
            const response = await this.postData('api/v1/mensagem', completeMessageData);
            return response;
        } catch (error) {
            this.error = error.message;
            console.error('Error sending message:', error);
            throw error;
        } finally {
            this.isLoading = false;
        }
    }
}