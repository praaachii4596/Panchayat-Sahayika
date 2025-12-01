from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).resolve().parent
# CSV_PATH = BASE_DIR / "uttarakhand_infra_deficits.csv"

CSV_PATH = BASE_DIR / "uttarakhand_infra_deficits_pdi.csv"

# village_code ko string rakhte hain
df = pd.read_csv(CSV_PATH, dtype={"village_code": str})

app = FastAPI(title="Smart Gram Planning API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def deficit_level(x: float) -> str:
    """
    Deficit is assumed 0–1 or 0–100 scaled to 0–1.
    High = x >= 0.7, Medium >= 0.4, else Low.
    """
    if x is None:
        return "NA"
    if x >= 0.7:
        return "High"
    elif x >= 0.4:
        return "Medium"
    else:
        return "Low"


def theme_status(score: float) -> str:
    """
    Theme score is 0–100; higher is better.
    Simple interpretation:
    - >= 75: Strong
    - >= 50: Moderate
    - < 50: Weak
    """
    if score is None:
        return "NA"
    if score >= 75:
        return "Strong"
    elif score >= 50:
        return "Moderate"
    return "Weak"


def to_float(v):
    """Safe conversion: numpy scalar -> Python float, None safe."""
    if pd.isna(v):
        return None
    return float(v)


@app.get("/api/districts")
def get_districts():
    if "district_name" not in df.columns:
        raise HTTPException(
            status_code=500,
            detail=f"Column 'district_name' missing in CSV. Columns: {list(df.columns)}",
        )

    districts = sorted(df["district_name"].dropna().unique().tolist())
    return {"districts": districts}


@app.get("/api/villages")
def get_villages(district: str):
    required_cols = [
        "district_name",
        "village_code",
        "village_name",
        "gp_name",
        "block_name",
        "service_deficit_index",
        "pdi_village",
        "pdi_grade",
    ]
    for col in required_cols:
        if col not in df.columns:
            raise HTTPException(
                status_code=500,
                detail=f"Column '{col}' missing in CSV",
            )

    dfg = df[df["district_name"].str.upper() == district.upper()]
    if dfg.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No villages found for district {district}",
        )

    records = []
    for _, row in dfg.iterrows():
        records.append(
            {
                "village_code": str(row.get("village_code", "")),
                "village_name": row.get("village_name", ""),
                "gp_name": row.get("gp_name", ""),
                "block_name": row.get("block_name", ""),
                "district_name": row.get("district_name", ""),
                "service_deficit_index": to_float(
                    row.get("service_deficit_index", 0.0)
                ),
                "pdi_village": to_float(row.get("pdi_village", None)),
                "pdi_grade": row.get("pdi_grade", ""),
            }
        )

    # Ab sort karenge lowest PDI first (worst performing villages)
    records = sorted(
        records,
        key=lambda r: (r["pdi_village"] is None, r["pdi_village"] or 9999.0),
    )
    return {"villages": records}


@app.get("/api/village_detail")
def get_village_detail(village_code: str):
    required_cols = [
        "district_name",
        "block_name",
        "gp_name",
        "village_name",
        "village_code",
        "service_deficit_index",
        "health_deficit",
        "education_deficit",
        "sanitation_deficit",
        "road_deficit",
        "digital_deficit",
        "electricity_deficit",
        "pdi_village",
        "pdi_grade",
        "theme_water_sanitation_score",
        "theme_health_score",
        "theme_education_score",
        "theme_roads_score",
        "theme_digital_electricity_score",
        "theme_livelihood_score",
    ]
    for col in required_cols:
        if col not in df.columns:
            raise HTTPException(
                status_code=500,
                detail=f"Column '{col}' missing in CSV",
            )

    dfg = df[df["village_code"] == str(village_code)]
    if dfg.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Village not found for code {village_code}",
        )

    row = dfg.iloc[0]

    # Theme details
    themes = {
        "water_sanitation": {
            "score": to_float(row.get("theme_water_sanitation_score")),
            "status": theme_status(to_float(row.get("theme_water_sanitation_score"))),
        },
        "health": {
            "score": to_float(row.get("theme_health_score")),
            "status": theme_status(to_float(row.get("theme_health_score"))),
        },
        "education": {
            "score": to_float(row.get("theme_education_score")),
            "status": theme_status(to_float(row.get("theme_education_score"))),
        },
        "roads": {
            "score": to_float(row.get("theme_roads_score")),
            "status": theme_status(to_float(row.get("theme_roads_score"))),
        },
        "digital_electricity": {
            "score": to_float(row.get("theme_digital_electricity_score")),
            "status": theme_status(
                to_float(row.get("theme_digital_electricity_score"))
            ),
        },
        "livelihood": {
            "score": to_float(row.get("theme_livelihood_score")),
            "status": theme_status(to_float(row.get("theme_livelihood_score"))),
        },
    }

    # Agar theme_service_score column hai toh add it as well
    if "theme_service_score" in df.columns:
        themes["service"] = {
            "score": to_float(row.get("theme_service_score")),
            "status": theme_status(to_float(row.get("theme_service_score"))),
        }

    detail = {
        "district_name": row["district_name"],
        "block_name": row["block_name"],
        "gp_name": row["gp_name"],
        "village_name": row["village_name"],
        "village_code": str(row["village_code"]),
        "service_deficit_index": to_float(row["service_deficit_index"]),
        "pdi_village": to_float(row["pdi_village"]),
        "pdi_grade": row.get("pdi_grade", ""),
        "themes": themes,
        "deficits": {
            "health": {
                "score": to_float(row["health_deficit"]),
                "level": deficit_level(to_float(row["health_deficit"])),
            },
            "education": {
                "score": to_float(row["education_deficit"]),
                "level": deficit_level(to_float(row["education_deficit"])),
            },
            "sanitation": {
                "score": to_float(row["sanitation_deficit"]),
                "level": deficit_level(to_float(row["sanitation_deficit"])),
            },
            "roads": {
                "score": to_float(row["road_deficit"]),
                "level": deficit_level(to_float(row["road_deficit"])),
            },
            "digital": {
                "score": to_float(row["digital_deficit"]),
                "level": deficit_level(to_float(row["digital_deficit"])),
            },
            "electricity": {
                "score": to_float(row["electricity_deficit"]),
                "level": deficit_level(to_float(row["electricity_deficit"])),
            },
        },
    }

    return detail