import io, json
import pandas as pd
from fastapi import UploadFile

from app.core.logging import setup_logging

logger = setup_logging()

async def file_parser(file: UploadFile) -> dict:
    """Parse uploaded file (CSV, Excel, JSON) to JSON structure."""
    try:
        contents = await file.read()
        filename = file.filename.lower()
        
        if filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
            return {
                "data": df.to_dict(orient='records'),
                "columns": list(df.columns),
                "row_count": len(df),
                "source": "csv_file"
            }
        
        elif filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(contents))
            return {
                "data": df.to_dict(orient='records'),
                "columns": list(df.columns),
                "row_count": len(df),
                "source": "excel_file"
            }
        
        elif filename.endswith('.json'):
            json_data = json.loads(contents.decode('utf-8'))
            # Handle both array and object formats
            if isinstance(json_data, list):
                return {
                    "data": json_data,
                    "row_count": len(json_data),
                    "source": "json_file"
                }
            else:
                return json_data
        
        else:
            raise ValueError(f"Unsupported file format: {filename}")
            
    except Exception as e:
        logger.error(f"File parsing error: {e}")
        raise ValueError(f"Could not parse file: {str(e)}")
