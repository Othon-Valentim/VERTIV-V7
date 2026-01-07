import os
import rasterio
import numpy as np
import json
from google.cloud import storage

# Configuração
BUCKET_NAME = os.getenv("BUCKET_NAME", "vertiv-spatial-data")
INPUT_FILE = os.getenv("INPUT_FILE", "dem.tif")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "vertiv-v6")


def calculate_slope(dem_array, cell_size):
    """Calcula declividade em graus usando gradiente numpy."""
    x, y = np.gradient(dem_array, cell_size, cell_size)
    slope_rad = np.arctan(np.sqrt(x * x + y * y))
    return np.degrees(slope_rad)


def process_dem():
    """Lê GeoTIFF do GCS (streaming), processa e salva metadados."""
    print(f"🌍 Iniciando processamento espacial: {INPUT_FILE}")

    # Simulação de leitura GCS (VSIGS)
    # gcs_path = f"/vsigs/{BUCKET_NAME}/{INPUT_FILE}"

    # Para teste local, vamos criar um array dummy se o arquivo não existir
    if not os.path.exists(INPUT_FILE):
        print("⚠️ Arquivo não encontrado localmente. Gerando terreno sintético...")
        dem_data = np.random.rand(100, 100) * 50  # Elevação 0-50m
        cell_size = 10.0  # 10m pixel
    else:
        with rasterio.open(INPUT_FILE) as src:
            dem_data = src.read(1)
            cell_size = src.transform[0]

    # Cálculo
    slope_map = calculate_slope(dem_data, cell_size)
    avg_slope = np.mean(slope_map)
    max_slope = np.max(slope_map)

    # Custo de Terraplanagem:
    # < 10 graus: 1.0x
    # 10-30 graus: 1.2x
    # > 30 graus: 1.5x

    flat_mask = slope_map < 10
    mod_mask = (slope_map >= 10) & (slope_map <= 30)
    steep_mask = slope_map > 30

    earthworks_factor = (
        np.sum(flat_mask) * 1.0 + np.sum(mod_mask) * 1.2 + np.sum(steep_mask) * 1.5
    ) / slope_map.size

    result = {
        "avg_slope_deg": float(avg_slope),
        "max_slope_deg": float(max_slope),
        "earthworks_factor": float(earthworks_factor),
        "status": "PROCESSED",
    }

    print(json.dumps(result, indent=2))

    # Aqui salvaríamos no Supabase ou GCS de volta
    return result


if __name__ == "__main__":
    process_dem()
