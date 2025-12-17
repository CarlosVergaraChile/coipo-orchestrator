# COIPO MVP Orchestrator - Descripción General

## Qué hace el MVP

El MVP COIPO Orchestrator es un sistema de automatización de flujos de trabajo que:

1. **Envía una invitación por email** con consentimiento explícito (usuario clickea "OK")
2. **Recibe la confirmación** a través de un webhook seguro
3. **Autoriza acceso** via OAuth2 (NO passwords) a Gmail
4. **Lee emails** recientes (readonly) con scope mínimo
5. **Analiza contenido** (heurísticas + LLM opcional)
6. **Genera informe HTML** con firma temporal (TTL 48h)
7. **Envía el informe** al usuario vía email
8. **Revoca acceso** limpiamente post-entrega

## Experiencia del usuario

```
Usuario recibe email → Hace clic en link "OK" → Se abre pantalla Google OAuth → Autoriza
↓
MVP accede Gmail (solo lectura) → Analiza → Genera informe → Envía email con link
↓
Usuario accede informe → Link expira en 48h → Acceso revocado automáticamente
```

## Lo que NO hace

- ❌ No solicita usuario/password de email
- ❌ No almacena contenido de emails persistentemente
- ❌ No modifica ni borra emails del usuario
- ❌ No envía autos confirmaciones (manual explicit only)
- ❌ No mantiene tokens después de revocación

## Arquitectura

**Stack:**
- **Orchestrator:** n8n (workflow automation)
- **Auth:** Gmail OAuth2 (no SMTP)
- **Report Delivery:** Email corto + URL firmada (pre-signed)
- **TTL/Cleanup:** Token revocation + temp file cleanup

## Próximos pasos

Ver documentos:
- `security_model.md` - Principios y reglas de seguridad
- `oauth_gmail_setup.md` - Configuración Google Cloud
- `workflow_nodes.md` - Nodos n8n específicos
