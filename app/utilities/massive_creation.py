import io
from datetime import date, datetime, timedelta
from typing import Dict, List

import pandas as pd
from fastapi import HTTPException, UploadFile


def process_excel(file: UploadFile) -> List[Dict]:
    """Procesa un archivo Excel y devuelve los datos estructurados."""
    try:
        # Leer el archivo Excel
        contents = file.file.read()  # Usar file.file para UploadFile
        df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")

        # Columnas requeridas y de bloques
        required_columns = [
            "id",
            "city",
            "service",
            "title_seo",
            "meta_description",
            "state",
            "key_phrase",
            "url",
            "review",
            "date",
        ]

        # Verificar columnas obligatorias
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise HTTPException(
                status_code=400,
                detail=f"Columnas obligatorias faltantes: {', '.join(missing_cols)}",
            )

        # Procesar bloques
        block_columns = [
            col for col in df.columns if col.endswith("_block")
        ]  # Cambiado a endswith
        df["blocks"] = df[block_columns].apply(
            lambda row: [
                col for col in block_columns if str(row[col]).strip().lower() == "x"
            ],
            axis=1,
        )

        # Limpieza y transformación de datos
        text_columns = ["title_seo", "service" ,"meta_description", "state", "key_phrase", "url"]
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
                if col in ["title_seo", "state", "key_phrase"]:
                    df[col] = df[col].str.title()

        # Procesamiento especial
        df["title_seo"] = df["title_seo"].str.replace(r"\s+", " ", regex=True)
        df["review"] = (
            pd.to_numeric(df["review"], errors="coerce").fillna(0).astype(int)
        )

        # Procesamiento de fechas
        try:
            df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y").dt.strftime(
                "%Y-%m-%d"
            )
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Formato de fecha inválido. Use dd/mm/yyyy"
            )

        # Seleccionar columnas finales
        result_columns = required_columns + ["blocks"]
        return df[result_columns].to_dict("records")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al procesar el archivo: {str(e)}"
        )


def massive_creation(data: List[Dict], create_function: callable) -> None:
    error_log = []
    success_ids = []

    for item in data:
        try:
            # Procesamiento de fecha (compatible con Excel y string)
            excel_date = item.get("date")
            processed_date = None

            if isinstance(excel_date, str):
                # Si es string, asumimos formato "YYYY-MM-DD" (salida de process_data)
                processed_date = datetime.strptime(excel_date, "%Y-%m-%d").date()
            elif isinstance(excel_date, (int, float)):
                # Si es numérico, convertimos desde fecha de Excel
                base_date = date(1899, 12, 30)  # Corrección para Excel
                processed_date = base_date + timedelta(days=float(excel_date))
            else:
                raise ValueError("Formato de fecha no reconocido")

            # Llamada a create_scheduled (versión mejorada)
            success = create_function(
                campaign_id=item.get("id"),
                city=item.get("city"),
                service=item.get("service"),
                title_seo=item.get("title_seo"),
                meta_description=item.get("meta_description"),
                state=item.get("state"),
                key_phrase=item.get("key_phrase"),
                url=item.get("url"),
                total_reviews=item.get("review", 150),
                blocks=item.get("blocks", []),
                date=processed_date.strftime("%Y-%m-%d"),
            )

            if success:
                success_ids.append(item.get("id"))
            else:
                error_log.append(f"Fallo al crear en ID {item.get('id')}")

        except Exception as e:
            error_log.append(f"Error en item {item.get('id')}: {str(e)}")

    # Guardar errores
    if error_log:
        with open("static/errors.txt", "a") as f:
            f.write(f"\n=== Batch {datetime.now()} ===\n")
            f.write("\n".join(error_log))

    return success_ids
