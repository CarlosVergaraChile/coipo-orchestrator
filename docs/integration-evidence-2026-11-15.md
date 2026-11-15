# Registro de verificación de integraciones — 2026-11-15

Documento de control para **revisión**, no configuración ni activación de integraciones. No contiene credenciales.

## Niveles de evidencia

- **Histórica:** el propietario informa que existió una conexión, sin prueba de funcionamiento actual.
- **Acceso autenticado:** una consulta de solo lectura respondió mediante el conector.
- **Prueba extremo a extremo:** un evento de prueba recorre origen, orquestador y destino, con IDs correlacionados, resultado y logs depurados.
- **Pendiente:** no hay evidencia suficiente; no significa desconectado.

## Estado comprobado en esta sesión

| Sistema | Evidencia | Nivel |
| --- | --- | --- |
| GitHub | Lectura autenticada de repositorios coipo-orchestrator, salmon y cartera-staging y PR #11–#15 | Acceso autenticado |
| Google Drive | Consulta de perfil mediante conector | Acceso autenticado |
| HubSpot | Consulta de propietarios mediante conector | Acceso autenticado |
| Hostinger Mail | Consulta de cuenta mediante conector | Acceso autenticado; **no** equivale a hosting web |
| Lovable | Proyecto de revisión con estado is_published=true | Publicación declarada por proveedor; URL externa no probada aquí |
| Zapier | El propietario confirma conexiones previamente configuradas | Histórica; inventario y prueba pendientes |
| Hostinger web | El propietario confirma conexión previa | Histórica; despliegue/administración web no probados |
| Gemini | Existe trabajo previo de puente, sin prueba E2E en esta revisión | Pendiente |
| DeepSeek | PR #14 adaptador opt-in y #15 privacidad dry-run, sin API real | Pendiente |
| Claude, Manus, Perplexity, n8n | Sin prueba E2E en esta revisión | Pendiente |

## Secuencia segura para Zapier como concentrador

1. Inventariar **Zaps existentes** y conexiones autorizadas desde la cuenta del propietario. No duplicar cuentas.
2. Registrar para cada flujo: disparador, filtros, cuenta destino, alcance de permisos, modo de ejecución, costo, responsable y opción de desactivación; **nunca copiar tokens**.
3. Comprobar con datos sintéticos y sin activar acciones pagadas: evento de origen -> identificador de correlación -> enrutamiento en modo simulación -> recepción de resultado -> idempotencia.
4. Para GitHub Issues `[AI-TASK]`, verificar identidad del emisor, aprobación explícita, lista permitida de proveedores, límite de gasto, protección de secretos y control de duplicados persistente **antes** de habilitar envío real.
5. Verificar por separado acceso de Hostinger web, ruta de despliegue, permisos mínimos y reversión; no inferirlo de Hostinger Mail.
6. Guardar evidencia: enlace al PR/CI, ID de ejecución (sin datos privados), fecha, resultado, errores redactados y responsable.

## GitHub CI observado

- PR #12: workflow «Orquesta - contrato y dry run» completado con éxito, run 43662862187.
- PR #13: workflow «Orquesta - validar contrato de issues» completado con éxito, run 43683346754.
- PR #14 y #15: sin ejecuciones PR encontradas para los SHA consultados. No afirmar CI aprobado.
- No fusionar PR apilados sin revisar sus bases y dependencias.

## Criterio de cierre

Una conexión solo se reporta **operativa extremo a extremo** cuando existe prueba reproducible y sin secretos del flujo completo. El estado histórico y el acceso autenticado nunca sustituyen esa prueba.
