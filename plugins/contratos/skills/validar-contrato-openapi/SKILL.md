---
name: validar-contrato-openapi
description: Valida un contrato OpenAPI contra los lineamientos de APIs de la organizacion -nomenclatura de rutas, versionado en la URL, codigos de error obligatorios y cabeceras de trazabilidad-. Usalo cuando alguien pida revisar, validar o auditar una especificacion OpenAPI o Swagger, o antes de publicar una API nueva.
license: Proprietary
metadata:
  id: demo.sdlc.validar-contrato-openapi
  owner_team: squad-sdlc
  owner_contact: squad-sdlc@ejemplo.dev
  data_classification: internal
  status: draft
  version: "0.2.3"
  standard_version: "8.0.0"
---

# Validar un contrato OpenAPI contra los lineamientos de APIs de la organizacion

## Cuando usarlo

Antes de publicar una API nueva, o al revisar un `openapi.yaml` en un pull request.

## Que comprueba

1. **Versionado en la ruta** — toda ruta empieza por `/v{n}/`.
2. **Nomenclatura** — sustantivos en plural y kebab-case: `/v1/cuentas-corrientes`.
3. **Errores obligatorios** — cada operacion declara `400`, `401`, `500`.
4. **Trazabilidad** — cabecera `X-Request-Id` declarada como requerida.
5. **Sin datos reales** — los ejemplos no llevan numeros de cuenta ni documentos de identidad.
6. **Paginacion declarada** — toda operacion que devuelva una coleccion declara `limit` y `cursor`.
   Una coleccion sin tope crece con los datos: responde hoy y deja de responder cuando el volumen
   sube, y el sintoma aparece en produccion y no en la revision.

## Como reportarlo

Agrupa por severidad y **cita la ruta exacta** de cada hallazgo. Si no hay hallazgos, dilo en
una linea: no rellenes con prosa.

## Lo que NO debes hacer

- No reescribas el contrato: reporta. La correccion la decide el equipo dueno de la API.
- No inventes lineamientos que no esten en esta lista.
