// Export plain Markdown for Copy page; repair Markdown routing only in mint dev.
(() => {
  const local = ['localhost', '127.0.0.1', '[::1]'].includes(window.location.hostname);

  function plainMarkdown(markdown, pageURL) {
    const code = [];
    let text = markdown.replace(/(^|\n)(`{3,}|~{3,})[^\n]*\n[\s\S]*?\n\2[^\n]*(?=\n|$)|`+[^`\n]+`+/g, (match) => {
      code.push(match);
      return `\u0000CODE${code.length - 1}\u0000`;
    });
    // Start with the article, as in a conventional Copy for LLM export.
    text = text.replace(/^[\s\S]*?(?=^# )/m, '');
    const attribute = (attributes, name) => {
      const match = attributes.match(new RegExp(`\\b${name}=["']([^"']*)["']`));
      return match ? match[1] : '';
    };
    const absolute = (href) => new URL(href, pageURL).href;
    text = text.replace(/<Card\b([^>]*)>([\s\S]*?)<\/Card>/g, (_, attributes, body) => {
      const title = attribute(attributes, 'title');
      const href = attribute(attributes, 'href');
      return `\n\n### ${href ? `[${title}](${absolute(href)})` : title}\n\n${body.trim()}\n\n`;
    });
    text = text.replace(/<(Info|Note|Warning)\b[^>]*>([\s\S]*?)<\/\1>/g, (_, type, body) => {
      const label = type === 'Warning' ? 'Warning' : 'Note';
      return `\n\n> **${label}:** ${body.trim().replace(/\n\s*/g, '\n> ')}\n\n`;
    });
    text = text.replace(/<Step\b([^>]*)>/g, (_, attributes) => `\n\n### ${attribute(attributes, 'title')}\n\n`);
    text = text.replace(/<\/?(?:CardGroup|Steps|Step)\b[^>]*>/g, '');
    text = text.replace(/(!?\[[^\]\n]*\]\()([^\s)]+)(\))/g, (_, start, href, end) => `${start}${absolute(href)}${end}`);
    text = text.replace(/\n[ \t]+/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
    return text.replace(/\u0000CODE(\d+)\u0000/g, (_, index) => code[Number(index)]) + '\n';
  }

  function markdownURL(href) {
    if (!local) return null;
    const url = new URL(href, window.location.href);
    if (url.origin !== window.location.origin || !url.pathname.endsWith('.md')) return null;
    if (url.pathname.startsWith('/_markdown/')) return null;
    const page = url.pathname.slice(0, -3).replace(/\/$/, '') || '/index';
    url.pathname = `/_markdown${page}`;
    return url.href;
  }

  // The native Copy page action fetches .md before writing to the clipboard.
  const originalFetch = window.fetch.bind(window);
  window.fetch = async (input, options) => {
    const href = input instanceof Request ? input.url : String(input);
    const destination = markdownURL(href);
    const request = destination && input instanceof Request
      ? new Request(destination, input)
      : destination || input;
    const response = await originalFetch(request, options);
    const url = new URL(href, window.location.href);
    const isMarkdown = url.pathname.endsWith('.md') || url.pathname.startsWith('/_markdown/');
    if (!response.ok || url.origin !== window.location.origin || !isMarkdown) return response;
    const headers = new Headers(response.headers);
    headers.delete('content-length');
    headers.delete('content-encoding');
    headers.set('content-type', 'text/markdown; charset=utf-8');
    return new Response(plainMarkdown(await response.text(), window.location.href), {
      status: response.status,
      statusText: response.statusText,
      headers,
    });
  };

  // Some contextual menu versions open Markdown with window.open, not an anchor.
  if (!local) return;
  const originalOpen = window.open.bind(window);
  window.open = (url, ...options) => originalOpen(
    url ? markdownURL(String(url)) || url : url,
    ...options,
  );

  const destination = markdownURL(window.location.href);
  if (destination) {
    window.location.replace(destination);
    return;
  }

  function updateLinks() {
    document.querySelectorAll('a[href]').forEach((link) => {
      const destination = markdownURL(link.href);
      if (destination) link.href = destination;
    });
  }

  updateLinks();
  new MutationObserver(updateLinks).observe(document.documentElement, {
    childList: true,
    subtree: true,
    attributes: true,
    attributeFilter: ['href'],
  });
})();
