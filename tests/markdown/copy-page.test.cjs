const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const script = fs.readFileSync(path.join(__dirname, '../../local-markdown.js'), 'utf8');

function preview(markdown, origin = 'http://localhost:3002') {
  const requests = [];
  const location = new URL('/guides/ai-tools/installation', origin);
  const window = {
    location,
    fetch: async (...args) => {
      requests.push(args);
      return new Response(markdown, { headers: { 'content-type': 'text/markdown' } });
    },
    open: () => {},
  };
  vm.runInNewContext(script, {
    window, URL, Request, Response, Headers,
    document: { documentElement: {}, querySelectorAll: () => [] },
    MutationObserver: class { observe() {} },
  });
  return { window, requests };
}

test('copy keeps indented fenced commands attached to their numbered steps', async () => {
  const block = '   ```bash\n   codex plugin marketplace add .\n   codex plugin add gomobile@gomobile\n   ```';
  const input = `> ## Documentation Index\n> Index metadata\n\n# Install Gomobile skills\n\n1. Install:\n\n${block}\n\n2. Start a new session.\n`;
  const { window, requests } = preview(input);
  const output = await (await window.fetch('/guides/ai-tools/installation.md')).text();
  assert.equal(output, input.slice(input.indexOf('# Install')));
  assert.equal(requests[0][0], 'http://localhost:3002/_markdown/guides/ai-tools/installation');
});

test('copy converts callouts and cards while preserving code and inline examples', async () => {
  const code = '```md\n<Warning>Keep this literal.</Warning>\n[Keep this link](/literal)\n\n\n    preserve four spaces\n```';
  const input = `# Example\n\n<Warning>\n  Tests send real messages.\n</Warning>\n\n<CardGroup cols={2}>\n<Card title="Usage" href="/guides/ai-tools/usage">Read the guide.</Card>\n</CardGroup>\n\n${code}\n\nUse \`[example](/literal)\`.\n`;
  const { window } = preview(input);
  const output = await (await window.fetch('/example.md')).text();
  assert.ok(output.includes('> **Warning:** Tests send real messages.'));
  assert.ok(output.includes('[Usage](https://docs.gomobile.ma/guides/ai-tools/usage)'));
  assert.ok(output.includes(code));
  assert.ok(output.includes('`[example](/literal)`'));
  assert.ok(!output.includes('<Card'));
});

test('localhost links become public docs links while external links stay intact', async () => {
  const input = '# Example\n\n[Usage](/guides/ai-tools/usage#review)\n[Section](#codex)\n[External](https://example.com/guide)\n';
  const { window } = preview(input);
  const output = await (await window.fetch('/example.md')).text();
  assert.ok(output.includes('[Usage](https://docs.gomobile.ma/guides/ai-tools/usage#review)'));
  assert.ok(output.includes('[Section](https://docs.gomobile.ma/guides/ai-tools/installation#codex)'));
  assert.ok(output.includes('[External](https://example.com/guide)'));
  assert.ok(!output.includes('localhost'));
});

test('Request objects keep their headers when local Markdown routing changes', async () => {
  const { window, requests } = preview('# Example\n');
  const request = new Request('http://localhost:3002/example.md?revision=1', {
    headers: { Accept: 'text/markdown' },
  });
  await window.fetch(request);
  assert.equal(requests[0][0].url, 'http://localhost:3002/_markdown/example?revision=1');
  assert.equal(requests[0][0].headers.get('Accept'), 'text/markdown');
});

test('deployed Markdown requests are not rewritten to the local preview route', async () => {
  const { window, requests } = preview('# Example\n\n[Usage](/guides/ai-tools/usage)\n', 'https://docs.gomobile.ma');
  const output = await (await window.fetch('/example.md')).text();
  assert.equal(requests[0][0], '/example.md');
  assert.ok(output.includes('https://docs.gomobile.ma/guides/ai-tools/usage'));
});

test('non-Markdown and external fetch responses remain untouched', async () => {
  const input = '  <Info>Do not alter unrelated data.</Info>  ';
  const { window, requests } = preview(input);
  assert.equal(await (await window.fetch('/api/example')).text(), input);
  assert.equal(await (await window.fetch('https://example.com/file.md')).text(), input);
  assert.equal(requests[0][0], '/api/example');
  assert.equal(requests[1][0], 'https://example.com/file.md');
});
