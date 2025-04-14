/**
 * server.js
 * Simple HTTP server for the MibiTech frontend application
 */

import http from 'http';
import https from 'https';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

// Get __dirname equivalent in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Define the port to use
const PORT = process.env.PORT || 3000;

// MIME types for different file extensions
const MIME_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.mjs': 'application/javascript',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.ttf': 'font/ttf',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.eot': 'application/vnd.ms-fontobject',
    '.otf': 'font/otf',
    '.wasm': 'application/wasm'
};

// Proxy configuration
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

// Create the HTTP server with logging disabled
const server = http.createServer((req, res) => {
    // Disable request logging
    // Handle API requests
    if (req.url.startsWith('/api/') || req.url.startsWith('/api/v1/')) {
        const apiUrl = `${API_BASE_URL}${req.url}`;
        const client = apiUrl.startsWith('https://') ? https : http;
        
        const proxyReq = client.request(apiUrl, (proxyRes) => {
            res.writeHead(proxyRes.statusCode, proxyRes.headers);
            proxyRes.pipe(res, { end: true });
        });
        
        req.pipe(proxyReq, { end: true });
        return;
    }
    
    // Parse the URL for static files
    let filePath = req.url;
    
    // Handle root URL
    if (filePath === '/') {
        filePath = '/index.html';
    }
    
    // Resolve the file path safely
    filePath = path.join(__dirname, ...filePath.split('/').filter(p => !p.includes('..')));
    
    // Get the file extension and MIME type
    const extname = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[extname] || 'application/octet-stream';
    
    // Read the file
    fs.readFile(filePath, (err, content) => {
        // Only log errors
        if (err) {
            if (err.code === 'ENOENT') {
                if (extname === '.html') {
                    const filename = path.basename(filePath);
                    const viewsFilePath = path.join(__dirname, 'views', filename);
                    
                    fs.readFile(viewsFilePath, (viewsErr, viewsContent) => {
                        if (viewsErr) {
                            fs.readFile(path.join(__dirname, 'views', 'index.html'), (indexErr, indexContent) => {
                                if (indexErr) {
                                    res.writeHead(404, { 'Content-Type': 'text/html' });
                                    res.end('<h1>404 Not Found</h1>');
                                    return;
                                }
                                
                                res.writeHead(200, { 'Content-Type': 'text/html' });
                                res.end(indexContent, 'utf-8');
                            });
                        } else {
                            res.writeHead(200, { 'Content-Type': 'text/html' });
                            res.end(viewsContent, 'utf-8');
                        }
                    });
                } else {
                    res.writeHead(404);
                    res.end(`File not found: ${req.url}`);
                }
            } else {
                res.writeHead(500);
                res.end(`Server Error: ${err.code}`);
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
        }
    });
});

// Start the server
server.listen(PORT, '0.0.0.0', () => {
    console.log(`\n=== SERVER STARTED ===`);
    console.log(`Server running at http://localhost:${PORT}/`);
    console.log(`Press Ctrl+C to stop the server\n`);
    
    // Add CORS headers for development
    server.on('request', (req, res) => {
        // Log all requests
        // console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
        
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    });
});