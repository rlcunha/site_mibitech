#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple API Server para o site MibiTech
Este servidor fornece endpoints básicos para o frontend, incluindo o envio de formulários de contato.
"""

import json
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import os
import datetime

# Configuração do servidor
PORT = 8000
HOST = "localhost"

# Armazenamento em memória para os contatos recebidos
contacts = []

# Dados de exemplo para portfolio
portfolio_items = [
    {
        "id": 1,
        "title": "Sistema de Gestão Empresarial",
        "description": "Desenvolvimento de um sistema completo de gestão empresarial com módulos de finanças, RH e logística.",
        "image": "project1.jpg",
        "technologies": ["Python", "Django", "React", "PostgreSQL"],
        "client": "Empresa ABC Ltda",
        "year": 2023
    },
    {
        "id": 2,
        "title": "Aplicativo Mobile de Delivery",
        "description": "Aplicativo para Android e iOS para serviço de delivery com rastreamento em tempo real.",
        "image": "project2.jpg",
        "technologies": ["React Native", "Node.js", "MongoDB", "Firebase"],
        "client": "DeliveryExpress",
        "year": 2022
    },
    {
        "id": 3,
        "title": "E-commerce B2B",
        "description": "Plataforma de e-commerce para vendas entre empresas com sistema de cotação e aprovação.",
        "image": "project3.jpg",
        "technologies": ["PHP", "Laravel", "Vue.js", "MySQL"],
        "client": "Distribuidora XYZ",
        "year": 2023
    }
]

# Dados de exemplo para a empresa
company_info = {
    "name": "MibiTech Soluções Digitais",
    "description": "Empresa especializada em desenvolvimento de software e soluções digitais para negócios.",
    "mission": "Transformar negócios através da tecnologia, oferecendo soluções inovadoras e de alta qualidade.",
    "vision": "Ser referência em inovação tecnológica, reconhecida pela excelência e impacto positivo nos negócios dos clientes.",
    "values": [
        "Inovação",
        "Qualidade",
        "Compromisso",
        "Ética",
        "Colaboração"
    ],
    "foundation_year": 2015,
    "team_size": 25,
    "address": "Av. Tecnologia, 1000 - São Paulo, SP",
    "contact": {
        "email": "contato@mibitech.com.br",
        "phone": "+55 11 3456-7890",
        "whatsapp": "+55 11 98765-4321"
    },
    "social_media": {
        "facebook": "https://facebook.com/mibitech",
        "instagram": "https://instagram.com/mibitech",
        "linkedin": "https://linkedin.com/company/mibitech",
        "github": "https://github.com/mibitech"
    }
}

class APIHandler(http.server.SimpleHTTPRequestHandler):
    """
    Manipulador de requisições HTTP para a API
    """
    
    def _set_headers(self, status_code=200, content_type="application/json"):
        """
        Configura os cabeçalhos da resposta HTTP
        """
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        # Configuração de CORS para permitir requisições do frontend
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def do_OPTIONS(self):
        """
        Responde a requisições OPTIONS (pré-voo CORS)
        """
        self._set_headers()
        self.wfile.write(json.dumps({}).encode())
    
    def do_GET(self):
        """
        Processa requisições GET
        """
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Rota para obter informações da empresa
        if path == "/api/company/":
            self._set_headers()
            self.wfile.write(json.dumps(company_info).encode())
        
        # Rota para obter itens do portfólio
        elif path == "/api/portfolio/":
            self._set_headers()
            self.wfile.write(json.dumps(portfolio_items).encode())
        
        # Rota para obter um item específico do portfólio
        elif path.startswith("/api/portfolio/") and len(path.split("/")) > 3:
            try:
                item_id = int(path.split("/")[3])
                item = next((item for item in portfolio_items if item["id"] == item_id), None)
                
                if item:
                    self._set_headers()
                    self.wfile.write(json.dumps(item).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Item não encontrado"}).encode())
            except ValueError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "ID inválido"}).encode())
        
        # Rota para obter contatos enviados
        elif path == "/api/contacts/":
            self._set_headers()
            self.wfile.write(json.dumps(contacts).encode())
        
        # Rota para obter informações de redes sociais
        elif path == "/api/social-media/":
            self._set_headers()
            # Transformar o objeto social_media em uma lista de objetos com id, nome, url e ícone
            social_media_list = [
                {"id": 1, "name": "Facebook", "url": company_info["social_media"]["facebook"], "icon": "fab fa-facebook-f"},
                {"id": 2, "name": "Instagram", "url": company_info["social_media"]["instagram"], "icon": "fab fa-instagram"},
                {"id": 3, "name": "LinkedIn", "url": company_info["social_media"]["linkedin"], "icon": "fab fa-linkedin-in"},
                {"id": 4, "name": "GitHub", "url": company_info["social_media"]["github"], "icon": "fab fa-github"}
            ]
            self.wfile.write(json.dumps(social_media_list).encode())
        
        # Rota para verificar status da API
        elif path == "/api/status/":
            self._set_headers()
            self.wfile.write(json.dumps({
                "status": "online",
                "timestamp": datetime.datetime.now().isoformat(),
                "version": "1.0.0"
            }).encode())
        
        # Rota não encontrada
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Rota não encontrada"}).encode())
    
    def do_POST(self):
        """
        Processa requisições POST
        """
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode("utf-8"))
            
            # Rota para envio de formulário de contato
            if self.path == "/api/submit-contact/":
                # Validação básica dos campos obrigatórios
                required_fields = ["name", "email", "subject", "message"]
                missing_fields = [field for field in required_fields if not data.get(field)]
                
                if missing_fields:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({
                        "success": False,
                        "message": f"Campos obrigatórios ausentes: {', '.join(missing_fields)}"
                    }).encode())
                    return
                
                # Adiciona timestamp ao contato
                contact = {
                    **data,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "id": len(contacts) + 1
                }
                
                # Armazena o contato na lista em memória
                contacts.append(contact)
                
                # Responde com sucesso
                self._set_headers()
                self.wfile.write(json.dumps({
                    "success": True,
                    "message": "Mensagem enviada com sucesso! Agradecemos seu contato.",
                    "contact_id": contact["id"]
                }).encode())
            
            # Rota não encontrada
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Rota não encontrada"}).encode())
        
        except json.JSONDecodeError:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Dados JSON inválidos"}).encode())


def run_server():
    """
    Inicia o servidor HTTP
    """
    server_address = (HOST, PORT)
    httpd = socketserver.TCPServer(server_address, APIHandler)
    print(f"Servidor API rodando em http://{HOST}:{PORT}/")
    print("Pressione Ctrl+C para encerrar")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado")
        httpd.server_close()


if __name__ == "__main__":
    run_server()