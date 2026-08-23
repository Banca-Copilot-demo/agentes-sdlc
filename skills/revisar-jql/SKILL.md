---
name: revisar-jql
description: Revisa una consulta JQL de Jira y senala los filtros que faltan, las proyecciones excesivas y las clausulas que degradan el rendimiento. Usalo cuando alguien escriba o pegue una consulta JQL, o pida optimizar una busqueda de incidencias.
license: Proprietary
metadata:
  id: demo.sdlc.revisar-jql
  owner_team: squad-sdlc
  owner_contact: squad-sdlc@ejemplo.dev
  data_classification: internal
  status: draft
  version: "1.0.0"
  standard_version: "8.0.0"
---

# Revisar una consulta JQL

Artefacto **suelto a proposito**: vive en la raiz del repositorio, fuera de todo plugin, conviviendo
con los cuatro plugins de `plugins/`. Demuestra que un repositorio de dominio no obliga a elegir: se
puede empaquetar lo que convenga distribuir junto y dejar suelto lo que no.

## Cuando NO conviene empaquetarlo

Este skill no depende de nada ni orquesta nada: se consulta y ya. Meterlo en un plugin obligaria a
quien quiere solo esto a instalar todo el conjunto, y cargaria el `description` de sus vecinos en cada
peticion. El plugin es una decision de empaquetado, y aqui la respuesta es que no hace falta.

Lo que se pierde por estar suelto es una sola cosa: **no tiene entrada en el marketplace**, porque las
entradas de un marketplace son plugins. Todo lo demas lo conserva -- dueno, version, estado, etiqueta,
paquete, atestacion y ficha en el catalogo -- porque el gobierno viaja en su propia metadata.

## Que comprobar en una consulta

**Filtro de proyecto ausente.** Una consulta sin `project = ` recorre todos los proyectos de la
instancia. Es el defecto que mas cuesta y el mas facil de pasar por alto, porque la consulta funciona:
solo tarda.

**Orden sin indice.** `ORDER BY` sobre un campo personalizado obliga a ordenar en memoria despues de
traer el conjunto entero.

**Negaciones amplias.** `status != Done` no puede usar el indice de estado: describe todo menos una
cosa. Cuando se conocen los estados de interes, enumerarlos con `IN` es mas rapido y ademas mas claro
de leer.

**Comodin por delante.** `summary ~ "*pago"` no aprovecha el indice de texto. Con el comodin al final
si.

## Que devolver

La consulta reescrita y, por cada cambio, **por que** era un problema. Una consulta corregida sin la
razon se copia una vez y el mismo defecto reaparece en la siguiente.
