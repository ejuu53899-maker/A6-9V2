# Release v1.22.0 Summary

## Overview

This document summarizes the major release (v1.22.0) of the MQL5 SMC + Trend Breakout Trading System. This release focuses on security hardening, accessibility improvements, performance optimizations, and expanded infrastructure support.

## Release Date

February 19, 2026

## What's New in This Release

### Security Hardening
Significant security improvements have been implemented across the system:
- **Telegram Bot Authorization**: Fixed a critical bypass vulnerability to ensure only authorized users can trigger deployments.
- **Web Dashboard Security**: Added standard security headers (CSP, HSTS, X-Frame-Options, Referrer-Policy) to protect the dashboard.
- **Secret Scanning**: Implemented automated secret scanning and removed historical leaks from the codebase.
- **Hardened WebRequest**: Disabled non-essential WebRequest functionality by default in MQL5.

### Accessibility & UX
Improved the user experience for all users:
- **WCAG AA Compliance**: Updated UI color palettes (e.g., Indigo 600) to ensure high contrast and readability.
- **Screen Reader Support**: Added ARIA labels, semantic icons, and skip-to-content links.
- **Non-Blocking Notifications**: Replaced intrusive update dialogs with elegant, non-blocking toast notifications.

### Performance Optimizations
Reduced latency and resource usage:
- **AI Parallelization**: Market research and code upgrades now run AI requests in parallel, significantly reducing execution time.
- **Template Pre-compilation**: The web dashboard now pre-compiles Jinja2 templates for near-instant rendering.
- **MQL5 Efficiency**: Optimized core loops in the SMC indicator and EA for better performance on MT5.

### Infrastructure & Automation
Expanded the ecosystem with more tools and platforms:
- **CLI Integrations**: Full support for Jules, Gemini, and Vercel CLIs with automated setup scripts.
- **CircleCI**: Integrated CircleCI for robust, industry-standard continuous integration.
- **Continuous Deployment**: Advanced CD workflows for automated multi-platform deployments.
- **SSH Key Management**: New tools for automated SSH setup and secure remote management.

## System Features (v1.22.0)

### Trading System
- **SMC Indicator**: Advanced structure detection (BOS/CHoCH).
- **Multi-Timeframe Confirmation**: Enhanced MTF logic for reliable entries.
- **AI Integration**: Support for Gemini and Jules AI trade validation.

### Automation
- **Knowledge Base Helper**: Instant access to project documentation and strategies.
- **Cross-Platform Startup**: Standardized startup scripts for Windows, Linux, and WSL.
- **Market Research**: AI-powered analysis runs every 4 hours.

## Installation

### From GitHub Release

1. Download `Exness_MT5_MQL5.zip` from the release page.
2. Verify checksum using `Exness_MT5_MQL5.zip.sha256`.
3. Extract to your MT5 Data Folder.
4. Compile in MetaEditor.

### Using Docker

```bash
docker pull ghcr.io/a6-9v/mql5-google-onedrive:v1.22.0
```

## Documentation

- [Full Documentation Index](docs/INDEX.md)
- [Jules CLI Setup](docs/Jules_CLI_setup.md)
- [Gemini CLI Setup](docs/Gemini_CLI_setup.md)
- [Vercel CLI Setup](docs/Vercel_CLI_setup.md)
- [SSH Key Investigation](docs/SSH_KEY_INVESTIGATION_QUICK_REF.md)

## Support

- **Repository**: https://github.com/A6-9V/MQL5-Google-Onedrive
- **Issues**: https://github.com/A6-9V/MQL5-Google-Onedrive/issues

---

**Release v1.22.0** - Hardened, accessible, and faster than ever.
