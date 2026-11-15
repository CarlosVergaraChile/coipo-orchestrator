# Handoff permanente — NovisEye y orquestación multi-IA
Fecha de corte 2026-11-14. Este documento es fuente de contexto para un chat nuevo; verificar siempre estado vivo.

## Prompt para retomar
> Actúa como director de producto de Ingeniería de Gestión. Lee este archivo y verifica GitHub antes de trabajar. No empieces de cero. Prioriza ventas B2B2B Chile, NovisEye V17, preservación de perspectivas por gerencia, QA adversarial y pruebas de orquestación. No modificar main ni producción ni contactar a Novis sin autorización. Recupera circuito Zapier→GitHub→Gemini→GitHub; reporta implementado/probado/publicado/validado comercialmente por separado.

## Reglas permanentes de producto
- Ofrecer módulos complementarios a operadores/proveedores existentes; no reemplazar sus sistemas sin justificación.
- Una situación, un conjunto de datos y múltiples perspectivas gerenciales coherentes: CEO, CFO, Riesgos, Legal, Tecnología, Operaciones, Personas y roles sectoriales.
- Benchmark competitivo obligatorio antes de construir; no inventar diferenciación.
- Separar costos reales, estimaciones, exposiciones contingentes y beneficios demostrados.
- Preservar IP y reutilización del motor común; modelos causales especializados por vertical.
- No agendar reunión de alto valor sin demo offline reproducible, pruebas, evidencias, respaldo y ensayo adversarial.

## NovisEye
- V16 en `CarlosVergaraChile/salmon/main:portfolio_publish/finanzas/novis/novis_v16.html`. Seis vistas por gerencia, simulador y reportes implementados en código; QA real no comprobada.
- Parser CSV usa split(','); no admite comillas/comas correctamente. Modelo `simulate` estima margen del operador AMS, no EBITDA del banco. Métricas promocionales son sintéticas/no acreditadas. PDF vinculados sin verificar.
- Añadir séptima perspectiva Riesgos/Continuidad y mantener seis actuales.
- Propuesta piloto V17 PR https://github.com/CarlosVergaraChile/salmon/pull/60
- Política transversal PR https://github.com/CarlosVergaraChile/salmon/pull/61
- Benchmark PR https://github.com/CarlosVergaraChile/salmon/pull/59
- Paquetes Claude/Gemini/DeepSeek/Perplexity PR https://github.com/CarlosVergaraChile/salmon/pull/62 — preparados, NO enviados.
- Relación personal con gerente general de Novis: una sola oportunidad; no solicitar reunión sin QA y validación.

## Orquesta existente
- Repositorio `CarlosVergaraChile/coipo-orchestrator`; rama `feat/ai-dispatch-bridge-20261113`, archivo `integrations/dispatch_ai.py`: proveedores permitidos claude, gemini, deepseek, perplexity, manus. Dry-run por defecto; envío requiere `IDG_AUTOMATION_WEBHOOK` y `IDG_AUTOMATION_TOKEN`. No hay prueba de configuración del webhook en esta revisión.
- Workflow `.github/workflows/orquesta-gemini-qa.yml` en main: acepta issues sintéticas con título exacto y propietario o workflow_dispatch, consulta Gemini con `GEMINI_API_KEY`, comenta y evita duplicados.
- **Evidencia positiva:** issue https://github.com/CarlosVergaraChile/coipo-orchestrator/issues/5 y ejecución https://github.com/CarlosVergaraChile/coipo-orchestrator/actions/runs/43529505808 : comentario de github-actions[bot] con respuesta Gemini 'El equipo completó el 80% de las tareas'.
- Issues #7 y #9 tienen título de prueba Zapier; **no demuestran por sí mismas** que Zapier las haya creado. Revisar autor/logs/historial.
- Seguimiento: issue #1 integración, #3 Zapier, #2 recuperación n8n.
- Estado: tramo GitHub→Gemini→GitHub **probado una vez**; Zapier→GitHub y Claude/DeepSeek/Perplexity/Manus **no verificados** en esta sesión.
- Siguiente tarea: comprobar origen de issues #7/#9, estado real del Zap, pruebas dry-run del puente y luego un roundtrip sintético idempotente. No disparar costos ni operaciones productivas sin control.

## Otros colaboradores
Claude trabaja AquaEye; Kodee trabaja homepage Hostinger; no interferir. Gemini benchmarking, DeepSeek red team y Perplexity fact-check son encargos preparados pero no demostrados como despachados.

## Verticales
NovisEye, AquaEye, HealthEye, EAS Conecta, Core Intelligence, Umbral/EquifaxEye. Aplicar B2B2B y perspectivas gerenciales por industria. No afirmar validación comercial sin evidencia.

## Seguridad y estado
Nunca guardar credenciales en issues/prompts/repos. No usar datos bancarios/pacientes reales sin autorización. No fusionar PRs ni publicar producción sin permiso. Un documento versionado es propuesta, no política vigente en main hasta su aprobación.
