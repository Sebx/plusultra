# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in plusultra, please **do not** open a public GitHub issue. Instead:

1. Email `sebastian.andres.rodriguez@blend360.com` with:
   - Description of the vulnerability
   - Steps to reproduce (if applicable)
   - Potential impact
   - Suggested fix (if you have one)

2. Include `[SECURITY]` in the subject line

## Response Timeline

- **Initial response**: Within 48 hours
- **Fix evaluation**: Within 1 week
- **Public disclosure**: Coordinated with you, typically 30 days after fix is released

## Scope

Vulnerabilities in **plusultra's code** are in scope:
- XSS or injection issues in the UI
- Unsafe model loading or inference
- Service worker security issues
- Tokenizer or ONNX Runtime misuse

**Out of scope** (report to the relevant project):
- ONNX Runtime CVEs — report to [Microsoft](https://github.com/microsoft/onnxruntime)
- Chocolate Doom issues — report to [chocolate-doom](https://github.com/chocolate-doom/chocolate-doom)
- Browser vulnerabilities — report to the browser vendor

## Security Considerations for Users

### What plusultra Does NOT Do

- Send data to any server (100% client-side)
- Store user input permanently
- Use external APIs
- Load arbitrary code from the network

### Model Safety

- The GLiClass model is a **classifier**, not a generative model — it can't produce arbitrary text
- Model weights are frozen and hash-verified
- The model has known weak spots (see README.md → Limitations)

### Browser Safety

- Service workers are trusted (they're part of the PWA)
- Web Workers run the same code as the UI thread
- WebGPU access is restricted to localhost or HTTPS
- No sensitive user data is stored in localStorage

---

Thank you for helping keep plusultra secure.
