# coipo-orchestrator
MVP Orchestrator para COIPO - n8n + OAuth2 (sin passwords) | Workflow automation, Gmail integration, secure token handling


## Estructura del Repositorio

```
coipo-orchestrator/
├── README.md
├── coipo/
│  ├── orchestrator/
│  │  ├── docs/
│  │  │  ├── mvp_overview.md (Descripción general del MVP)
│  │  │  ├── COIPO_MVP_SPEC_COMPLETO.md (Especificación técnica completa)
│  │  └── (futuros: security_model.md, oauth_gmail_setup.md, workflow_nodes.md, etc.)
│  └── n8n/ (workflows, credentials, etc.)
└── (futuros: tests/, deployment/, etc.)
```

## Key Documents

- **coipo/orchestrator/docs/mvp_overview.md** - Overview del flujo end-to-end, experiencia del usuario, arquitectura
- **coipo/orchestrator/docs/COIPO_MVP_SPEC_COMPLETO.md** - Especificación técnica completa (security, OAuth2, workflow nodes, email templates, revocation)

## Principios Clave

✅ **Sin Passwords** - Solo OAuth2 (Gmail API)  
✅ **Scopes Mínimos** - Principle of Least Privilege  
✅ **Temporalidad** - Token TTL 1h, Report TTL 48h  ✅ **Revocación Automática** - Post-entrega, cleanup completo  
✅ **Seguridad** - No almacenamiento de emails, logging seguro

## Getting Started

1. Lee `coipo/orchestrator/docs/mvp_overview.md` para entender el flujo
2. Lee `coipo/orchestrator/docs/COIPO_MVP_SPEC_COMPLETO.md` para detalles técnicos
3. Implementa los nodos en n8n siguiendo la especificación
4. Prueba con Gmail OAuth2 (sin passwords)
5. Deploy con cleanup automático post-revocación

## Status

**Versión:** 1.0.0  
**Fecha:** 2025-12-17  
**Status:** En Proceso - Artefacto Técnico Versionado
