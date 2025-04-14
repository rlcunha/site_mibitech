/**
 * model_test.js
 * Testes para verificar a propagação de dados da camada model para controllers e views
 */

import CompanyModel from '../models/CompanyModel.js';
import ContactModel from '../models/ContactModel.js';
import PortfolioModel from '../models/PortfolioModel.js';
import FRONTEND_CONFIG from './config.test.js';

// Mock para o DOM
class MockElement {
    constructor() {
        this.innerHTML = '';
        this.children = [];
        this.classList = {
            add: () => {},
            remove: () => {},
            contains: () => false
        };
        this.style = {};
        this.attributes = {};
    }

    querySelector(selector) {
        return new MockElement();
    }

    querySelectorAll(selector) {
        return [new MockElement()];
    }

    getAttribute(name) {
        return this.attributes[name] || null;
    }

    setAttribute(name, value) {
        this.attributes[name] = value;
    }

    addEventListener(event, callback) {
        // Armazena o callback para poder testá-lo
        this.eventListeners = this.eventListeners || {};
        this.eventListeners[event] = this.eventListeners[event] || [];
        this.eventListeners[event].push(callback);
    }

    appendChild(child) {
        this.children.push(child);
    }
}

// Mock para o document
global.document = {
    getElementById: (id) => new MockElement(),
    querySelector: (selector) => new MockElement(),
    querySelectorAll: (selector) => [new MockElement()],
    createElement: (tag) => new MockElement()
};

// Mock para o console
const originalConsole = console;
let consoleOutput = [];
global.console = {
    log: (...args) => {
        consoleOutput.push(['log', ...args]);
        originalConsole.log(...args);
    },
    error: (...args) => {
        consoleOutput.push(['error', ...args]);
        originalConsole.error(...args);
    },
    warn: (...args) => {
        consoleOutput.push(['warn', ...args]);
        originalConsole.warn(...args);
    }
};

// Variáveis para controle de progresso dos testes
let totalTests = 0;
let completedTests = 0;
let failedTests = 0;
let testStartTime = 0;
let currentTestName = '';

// Função para iniciar um teste com timeout
function startTest(testName, timeoutMs = 10000) {
    currentTestName = testName;
    totalTests++;
    testStartTime = Date.now();
    console.log(`\n🔄 Iniciando teste: ${testName} (${completedTests}/${totalTests} concluídos, ${Math.round((completedTests/totalTests)*100)}% completo)`);
    
    // Configurar timeout para evitar que o teste trave indefinidamente
    return setTimeout(() => {
        console.error(`⏱️ TIMEOUT: O teste "${testName}" excedeu ${timeoutMs/1000} segundos e foi interrompido`);
        failedTests++;
        completeTest(testName, false);
    }, timeoutMs);
}

// Função para finalizar um teste
function completeTest(testName, success = true) {
    if (currentTestName === testName) {
        const duration = Date.now() - testStartTime;
        completedTests++;
        currentTestName = '';
        
        if (success) {
            console.log(`✅ Teste concluído: ${testName} em ${duration}ms (${completedTests}/${totalTests} concluídos, ${Math.round((completedTests/totalTests)*100)}% completo)`);
        } else if (!success) {
            console.error(`❌ Teste falhou: ${testName} após ${duration}ms (${completedTests}/${totalTests} concluídos, ${Math.round((completedTests/totalTests)*100)}% completo)`);
        }
    }
}

// Importação dinâmica dos controllers
async function importControllers() {
    console.log('Iniciando importação dinâmica dos controllers...');
    const controllers = {};
    
    try {
        console.log('Tentando importar CompanyController...');
        controllers.CompanyController = (await import('../controllers/CompanyController.js')).default;
        console.log('CompanyController importado com sucesso');
    } catch (error) {
        console.error('Erro ao importar CompanyController:', error.message);
    }
    
    try {
        console.log('Tentando importar ContactController...');
        controllers.ContactController = (await import('../controllers/ContactController.js')).default;
        console.log('ContactController importado com sucesso');
    } catch (error) {
        console.error('Erro ao importar ContactController:', error.message);
    }
    
    try {
        console.log('Tentando importar PortfolioController...');
        controllers.PortfolioController = (await import('../controllers/PortfolioController.js')).default;
        console.log('PortfolioController importado com sucesso');
    } catch (error) {
        console.error('Erro ao importar PortfolioController:', error.message);
    }
    
    return controllers;
}

