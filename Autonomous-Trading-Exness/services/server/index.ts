/**
 * @file This is the main entry point for the server. It sets up an Express server,
 * configures middleware, defines a health check endpoint, registers API routes,
 * and sets up a WebSocket server.
 */
import express from 'express';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import cors from 'cors';
import rateLimit from 'express-rate-limit';
import { setupVite, serveStatic } from './vite.js';
import { registerRoutes } from './routes.js';
import { createServer, request } from 'http';
import { WebSocketServer } from 'ws';

const __dirname = dirname(fileURLToPath(import.meta.url));
const app = express();
const PORT = process.env.PORT || 5000;

// Rate limiting middleware to prevent brute-force and DoS
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  standardHeaders: true,
  legacyHeaders: false,
});

app.use(limiter);

// Enhanced logging middleware
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`${new Date().toISOString()} - ${req.method} ${req.url} - ${res.statusCode} - ${duration}ms`);
  });
  next();
});

// Simple proxy for /api requests to Python backend
app.use(['/api/v1', '/trading-pairs'], (req, res) => {
  // Mitigate SSRF by strictly constructing the target URL
  // Use 'api' service name for Docker networking and hardcoded base
  const targetBase = 'http://api:8000';

  // Safely construct the target URL using only the path and query components
  const targetUrl = new URL(targetBase);

  // Use req.baseUrl and req.path to construct the pathname safely
  targetUrl.pathname = (req.baseUrl + req.path).replace(/\/+/g, '/');

  // Safely append query parameters if present
  const searchIndex = req.originalUrl.indexOf('?');
  if (searchIndex !== -1) {
    targetUrl.search = req.originalUrl.substring(searchIndex);
  }

  const options = {
    method: req.method,
    headers: { ...req.headers },
  };
  // remove host header to avoid issues
  delete options.headers.host;

  const proxyReq = request(targetUrl, options, (proxyRes) => {
    res.writeHead(proxyRes.statusCode || 500, proxyRes.headers);
    proxyRes.pipe(res);
  });

  proxyReq.on('error', (err) => {
    console.error('Proxy error:', err);
    if (!res.headersSent) {
      res.status(502).json({ error: 'Bad Gateway', details: err.message });
    }
  });

  req.pipe(proxyReq);
});

// CORS configuration
app.use(cors({
  origin: process.env.NODE_ENV === 'production'
    ? false
    : ['http://localhost:3000', 'http://0.0.0.0:3000'],
  credentials: true
}));

app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'OK',
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV || 'development'
  });
});

// Register API routes
registerRoutes(app);

// Create HTTP server
const server = createServer(app);

// WebSocket setup
const wss = new WebSocketServer({ server });

wss.on('connection', (ws, req) => {
  console.log('WebSocket connection established from:', req.socket.remoteAddress);

  ws.on('message', (data) => {
    try {
      const message = JSON.parse(data.toString());
      console.log('Received WebSocket message:', message);

      // Echo back for testing
      ws.send(JSON.stringify({
        type: 'echo',
        data: message,
        timestamp: new Date().toISOString()
      }));
    } catch (error) {
      console.error('WebSocket message error:', error);
      ws.send(JSON.stringify({
        type: 'error',
        message: 'Invalid JSON format'
      }));
    }
  });

  ws.on('close', () => {
    console.log('WebSocket connection closed');
  });

  ws.on('error', (error) => {
    console.error('WebSocket error:', error);
  });

  // Send welcome message
  ws.send(JSON.stringify({
    type: 'welcome',
    message: 'Connected to GenZ Trading Bot Pro',
    timestamp: new Date().toISOString()
  }));
});

// Setup Vite in development or serve static files in production
if (process.env.NODE_ENV === 'production') {
  serveStatic(app, join(__dirname, '../../client/dist'));
} else {
  await setupVite(app, server);
}

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Server error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    path: req.originalUrl
  });
});

// Start server
server.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Server running on http://0.0.0.0:${PORT}`);
  console.log(`📊 Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`🔗 WebSocket server ready`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully');
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});
