// Deliberately serves only the demo's three known assets, on loopback.
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
const assets = { '/': ['index.html', 'text/html'], '/app.js': ['app.js', 'text/javascript'], '/styles.css': ['styles.css', 'text/css'] };
createServer(async (req, res) => {
  const asset = assets[new URL(req.url, 'http://localhost').pathname];
  if (!asset) { res.writeHead(404); res.end('Not found'); return; }
  try {
    const body = await readFile(new URL(`../demo/${asset[0]}`, import.meta.url));
    res.writeHead(200, { 'Content-Type': `${asset[1]}; charset=utf-8`, 'Cache-Control': 'no-store' }); res.end(body);
  } catch { res.writeHead(500); res.end('Demo asset unavailable'); }
}).listen(4173, '127.0.0.1', () => console.log('Demo: http://127.0.0.1:4173'));