// Função para limpar a saída do console
function clearConsoleOutput() {
    consoleOutput = [];
}

// Função para verificar se um valor existe na saída do console
function checkConsoleForValue(value) {
    return consoleOutput.some(entry => 
        entry.some(item => 
            typeof item === 'string' && item.includes(value) ||
            typeof item === 'object' && JSON.stringify(item).includes(value)
        )
    );
}

async function testModelToControllerPropagation() {
    console.log('\n=== Testando propagação de Model para Controller ===');
    
    const { CompanyController, ContactController, PortfolioController } = await importControllers();
    
    // Teste CompanyModel -> CompanyController
    if (CompanyController) {
        const testName = 'CompanyModel -> CompanyController';
        const timeout = startTest(testName);
        
        try {
            const companyController = new CompanyController();
            const mockContainer = new MockElement();
            
            // Espiona o método renderSocialMedia
            const originalRenderMethod = companyController.renderSocialMedia;
            let renderCalled = false;
            let renderedData = null;
            
            companyController.renderSocialMedia = (data, container) => {
                renderCalled = true;
                renderedData = data;
                return originalRenderMethod.call(companyController, data, container);
            };
            
            // Inicializa o controller com o container mock
            companyController.socialMediaContainer = mockContainer;
            await companyController.loadSocialMedia();
            
            // Verifica se os dados do modelo foram passados para o controller
            console.log('Render foi chamado:', renderCalled);
            console.log('Dados renderizados:', renderedData);
            
            clearTimeout(timeout);
            completeTest(testName, renderCalled && renderedData);
        } catch (error) {
            console.error(`Erro no teste ${testName}:`, error);
            clearTimeout(timeout);
            completeTest(testName, false);
        }
    }
    
    // Teste ContactModel -> ContactController
    if (ContactController) {
        const testName = 'ContactModel -> ContactController';
        const timeout = startTest(testName);
        
        try {
            const contactController = new ContactController();
            const mockContainer = new MockElement();
            
            // Espiona o método renderContacts
            const originalRenderMethod = contactController.renderContacts;
            let renderCalled = false;
            let renderedData = null;
            
            contactController.renderContacts = (data) => {
                renderCalled = true;
                renderedData = data;
                return originalRenderMethod.call(contactController, data);
            };
            
            // Inicializa o controller com o container mock
            contactController.contactContainer = mockContainer;
            await contactController.loadContacts();
            
            // Verifica se os dados do modelo foram passados para o controller
            console.log('Render foi chamado:', renderCalled);
            console.log('Dados renderizados:', renderedData);
            
            clearTimeout(timeout);
            completeTest(testName, renderCalled && renderedData);
        } catch (error) {
            console.error(`Erro no teste ${testName}:`, error);
            clearTimeout(timeout);
            completeTest(testName, false);
        }
    }
    
    // Teste PortfolioModel -> PortfolioController
    if (PortfolioController) {
        const testName = 'PortfolioModel -> PortfolioController';
        const timeout = startTest(testName);
        
        try {
            console.log('Criando instância do PortfolioController...');
            const portfolioController = new PortfolioController();
            console.log('PortfolioController instanciado com sucesso');
            
            const mockGrid = new MockElement();
            console.log('Mock grid criado');
            
            // Espiona o método renderProjects
            console.log('Configurando espionagem do método renderProjects...');
            const originalRenderMethod = portfolioController.renderProjects;
            let renderCalled = false;
            
            portfolioController.renderProjects = () => {
                console.log('Método renderProjects foi chamado');
                renderCalled = true;
                console.log('Chamando método original renderProjects...');
                const result = originalRenderMethod.call(portfolioController);
                console.log('Método original renderProjects executado com sucesso');
                return result;
            };
            
            // Inicializa o controller com o grid mock
            console.log('Configurando portfolioGrid no controller...');
            portfolioController.portfolioGrid = mockGrid;
            console.log('Chamando renderProjects...');
            portfolioController.renderProjects();
            console.log('renderProjects concluído');
            
            // Verifica se o método de renderização foi chamado
            console.log('Render foi chamado:', renderCalled);
            
            clearTimeout(timeout);
            completeTest(testName, renderCalled);
        } catch (error) {
            console.error(`Erro no teste ${testName}:`, error);
            console.error('Stack trace:', error.stack);
            clearTimeout(timeout);
            completeTest(testName, false);
        }
    }
}

