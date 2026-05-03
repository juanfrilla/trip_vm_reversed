# Trip.com JSVMP Reversing: Phantom-Token Logic Reconstruction

## Overview

This repository documents the reverse engineering of the **Trip.com Phantom-Token** generation logic. By analyzing the underlying Stack-Based Virtual Machine (JSVMP), I managed to reconstruct the cryptographic and fingerprinting logic to run natively in a standalone environment, completely bypassing the need for a browser or a heavy automation framework.

---

## Methodology: "Taint Analysis"

### The Process

0. **Localizing the Token Generation:** Using the browser's DevTools, the phantom-token
   generation was traced to a single call: `var C = window.signature(o.data);`, where
   `o.data` is the request payload. Notably, an empty payload is also accepted and will
   return a valid token.
1. **VM Sandboxing:** Isolated the JSVMP environment and provided mocked browser globals
   (`window`, `document`, `location`, `navigator` and `screen`) on-demand via a Proxy
   that intercepts property accesses returning `undefined` as they are requested by the VM
   (see the `watch` method in `./js/vm_logged.js`), until the full token generation flow
   completed successfully.
2. **High-Level Hooking:** Instrumented the VM's main dispatcher to log inputs and outputs of critical handlers, the closest to the JavaScript runtime:
   - `func_call` & `new` (Object instantiation and API calls)
   - Bitwise & Arithmetic operations
   - String manipulation logic
3. **Trace Export:** Generated a comprehensive execution trace in `.txt` format via `node ./js/vm_logged.js > out.txt`.
4. **Pattern Recognition:** Analyzed the trace from top to bottom (from line 0 to the end) to identify the underlying algorithms and reconstruct the js logic.


## Steps to Make It Work

### 1. JavaScript — Generate the Trace

```bash
node ./js/vm_logged.js > out.txt
```

### 2. Python — Run the Token Server

```bash
uv venv venv
source venv/bin/activate
uv pip install -r requirements.txt

python main.py
```

## Key Tech Stack

| Category   | Details                                                           |
| ---------- | ----------------------------------------------------------------- |
| Language   | JavaScript (Node.js)                                              |
| Techniques | Hooking, Sandboxing, Taint Analysis, Cryptographic Identification |
| Target     | Stack-Based JSVMP                                                 |


> **Disclaimer:** This project is for educational and research purposes only. Use of this tool must comply with the target website's Terms of Service and applicable data privacy laws.