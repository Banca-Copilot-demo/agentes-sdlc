---
name: demo.sdlc.revisar
description: "Lanza la revision del pull request actual delegando en el agente revisor del dominio."
argument-hint: "rama-base (opcional, por defecto main)"
agent: demo.sdlc.revisor
model: claude-sonnet-4-6
metadata:
  id: demo.sdlc.revisar
  owner_team: squad-sdlc
  owner_contact: squad-sdlc@ejemplo.dev
  data_classification: internal
  status: draft
  version: "0.1.0"
  standard_version: "7.0.0"
---

# Revisar el pull request actual

Punto de entrada por nombre. **Enruta al agente `demo.sdlc.revisor`**, que es quien decide y produce
los hallazgos; este archivo solo fija quien ejecuta y con que modelo.

Existe como `prompt` y no como `skill` por una razon concreta: se teclea. Quien revisa quiere lanzarlo
cuando decide revisar, no cuando el modelo crea que encaja.
