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


def test_el_brazo_de_evaluacion_sigue_llamandose_comportamiento():
    """LA OTRA MITAD DEL NOMBRE REQUERIDO. `comportamiento / Veredicto de comportamiento` se compone
    del ID de ESTE job y del `name:` del agregador del reutilizable; el ruleset lo exige por
    coincidencia EXACTA. Renombrar el job -- tentador ahora que el canal tambien valida -- deja la
    comprobacion requerida sin nadie que la emita, y el pull request se atasca en «Expected — waiting
    for status» en vez de rechazarse. MEDIDO: ese atasco ya ocurrio dos veces en este proyecto."""
    nombre, _ = _job_que_evalua()

    assert nombre == "comportamiento", (
        f"el job que llama a la evaluacion se llama `{nombre}`: la comprobacion pasaria a ser "
        f"`{nombre} / Veredicto de comportamiento` y el ruleset seguiria esperando la de "
        "`comportamiento`")


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


def _job_de_conformidad() -> tuple[str, dict]:
    for nombre, job in _jobs().items():
        if "workflows/validar.yml" in str(job.get("uses", "")):
            return nombre, job
    raise AssertionError("ningun job de `validar.yml` llama al gate determinista del estandar")


def test_el_trabajo_de_conformidad_sigue_llamandose_validar():
    """EL NOMBRE DE LA COMPROBACION REQUERIDA ES `conformidad / validar`, Y SE COMPONE DE DOS MITADES
    QUE VIVEN EN ARCHIVOS DISTINTOS: el ID de ESTE job y el `name:` del job del reutilizable. El
    ruleset la exige por coincidencia EXACTA de texto, asi que si cualquiera de las dos cambia, la
    comprobacion deja de emitirse con ese nombre y TODAS las solicitudes de cambio quedan bloqueadas
    para siempre en «Expected — waiting for status», esperando un estado que ya nadie enviara.

    MEDIDO: ese atasco ya ocurrio dos veces en este proyecto, y no se lee como un rechazo -- parece un
    fallo de la plataforma --. Aqui se fija la mitad que este repositorio controla.
    """
    nombre, _ = _job_de_conformidad()

    assert nombre == "conformidad", (
        f"el job del gate determinista se llama `{nombre}` y no `conformidad`: la comprobacion pasaria "
        f"a llamarse `{nombre} / validar` y el ruleset seguiria esperando `conformidad / validar`")


def test_la_conformidad_solo_corre_las_reglas_de_repositorio_en_una_solicitud_de_cambio():
    """LA MITAD QUE NO SE VE AL REPARTIR EL GATE. Las reglas de cada unidad se mudaron al canal de su
    unidad, que solo existe en una solicitud de cambio. Si este job pidiera `repositorio` tambien en el
    push a `main`, las unidades se quedarian SIN VALIDAR en la rama publicada -- en verde, porque nadie
    las estaria mirando --. Y si no pidiera nada, cada unidad se validaria DOS veces en cada pull
    request: aqui y en su canal."""
    _, job = _job_de_conformidad()
    alcance = str((job.get("with") or {}).get("alcance", ""))

    assert "repositorio" in alcance and "pull_request" in alcance, (
        f"el alcance del gate determinista es {alcance!r}: tiene que pedir `repositorio` en una "
        "solicitud de cambio -- donde cada unidad tiene su canal -- y el recorrido completo fuera de "
        "ella, donde no hay canales que validen las unidades")


def test_la_evaluacion_recibe_los_secretos_que_necesita_para_comprobar_el_dueno():
    """LA REGLA QUE SE DEBILITA EN SILENCIO AL MUDAR LA VALIDACION. G4 exige que el `owner_team`
    declarado EXISTA en la organizacion, y el `GITHUB_TOKEN` de Actions no puede leer los equipos --
    responde 403, MEDIDO --: sin un token de la App, el validador no comprueba y degrada a AVISO.

    Ahora que la validacion por unidad corre dentro de los canales, olvidarlos aqui no rompe nada
    visible: el gate sigue en verde y un artefacto con un dueño inexistente se publica igual. Es
    exactamente la clase de fallo que este repositorio persigue -- un control en verde que no protege
    nada --."""
    nombre, job = _job_que_evalua()
    secretos = job.get("secrets") or {}

    for secreto in ("app-id", "app-key"):
        assert secreto in secretos, (
            f"el job `{nombre}` no le pasa `{secreto}` a la evaluacion (secrets={sorted(secretos)}): "
            "la validacion de cada unidad corre alli y no podria resolver los equipos de la "
            "organizacion, asi que un `owner_team` inexistente pasaria de ERROR a aviso")
