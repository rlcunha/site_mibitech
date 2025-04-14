import CompanyModel from '../models/CompanyModel.js';
import ContactModel from '../models/ContactModel.js';
import FRONTEND_CONFIG from './config.test.js';

async function runTests() {
    console.log('Iniciando testes dos modelos...');
    console.log('URL Base:', FRONTEND_CONFIG.API_BASE_URL);

    // Teste do CompanyModel
    console.log('\n=== Testando CompanyModel ===');
    const companyModel = new CompanyModel();
    
    try {
        console.log('Buscando redes sociais...');
        const socialMedia = await companyModel.fetchSocialMedia();
        console.log('Redes sociais obtidas:', socialMedia);
        
        if (socialMedia && socialMedia.length > 0) {
            console.log('Teste de getSocialMediaById...');
            const firstItem = companyModel.getSocialMediaById(socialMedia[0].id);
            console.log('Primeiro item:', firstItem);
        }
    } catch (error) {
        console.error('Erro no CompanyModel:', error);
    }

    // Teste do ContactModel
    console.log('\n=== Testando ContactModel ===');
    const contactModel = new ContactModel();
    
    try {
        console.log('Buscando contatos...');
        const contacts = await contactModel.fetchContacts();
        console.log('Contatos obtidos:', contacts);
        
        if (contacts && contacts.length > 0) {
            console.log('Teste de getContactById...');
            const firstContact = contactModel.getContactById(contacts[0].id);
            console.log('Primeiro contato:', firstContact);
        }
    } catch (error) {
        console.error('Erro no ContactModel:', error);
    }

    // Teste de envio de mensagem
    try {
        console.log('\nTestando envio de mensagem...');
        const messageData = {
            snome: 'Teste',
            semail: 'teste@example.com',
            stelefone: '11999999999',
            sassunto: 'Teste de mensagem',
            smensagem: 'Esta é uma mensagem de teste'
        };
        const result = await contactModel.sendMessage(messageData);
        console.log('Mensagem enviada com sucesso:', result);
    } catch (error) {
        console.error('Erro ao enviar mensagem:', error);
    }

    console.log('\nTestes concluídos!');
}

runTests();