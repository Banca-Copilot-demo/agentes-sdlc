"""El brazo de evaluacion ARRANCA SIEMPRE, aunque el gate determinista este en rojo.

EL DEFECTO QUE FIJA, MEDIDO en el commit `f6e00a1a` de este repositorio:

    failure  conformidad / validar
    skipped  comportamiento
    (ninguna linea de `Veredicto de comportamiento`)

Con la conformidad en `failure`, el job `comportamiento` se salto por su `needs:`. Y al saltarse EL
LLAMADOR, el workflow reutilizable no arranca: sus jobs internos NO SE MATERIALIZAN -- no emiten un
check-run «skipped», sencillamente no existen --. Como `comportamiento / Veredicto de comportamiento`
es comprobacion REQUERIDA del ruleset, GitHub se quedaba en «Expected — waiting for status»:
esperando indefinidamente un estado que ya nadie iba a emitir. La solicitud de cambio no quedaba
rechazada, quedaba ATASCADA.

El contraste esta en el commit `c44d21a`, con una celda de matriz en rojo: alli el veredicto SI se
emitio en `failure`, porque el brazo habia arrancado.

POR QUE UNA PRUEBA Y NO BASTA CON MIRARLO. `if: always()` junto a un `needs:` se lee como redundante
-- «ya depende de la conformidad, ¿para que quiere correr siempre?» -- y es exactamente la linea que
la proxima persona que ordene el archivo va a borrar por parecer sobrante. Su ausencia no rompe nada
visible: solo devuelve el gate al estado de atasco, y solo el dia que la conformidad falle.
"""
from __future__ import annotations

from pathlib import Path

import yaml

_VALIDAR = Path(__file__).resolve().parents[1] / "workflows" / "validar.yml"
_EVALUACION = "workflows/evaluar.yml"


def _jobs() -> dict:
    return yaml.safe_load(_VALIDAR.read_text(encoding="utf-8"))["jobs"]


def _job_que_evalua() -> tuple[str, dict]:
    for nombre, job in _jobs().items():
        if _EVALUACION in str(job.get("uses", "")):
            return nombre, job
    raise AssertionError(
        f"ningun job de `validar.yml` llama a `{_EVALUACION}`: o se retiro la evaluacion, o el "
        "`uses:` cambio de forma y esta prueba dejo de mirar nada")


def test_el_brazo_de_evaluacion_arranca_aunque_la_conformidad_falle():
    """SIN ESTO EL GATE SE ATASCA, no se pone en rojo. Un job saltado al menos reporta algo; una
    LLAMADA saltada no reporta nada, y la comprobacion requerida espera para siempre."""
    nombre, job = _job_que_evalua()

    assert "always()" in str(job.get("if", "")), (
        f"el job `{nombre}` no lleva `if: always()` (if={job.get('if')!r}): con la conformidad en "
        "rojo se salta, y con el se salta la llamada entera, asi que `Veredicto de comportamiento` "
        "-- comprobacion requerida -- no se emite y el pull request queda en «Expected — waiting "
        "for status» en vez de rechazado")


def test_el_orden_frente_a_la_conformidad_se_conserva():
    """LA MITAD QUE NO SE PUEDE PERDER AL ANADIR LA OTRA. `always()` desactiva la condicion, no la
    dependencia: sin el `needs:` la evaluacion correria EN PARALELO con el gate determinista, que es
    pagar inferencia sin esperar a saber si el formato del artefacto es siquiera valido -- el orden
    por COSTE CRECIENTE que estos controles defienden --."""
    nombre, job = _job_que_evalua()
    depende = job.get("needs") or []
    depende = [depende] if isinstance(depende, str) else depende

    assert "conformidad" in depende, (
        f"el job `{nombre}` ya no depende de `conformidad` (needs={depende!r}): la evaluacion "
        "arrancaria en paralelo al gate determinista y gastaria modelo sin saber si el artefacto "
        "esta bien formado")


def test_el_resultado_de_la_conformidad_llega_al_workflow_que_evalua():
    """EL CORTOCIRCUITO VIVE ALLA, PERO EL DATO SALE DE AQUI. El workflow reutilizable no ve los jobs
    de este archivo -- `needs` es local --, asi que sin este input arrancaria a evaluar igualmente y
    gastaria la cuota de inferencia en un artefacto cuyo formato el gate ya declaro roto. Con
    `always()` puesto y este input olvidado, el arreglo se vuelve un gasto."""
    nombre, job = _job_que_evalua()
    entradas = job.get("with") or {}

    assert "needs.conformidad.result" in str(entradas.get("conformidad", "")), (
        f"el job `{nombre}` no le pasa el resultado de la conformidad a la evaluacion "
        f"(with={entradas!r}): el workflow llamado no puede deducirlo, asi que evaluaria un "
        "artefacto que ya se sabe mal formado -- y su veredicto no podria salir `no_evaluable`")
