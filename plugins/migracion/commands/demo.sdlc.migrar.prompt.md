---
name: demo.sdlc.migrar
description: "Ejecuta la migracion Atlas a CNF sobre una estructura ya analizada, delegando en el agente migrador."
argument-hint: "ruta-de-salida (opcional)"
agent: demo.sdlc.migrador
model: claude-sonnet-4-6
metadata:
  id: demo.sdlc.migrar
  owner_team: squad-sdlc
  owner_contact: squad-sdlc@ejemplo.dev
  data_classification: internal
  status: draft
  version: "0.2.1"
  standard_version: "8.0.0"
---

# Migrar Atlas a CNF

Punto de entrada del paso de migracion. **Enruta al agente `demo.sdlc.migrador`**, que es quien
decide y produce los entregables; este archivo solo fija quien ejecuta y con que modelo.

## Antes de empezar

Comprueba que existe el analisis previo en la ruta de salida. Si no existe, **detente y dilo**:
migrar sin analisis produce un resultado que nadie puede revisar.

## Que produce

El proyecto CNF migrado en la ruta de salida, y un informe de lo que no se pudo migrar
automaticamente. **Lo segundo importa mas que lo primero**: es la lista de trabajo humano.
