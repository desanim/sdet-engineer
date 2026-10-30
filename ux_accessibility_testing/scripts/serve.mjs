// Self-contained local fixture. No wallet, RPC, persistence or external calls.
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
const assets = { '/': ['index.html', 'text/html'], '/app.js': ['app.js', 'text/javascript'], '/styles.css': ['styles.css', 'text/css'] };
const sendJSON = (res, code, body) => { res.writeHead(code, { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' }); res.end(JSON.stringify(body)); };
createServer(async (req, res) => {
  try {
    const path = new URL(req.url, 'http://localhost').pathname;
    if (path === '/api/health' && req.method === 'GET') return sendJSON(res, 200, { status: 'ok', service: 'simulated-quotes' });
    if (path === '/api/quote') {
      if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return sendJSON(res, 405, { error: 'method_not_allowed' }); }
      let body = ''; let bytes = 0;
      for await (const chunk of req) { bytes += chunk.length; if (bytes > 4096) return sendJSON(res, 413, { error: 'payload_too_large' }); body += chunk; }
      let data;
      try { data = JSON.parse(body); } catch { return sendJSON(res, 400, { error: 'invalid_json' }); }
      if (!data || typeof data.amount !== 'number' || !Number.isFinite(data.amount) || data.amount < 0.000001 || data.amount > 5) {
        return sendJSON(res, 422, { error: 'invalid_amount', message: 'Amount must be between 0.000001 and 5 ETH.' });
      }
      return sendJSON(res, 200, { amount: data.amount, rate: 3124.5, receive: Number((data.amount * 3124.5).toFixed(2)), from: 'ETH', to: 'USDC', simulated: true });
    }
    const asset = Object.hasOwn(assets, path) ? assets[path] : null;
    if (!asset) return sendJSON(res, 404, { error: 'not_found' });
    if (req.method !== 'GET') { res.setHeader('Allow', 'GET'); return sendJSON(res, 405, { error: 'method_not_allowed' }); }
    const body = await readFile(new URL(`../demo/${asset[0]}`, import.meta.url));
    res.writeHead(200, { 'Content-Type': `${asset[1]}; charset=utf-8`, 'Cache-Control': 'no-store' }); res.end(body);
  } catch { if (!res.headersSent) sendJSON(res, 500, { error: 'fixture_error' }); else res.end(); }
}).listen(4173, '127.0.0.1', () => console.log('Demo + API: http://127.0.0.1:4173'));