async function testControllerToViewPropagation() {
    console.log('\n=== Testando propagação de Controller para View ===');
    
    const { CompanyController, ContactController, PortfolioController } = await importControllers();
    
    // Teste CompanyController -> View
    if (CompanyController) {
        const testName = 'CompanyController -> View';
        const timeout = startTest(testName);
        
        try {
            const companyController = new CompanyController();
            const mockContainer = new MockElement();
            
            // Inicializa o controller com o container mock
            companyController.socialMediaContainer = mockContainer;
            await companyController.loadSocialMedia();
            
            // Verifica se o HTML foi modificado
            console.log('Container HTML após renderização:', mockContainer.innerHTML);
            console.log('Número de elementos filhos:', mockContainer.children.length);
            
            const success = mockContainer.children.length > 0 || mockContainer.innerHTML.length > 0;
            clearTimeout(timeout);
            completeTest(testName, success);
        } catch (error) {
            console.error(`Erro no teste ${testName}:`, error);
            clearTimeout(timeout);
            completeTest(testName, false);
        }
    }
    
    // Teste ContactController -> View
    if (ContactController) {
        const testName = 'ContactController -> View';
        const timeout = startTest(testName);
        
        try {
            const contactController = new ContactController();
            const mockContainer = new MockElement();
            
            // Inicializa o controller com o container mock
            contactController.contactContainer = mockContainer;
            await contactController.loadContacts();
            
            // Verifica se o HTML foi modificado
            console.log('Container HTML após renderização:', mockContainer.innerHTML);
            
            const success = mockContainer.innerHTML.length > 0;
            clearTimeout(timeout);
            completeTest(testName, success);
        } catch (error) {
            console.error(`Erro no teste ${testName}:`, error);
            clearTimeout(timeout);
            completeTest(testName, false);
        }
    }
    
    // Teste PortfolioController -> View
    if (PortfolioController) {
        const testName = 'PortfolioController -> View';
        const timeout = startTest(testName);
        
        try {
            const portfolioController = new PortfolioController();
            const mockGrid = new MockElement();
            
            // Inicializa o controller com o grid mock
            portfolioController.portfolioGrid = mockGrid;
            portfolioController.renderProjects();
            
            // Verifica se o HTML foi modificado
            console.log('Grid HTML após renderização:', mockGrid.innerHTML);
            
            const success = mockGrid.innerHTML.length > 0 || mockGrid.children.length > 0;
            clearTimeout(timeout);
            completeTest(testName, success);
        } catch (error) {
            console.error(`Erro no teste ${testName}:`, error);
            clearTimeout(timeout);
            completeTest(testName, false);
        }
    }
}

async function runTests() {
    console.log('Iniciando testes de propagação de dados...');
    console.log('URL Base da API:', FRONTEND_CONFIG.API_BASE_URL);
    console.log('Node.js versão:', process.version);
    
    // Resetar contadores de teste
    totalTests = 0;
    completedTests = 0;
    failedTests = 0;
    
    const startTime = Date.now();
    
    try {
        console.log('\nIniciando testes de propagação Model -> Controller...');
        // Teste de propagação de Model para Controller
        await testModelToControllerPropagation();
        
        console.log('\nIniciando testes de propagação Controller -> View...');
        // Teste de propagação de Controller para View
        await testControllerToViewPropagation();
        
        const duration = Date.now() - startTime;
        console.log('\n=== Resumo dos Testes ===');
        console.log(`Total de testes: ${totalTests}`);
        console.log(`Testes concluídos: ${completedTests}`);
        console.log(`Testes com sucesso: ${completedTests - failedTests}`);
        console.log(`Testes com falha: ${failedTests}`);
        console.log(`Percentual de sucesso: ${Math.round(((completedTests - failedTests) / totalTests) * 100)}%`);
        console.log(`Tempo total de execução: ${duration}ms`);
        console.log('\n=== Testes concluídos! ===');
    } catch (error) {
        console.error('\n❌ ERRO CRÍTICO durante a execução dos testes:');
        console.error('Mensagem:', error.message);
        console.error('Stack trace:', error.stack);
        console.error('Tipo de erro:', error.name);
        
        if (error.code === 'ERR_MODULE_NOT_FOUND') {
            console.error('\nErro de módulo não encontrado. Verifique se todos os arquivos estão no caminho correto.');
            console.error('Dica: Para executar módulos ES no Node.js, você pode precisar adicionar a flag "--experimental-modules" ou usar a extensão ".mjs".');
        }
    }
}

runTests();