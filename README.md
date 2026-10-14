# Gomobile documentation

Product guides and API reference for Gomobile, built with Mintlify.

## Getting started

Install [Node.js](https://nodejs.org/) **20.17.0 or newer** with npm, and ensure you have Git and access to the repository.

Clone the project:

```bash
git clone https://github.com/Gomobile-Africa/product-docs.git
cd product-docs
```

## Development

Install the Mintlify CLI:

```bash
npm install -g mint
```

Run the preview from the repository root, where `docs.json` is located:

```bash
mint dev
```

Open **http://localhost:3000**, or the URL printed in your terminal. Keep the terminal running while previewing. Changes to `.mdx` pages update the preview; press **Ctrl+C** to stop it.

No Gomobile backend, database, or API credentials are needed to preview the documentation.

## Check changes

Before opening a pull request, run:

```bash
mint validate
mint broken-links
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for content guidelines.

## Publishing changes

Submit changes through a pull request for team review. If this repository and branch are connected to Mintlify, merged changes deploy through that connection. Confirm the deployment branch and status in the Mintlify dashboard.

## Troubleshooting

- **`node` or `npm` not found:** install Node.js and reopen your terminal.
- **CLI missing or outdated:** run `npm install -g mint@latest`.
- **Global installation fails:** use `npx mint@latest dev` to preview without a global install.
- **Preview fails to find pages:** run the command from the folder containing `docs.json`.
- **Search asks you to log in:** run `mint login`, sign in to Mintlify, then restart `mint dev` and refresh the browser. CLI login enables search in the local preview.
- **Port occupied:** run `mint dev --port 3333` and open http://localhost:3333.

For more help, see the [Mintlify installation guide](https://www.mintlify.com/docs/cli/install).
