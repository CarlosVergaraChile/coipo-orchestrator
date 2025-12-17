# COIPO MVP Orchestrator - Especificación Técnica Completa

**Fecha:** 2025-12-17  
**Versión:** 1.0.0  
**Status:** En Proceso - Artefacto Técnico  
**Repo:** https://github.com/CarlosVergaraChile/coipo-orchestrator

---

## 1. SECURITY MODEL - Principios

### 1.1 Prohibición Absoluta de Passwords
- ❌ **NUNCA** solicitar usuario/password de correo
- ❌ **NUNCA** almacenar credenciales en plain text
- ❌ **NUNCA** usar SMTP con credenciales
- ✅ **SOLO** OAuth2 (Gmail API)

### 1.2 Scopes Mínimos (Principle of Least Privilege)
- `gmail.readonly` - Lectura de emails (APENAS lo necesario)
- `gmail.compose` - Composición de emails (si se necesita en Gmail)
- `gmail.labels` - Para categorizar/marcar emails
- ❌ No `gmail.modify` (evitar borrados accidentales)

### 1.3 Temporalidad y Revocación
- **Token TTL:** Máx 1 hora para operaciones
- **Report expira:** 48h (pre-signed URL)
- **Revocación automática:** Post-entrega (webhook cleanup)
- **No almacenamiento:** Sin snapshots de emails en BD

### 1.4 Logging Seguro
- ✅ Log: "Acceso a Gmail autorizado para usuario X"
- ❌ Log: Contenido de emails
- ❌ Log: Tokens o credenciales

---

## 2. OAUTH2 GMAIL SETUP - Google Cloud

### 2.1 Habilitar Gmail API
1. Google Cloud Console → APIs & Services
2. Enable "Gmail API"
3. Create "OAuth 2.0 Client ID" (Web application)

### 2.2 OAuth Consent Screen
- **Type:** External (or Internal si es empresa)
- **Scopes:** `gmail.readonly`, `gmail.compose`, `gmail.labels`
- **Redirect URI:** `https://oauth.n8n.cloud/oauth2/callback`

### 2.3 n8n Configuration
1. Ir a Credentials en n8n
2. Seleccionar "Gmail"
3. Elegir "OAuth2" (NO "Service Account")
4. Hacer click "Sign in with Google"
5. Autorizar scopes solicitados

**Resultado:** Credencial OAuth2 guardada en n8n (sin passwords, solo tokens)

---

## 3. WORKFLOW NODES - Flujo Completo

### 3.1 Nodos del Workflow MVP

```
[1] Manual Trigger
     ↓
[2] Send Email (Invitación)
     ├─ To: usuario@example.com
     ├─ Subject: "Autorización análisis COIPO"
     ├─ Body: Link + botón "OK"
     └─ Via: Gmail OAuth2
     ↓
[3] Webhook (Recibe confirmación "OK")
     ├─ URL: https://coipo.webhook/auth/ok
     ├─ Payload: { user_id, consent_timestamp }
     └─ Trigger: Cuando usuario hace click
     ↓
[4] HTTP Request (Obtener access token)
     ├─ From: Webhook  
     ├─ Method: POST
     ├─ Endpoint: https://oauth.n8n.cloud/oauth2/callback
     └─ Response: access_token (1h TTL)
     ↓
[5] Gmail Get Many (Readonly)
     ├─ Gmail Credential: OAuth2
     ├─ Filter: "newer_than:30d"
     ├─ Max results: 100
     └─ Fields: subject, from, date, snippet (NO full body)
     ↓
[6] Analysis Node (Custom/LLM)
     ├─ Input: Email snippets
     ├─ Logic: Heurísticas + LLM si aplica
     ├─ Output: insights, alerts, recommendations
     └─ TTL: 5 min (temp memory only)
     ↓
[7] Generate Report HTML
     ├─ Template: report_template.html
     ├─ Data: { user, insights, alerts, actions }
     ├─ Sign: Firmado con HS256
     ├─ URL: Pre-signed S3/bucket link (48h expiry)
     └─ Output: { report_url, expires_at }
     ↓
[8] Send Email (Entrega)
     ├─ To: usuario@example.com
     ├─ Subject: "Tu informe COIPO está listo"
     ├─ Body: "Tu informe: [link] Válido por 48h"
     └─ Via: Gmail OAuth2
     ↓
[9] Revoke Access + Cleanup
     ├─ Revoke: GET https://accounts.google.com/o/oauth2/revoke
     ├─ Params: token=<access_token>
     ├─ Delete: temp files, snapshots
     ├─ Log: "Access revoked for user X"
     └─ Webhook notify: cleanup_complete
```

### 3.2 Inputs/Outputs por Nodo

