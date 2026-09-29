from __future__ import annotations
from pathlib import Path
import pandas as pd
from config import DEFAULT_TARGET_TABLE, DEFAULT_USUARIO_REGISTRO_ID, DEFAULT_SHEET_NAME
from .db import connect_from_path
from .db_questions import load_questions
from .excel_reader import read_excel_matrix
from .mapping import map_row_to_respuesta
from .repo import get_aplicacion_id

def _validate_table_name(table: str) -> str:
    t = table.strip()
    if not t or any(ch in t for ch in [";", "--", "/*", "*/"]):
        raise ValueError(f"Nombre de tabla no permitido: {table}")
    return t

def load_excel_to_sql(
    evaluacion_id: int,
    informante_id: int,
    excel_path: str | Path,
    db_config_path: str | Path,
    table: str = DEFAULT_TARGET_TABLE,
    usuario_registro_id: int = DEFAULT_USUARIO_REGISTRO_ID,
    sheet_name: str = DEFAULT_SHEET_NAME,
) -> int:
    table = _validate_table_name(table)
    aplicacion_id = get_aplicacion_id(evaluacion_id, informante_id, db_config_path)
    print(f"\n[INFO] Iniciando carga en {table} para AplicacionId: {aplicacion_id}")
    df_preg = load_questions(evaluacion_id=evaluacion_id, db_config_path=db_config_path)
    code_to_id = dict(zip(df_preg["PREGUNTA_CODIGO"], df_preg["ID_PREGUNTA"]))
    print(f"[OK] Preguntas maestras cargadas: {len(df_preg)}")
    df_xls = read_excel_matrix(Path(excel_path), sheet_name=sheet_name)
    print(f"[INFO] Filas en Excel encontradas: {len(df_xls)}")
    merge_sql = f"""
    MERGE INTO {table} AS target
    USING (SELECT ? AS AplicacionId, ? AS PreguntaId) AS source
    ON (target.AplicacionId = source.AplicacionId AND target.PreguntaId = source.PreguntaId)
    WHEN MATCHED THEN
      UPDATE SET 
        SituacionActual = CASE WHEN ISNULL(target.SituacionActual, '') <> '' THEN target.SituacionActual + CHAR(13) + CHAR(10) + CAST(? AS varchar(max)) ELSE CAST(? AS varchar(max)) END,
        Notas = CASE WHEN ISNULL(target.Notas, '') <> '' THEN target.Notas + CHAR(13) + CHAR(10) + CAST(? AS varchar(max)) ELSE CAST(? AS varchar(max)) END,
        RespuestaLiteral = CASE WHEN ISNULL(target.RespuestaLiteral, '') <> '' THEN target.RespuestaLiteral + CHAR(13) + CHAR(10) + CAST(? AS varchar(max)) ELSE CAST(? AS varchar(max)) END,
        UsuarioRegistroId = ?, FechaRegistro = GETDATE()
    WHEN NOT MATCHED THEN
      INSERT (AplicacionId, PreguntaId, SituacionActual, Notas, RespuestaLiteral, UsuarioRegistroId, FechaRegistro)
      VALUES (?, ?, CAST(? AS varchar(max)), CAST(? AS varchar(max)), CAST(? AS varchar(max)), ?, GETDATE());
    """
    rows_ok = 0
    with connect_from_path(db_config_path) as conn:
        cur = conn.cursor()
        for index, row in df_xls.iterrows():
            codigo = str(row.get("PREGUNTA_CODIGO", "")).strip()
            if not codigo or codigo not in code_to_id:
                continue
            pregunta_id = code_to_id[codigo]
            mapped = map_row_to_respuesta(row=row, pregunta_id=pregunta_id, aplicacion_id=aplicacion_id)
            print("-" * 50)
            print(f"CÓDIGO: {codigo} (ID: {pregunta_id})")
            print(f" > NOTAS:      {str(mapped['Notas'])[:80]}...")
            print(f" > LITERAL:    {str(mapped['RespuestaLiteral'])[:80]}...")
            print(f" > SITUACIÓN:  {str(mapped['SituacionActual'])[:80]}...")
            if not (mapped["Notas"] or mapped["RespuestaLiteral"] or mapped["SituacionActual"]):
                print("   [SALTO] Fila vacía, no se sube.")
                continue
            try:
                cur.execute(
                    merge_sql,
                    aplicacion_id, pregunta_id,
                    mapped["SituacionActual"], mapped["SituacionActual"],
                    mapped["Notas"], mapped["Notas"],
                    mapped["RespuestaLiteral"], mapped["RespuestaLiteral"],
                    usuario_registro_id,
                    aplicacion_id, pregunta_id,
                    mapped["SituacionActual"], mapped["Notas"], mapped["RespuestaLiteral"], usuario_registro_id
                )
                rows_ok += 1
            except Exception as e:
                print(f"[ERROR] Falló al insertar fila {index} (Código {codigo}): {e}")
        print(f"\n[INFO] Confirmando transacción en SQL ({rows_ok} filas procesadas)...")
        conn.commit()
    print(f"[EXITO] Proceso terminado. Datos guardados en AplicacionId: {aplicacion_id}")
    return rows_ok