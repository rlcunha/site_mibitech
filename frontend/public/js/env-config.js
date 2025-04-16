/**
 * env-config.js
 * Este arquivo é responsável por disponibilizar as variáveis de ambiente para o frontend
 * Todas as variáveis de ambiente são consolidadas no objeto window.ENV
 */

// Inicializa o objeto global para variáveis de ambiente
window.ENV = window.ENV || {};

// Define as variáveis de ambiente com valores padrão
// Este arquivo será modificado pelo servidor para injetar as variáveis de ambiente reais
window.ENV = {
  // URL base da API
  API_BASE_URL: window.ENV.API_BASE_URL || 'http://apirest.mibitech.com.br:8000',
  
  // Ambiente de execução (development, production, test)
  NODE_ENV: window.ENV.NODE_ENV || 'development',
  
  // Outras variáveis de ambiente podem ser adicionadas aqui
  VERSION: window.ENV.VERSION || '1.0.0'
};

// Exporta o objeto ENV para uso em módulos ES6
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { ENV: window.ENV };
}