| Nodo | Input | Output | Notes |
|------|-------|--------|-------|
| Manual Trigger | {} | { trigger_id, timestamp } | Inicia workflow |
| Send Email (Inv) | { to, template } | { status, message_id } | OAuth2 sign |
| Webhook | HTTP POST | { consent, user_id } | Valida firma |
| Get Token | { code } | { access_token, expires_in } | 1h TTL |
| Gmail Get Many | { token, filter } | [ emails ] | readonly |
| Analysis | [ emails ] | { insights, risks } | Temp memory |
| Report Gen | { insights } | { url, expires_at } | Pre-signed |
| Send Email (Report) | { to, report_url } | { status } | Final delivery |
| Revoke + Cleanup | { token } | { revoked, cleaned } | TTL reset |

---

## 4. EMAIL TEMPLATES

### 4.1 Plantilla de Invitación

```
Subject: Análisis confidencial COIPO - Autorización requerida

Hola [nombre],

Necesitamos tu autorización para analizar tus emails de los últimos 30 días.

>> [BOTÓN: AUTORIZAR] <<
Link: https://coipo.webhook/auth/ok?user_id=X&token=Y&expires_at=Z

Notas:
- No modificaremos ni borraremos tus emails
- Tu información se elimina después del análisis
- Acceso se revoca automáticamente en 48h

Si no autorizas, puedes ignorar este email.

COIPO Team
```

### 4.2 Plantilla de Entrega del Informe

```
Subject: Tu informe COIPO está listo

Hola [nombre],

Tu análisis fue completado. Accede al informe:

>> [BOTÓN: VER INFORME] <<
Link: [pre-signed-url]

⏰ Este link expira en: 48 horas

Resumen:
- Alertas detectadas: N
- Acciones sugeridas: N
- Confianza: 95%

COIPO Team
```

### 4.3 Plantilla de Cierre (Revocación)

```
Subject: Acceso COIPO revocado (automático)

Hola [nombre],

Se revocó automáticamente el acceso a tu Gmail.
Tus datos fueron eliminados.

Esta es una confirmación automática.
No requiere acción.

COIPO Team
```

---

## 5. REPORT CONTRACT - Estructura del Informe

### 5.1 Estructura JSON del Informe

```json
{
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "generated_at": "2025-12-17T19:30:00Z",
    "expires_at": "2025-12-19T19:30:00Z"
  },
  "executive_summary": "Análisis de 87 emails de últimos 30 días.",
  "key_alerts": [
    { "severity": "high", "message": "Alert 1" },
    { "severity": "medium", "message": "Alert 2" }
  ],
  "actions_now": ["Action 1", "Action 2"],
  "actions_today": ["Action 3"],
  "actions_this_week": ["Action 4"],
  "suggested_messages": [ "Msg 1", "Msg 2" ],
  "confidence": 0.95,
  "signature": "HS256(payload)"
}
```

### 5.2 Reglas de Privacidad en Informe
- ❌ NO incluir cuerpo completo de emails
- ❌ NO guardar referencias a remitentes sensibles
- ✅ SI incluir tendencias/patrones anónimos
- ✅ SI incluir timestamps (sin contenido)
- **Retención:** Auto-delete después de expires_at

---

## 6. REVOCATION & CLEANUP

### 6.1 Proceso de Revocación

```
POST https://accounts.google.com/o/oauth2/revoke
?token=<access_token>

Response:
200 OK → Token revocado  
400 Bad Request → Token ya expirado (ok)
```

### 6.2 Limpieza de Temporales

- [ ] Eliminar snapshots de emails
- [ ] Eliminar logs con personal data
- [ ] Eliminar archivos temporales (temp/)
- [ ] Notificar webhook cleanup_complete
- [ ] Guardar SOLO: { user_id, timestamp, status: "revoked" }

### 6.3 Logs Seguros (Post-Cleanup)

```
2025-12-17T19:35:00Z - OAuth token revoked for user_123
2025-12-17T19:35:02Z - Temp files deleted (5 files, 2.3MB)
2025-12-17T19:35:03Z - Cleanup webhook notified
Status: SUCCESS
```

---

## 7. IMPLEMENTATION CHECKLIST

- [x] Crear repo coipo-orchestrator
- [x] Documentar MVP overview
- [ ] Crear Google Cloud project
- [ ] Habilitar Gmail API
- [ ] Configurar OAuth consent screen
- [ ] Crear n8n workflow (mock)
- [ ] Implementar webhook /auth/ok
- [ ] Crear template de informe
- [ ] Implementar revocación
- [ ] Tests e2e (sin passwords)
- [ ] Deployment docs

---

## 8. REFERENCIAS

- [Gmail API Scopes](https://developers.google.com/gmail/api/auth/scopes)
- [OAuth2 Revocation](https://developers.google.com/identity/protocols/oauth2/revocation)
- [n8n Gmail Integration](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail/)
- [Pre-signed URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html)

---

**Fin de especificación.**
