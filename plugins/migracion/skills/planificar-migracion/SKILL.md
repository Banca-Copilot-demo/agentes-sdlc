---
name: planificar-migracion
description: "Planifica la migracion de un microservicio a la plataforma destino: inventaria dependencias, ordena los pasos y estima el esfuerzo. Usalo antes de empezar a migrar codigo, cuando alguien pregunte por donde empezar o pida un plan."
license: Proprietary
metadata:
  id: demo.sdlc.planificar-migracion
  owner_team: squad-sdlc
  owner_contact: squad-sdlc@ejemplo.dev
  status: draft
  version: "0.2.2"
  data_classification: internal
  standard_version: "8.0.0"
---

# Planificar una migracion

Inventaria las dependencias del servicio, ordena los pasos por riesgo y estima el esfuerzo.

## Que producir

Devuelve un plan con estas tres secciones, en este orden:

1. **Dependencias**, cada una clasificada con **una de estas dos palabras exactas**: `bloqueante` o
   `diferible`. Una dependencia es **bloqueante** si el servicio no arranca sin ella en la plataforma
   destino — y eso incluye el caso en que la dependencia **no existe** en destino, que es bloqueante
   igualmente y no una categoria aparte. No uses otras etiquetas por muy descriptivas que parezcan:
   quien lee el plan filtra por esas dos palabras, y un «no migra» o un «pendiente» deja la dependencia
   fuera de la cuenta de lo que impide arrancar.
2. **Pasos ordenados por riesgo**, del mas arriesgado al menos. El primer paso es siempre el que,
   si falla, obliga a replantear el resto: descubrirlo tarde es lo que hace fracasar una migracion.
3. **Esfuerzo estimado** por paso, en jornadas-persona y como rango, nunca como numero unico.

## Reglas

- **Nombra explicitamente lo que no se puede migrar.** Un plan que omite el componente que se queda
  atras se lee como completo y no lo es.
- **Ninguna estimacion sin su supuesto.** Un rango sin la condicion que lo sostiene no es una
  estimacion, es un deseo.
- **Si falta informacion para ordenar el riesgo, pidela** en vez de asumir un orden. Un plan con el
  orden equivocado es peor que no tener plan, porque se sigue.
