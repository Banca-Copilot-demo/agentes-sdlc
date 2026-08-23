---
name: revisar-cobertura
description: "Revisa si los cambios de un pull request llevan pruebas que cubran lo que tocan, y nombra los caminos que quedan sin cubrir. Usalo cuando alguien pida revisar la cobertura de un cambio, pregunte si un PR necesita mas pruebas, o quiera saber que casos faltan antes de pedir revision."
license: Proprietary
allowed-tools: Bash(git:*) Read Grep
metadata:
  id: demo.sdlc.revisar-cobertura
  owner_team: squad-sdlc
  owner_contact: squad-sdlc@ejemplo.dev
  data_classification: internal
  status: draft
  version: "0.1.0"
  standard_version: "7.0.0"
---

# Revisar la cobertura de un cambio

No mide un porcentaje: busca **caminos sin cubrir**. Un 90 % de cobertura con el caso de error sin
probar es peor que un 60 % que cubre los tres caminos que importan.

## Como se hace

1. Saca lo que cambio: `git diff --name-only origin/main...HEAD`
2. Por cada archivo de codigo tocado, busca su archivo de pruebas correspondiente.
3. Compara lo que el cambio introduce con lo que las pruebas ejercitan.

## Que se reporta

Los caminos **no cubiertos**, nombrando el caso y no el archivo:

- una rama condicional nueva que ninguna prueba recorre
- un tipo de error nuevo que nada provoca
- un limite -- vacio, maximo, negativo -- que no se toca

Si todo lo que cambio esta cubierto, dilo en una linea y para. No inventes carencias para tener algo
que decir: un informe con hallazgos falsos ensena a ignorar el informe.
