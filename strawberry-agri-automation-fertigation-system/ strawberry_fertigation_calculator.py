# =============================================================================
# MIT License
#
# Copyright (c) 2026 Strawberry Agri-Automation Fertigation System (SAAFS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# =============================================================================
#
# Project   : Strawberry Agri-Automation Fertigation System (SAAFS)
# Module    : strawberry_fertigation_calculator.py
# Author    : SAAFS Engineering Team
# Version   : 1.0.0
# Created   : 2026-06-01
# License   : MIT
#
# Description:
#   This module implements the core calculation engine for strawberry open-field 
#   fertigation based on the SAAFS solid powder nutrient architecture.
#   It supports dynamic scaling for three major growth stages under any target 
#   water volume. Ideal for AIoT platform integration, local debugging, and 
#   field-level fertigation guidance.
#
# SAAFS Raw Material Index:
#   A — Calcium Nitrate Tetrahydrate (g)  |  B — Potassium Nitrate             (g)
#   C — Potassium Sulfate            (g)  |  D — Monopotassium Phosphate      (g)
#   E — Magnesium Sulfate Heptahydrate(g) |  F — EDTA-Ca                      (g)
#   G — EDTA-Mg                      (g)  |  H — Chelated Iron Solution       (ml)
#   I — Complex Micronutrient Sol.   (ml)
# =============================================================================

from __future__ import annotations

import textwrap
from dataclasses import dataclass, field
from typing import Dict, Optional


# ---------------------------------------------------------------------------
# Data Structure Definitions
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Ingredient:
    """
    Descriptor for a single SAAFS raw material.

    Attributes:
        name_en (str):   English full name of the raw material.
        name_abbr (str): Alphabetical abbreviation (A-I).
        unit (str):      Measurement unit, 'g' for solids, 'ml' for liquids.
    """
    name_en: str
    name_abbr: str
    unit: str


@dataclass
class StageFormula:
    """
    Data container for a single growth stage formula.

    Attributes:
        stage_id (int):         Stage identifier (1-3).
        stage_name (str):       Name of the growth stage.
        target_ec (float):      Target Electrical Conductivity in mS/cm.
        base_volume_l (float):  Baseline water volume for this formula in Liters (L).
        dosages (Dict[str, float]):
            Raw material dosage dictionary where keys are abbreviations ('A'–'I')
            and values are the dosages (g or ml) under the baseline water volume.
    """
    stage_id: int
    stage_name: str
    target_ec: float
    base_volume_l: float
    dosages: Dict[str, float] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Core Calculator Class
# ---------------------------------------------------------------------------

class StrawberryFertigationCalculator:
    """
    SAAFS Solid Powder Nutrient Architecture — Strawberry Lifecycle Calculator.

    This class encapsulates the core formula datasets for three critical growth 
    stages of open-field strawberries, providing linear scaling calculations and 
    formatted recipe printouts based on any target water volume.

    Typical usage::

        calc = StrawberryFertigationCalculator()

        # Query the batch sheet for Stage 2 (Flowering & Fruit Set) at 250 L target volume
        result = calc.calculate(stage_id=2, target_volume_l=250.0)
        calc.print_recipe(result)

    Raises:
        ValueError: If stage_id is out of bounds or target_volume_l is non-positive.
        TypeError:  If target_volume_l cannot be converted to a float.
    """

    # ------------------------------------------------------------------
    # SAAFS Raw Material Catalog — Immutable runtime reference
    # ------------------------------------------------------------------
    INGREDIENT_CATALOG: Dict[str, Ingredient] = {
        "A": Ingredient("Calcium Nitrate Tetrahydrate",  "A", "g"),
        "B": Ingredient("Potassium Nitrate",             "B", "g"),
        "C": Ingredient("Potassium Sulfate",             "C", "g"),
        "D": Ingredient("Monopotassium Phosphate",        "D", "g"),
        "E": Ingredient("Magnesium Sulfate Heptahydrate", "E", "g"),
        "F": Ingredient("EDTA-Ca",                       "F", "g"),
        "G": Ingredient("EDTA-Mg",                       "G", "g"),
        "H": Ingredient("Chelated Iron Solution",        "H", "ml"),
        "I": Ingredient("Complex Micronutrient Sol.",    "I", "ml"),
    }

    # ------------------------------------------------------------------
    # Strawberry Core Formula Dataset (Baseline: 100 L Pure Water)
    #
    # ★ Agricultural Engineering Notes ★
    #
    # 【Physiological Basis for Aggressive Scaling of C (K2SO4) and D (KH2PO4) 
    #   in Stage 2 & Stage 3】
    #
    # Potassium (K) is the core mineral element governing fruit expansion and quality:
    #   1. Osmoregulation & Carbohydrate Accumulation: K⁺ participates in phloem 
    #      sucrose loading, directly driving the translocation of photoassimilates 
    #      to the sink (fruit), significantly boosting Total Soluble Solids (Brix).
    #   2. Turgor & Cell Wall Rigidity: K⁺ maintains cell turgor pressure, promoting 
    #      fruit cell expansion, aligning single-fruit weight with cosmetic marketability.
    #   3. Phosphorus (P) Synergy: Monopotassium Phosphate (D) supplies both P and K. 
    #      P enhances pollen viability, fertilization rates, and early embryo development 
    #      during flowering; it then powers ATP synthesis during expansion, providing the 
    #      energetic substrate for active carbohydrate accumulation.
    #   4. Chloride-Free Potassium: Potassium Sulfate (C) serves as a zero-chloride K source, 
    #      evading the negative impacts of Cl⁻ on strawberry quality (excessive acidity, 
    #      pericarp thinning), while providing Sulfur (S) for protein and terpene (aroma) synthesis.
    # ------------------------------------------------------------------
    _STAGE_FORMULAS: Dict[int, StageFormula] = {
        1: StageFormula(
            stage_id=1,
            stage_name="Vegetative Growth",
            target_ec=1.2,
            base_volume_l=100.0,
            dosages={
                "A": 55.0,   # Calcium Nitrate  — Primary N + Ca source, reinforcing cell walls
                "B": 18.0,   # Potassium Nitrate — Dual N-K supply, maintaining baseline vegetative K
                "C":  0.0,   # Potassium Sulfate — Omitted in early stage to limit root-inhibiting salinity
                "D": 11.0,   # Monopotassium Phosphate — Structural P for root growth and ATP energetics
                "E": 27.0,   # Magnesium Sulfate — Magnesium source, the core of chlorophyll for photosynthetics
                "F":  2.0,   # EDTA-Ca           — Chelated calcium targeting fast-transpiring tissues
                "G":  3.6,   # EDTA-Mg           — Chelated magnesium buffering sulfate availability fluxes
                "H": 200.0,  # Chelated Iron     — Fe drives chlorophyll assembly and electron transport
                "I": 100.0,  # Micronutrients    — Full spectrum trace element replenishment (Mn/Zn/B/Cu/Mo)
            },
        ),
        2: StageFormula(
            stage_id=2,
            stage_name="Flowering & Fruit Set",
            target_ec=1.6,
            base_volume_l=100.0,
            dosages={
                "A": 52.8,   # Calcium Nitrate   — Moderated N, sustained Ca to prevent blossom-end rot
                "B": 12.0,   # Potassium Nitrate  — Shifting N:K balance in favor of Potassium sink
                "C": 14.4,   # Potassium Sulfate  ★ Escalated from 0 to 14.4g to initiate sugar paths
                "D": 22.0,   # Monopotassium Phosphate ★ Doubled: optimizes pollen viability and early embryogenesis
                "E": 50.4,   # Magnesium Sulfate  — Heightened Mg: covers peak photosynthetic demand during fruit set
                "F": 34.0,   # EDTA-Ca           ★ Sharp spike: safeguards fruit firmness and skin integrity
                "G":  0.0,   # EDTA-Mg           — Magnesium covered by bulk sulfate; chelate phases out
                "H": 250.0,  # Chelated Iron     — Elevated: Fe-enzymes catalyze anthocyanin synthesis for coloring
                "I": 100.0,  # Micronutrients    — Maintaining full-spectrum trace element homeostasis
            },
        ),
        3: StageFormula(
            stage_id=3,
            stage_name="Fruit Expansion & Harvest",
            target_ec=1.8,
            base_volume_l=100.0,
            dosages={
                "A": 44.0,   # Calcium Nitrate   — Minimal N stage; structural Ca preserves shelf-life
                "B":  6.0,   # Potassium Nitrate  — Lowest N:K ratio to keep Potassium completely dominant
                "C": 21.0,   # Potassium Sulfate  ★ Lifecycle Peak: Maximizes cell turgor and sizing
                "D": 24.0,   # Monopotassium Phosphate ★ Lifecycle Peak: Drives ATP-dependent phloem loading
                "E": 55.8,   # Magnesium Sulfate  — Peak Mg level: maintains high photosynthetic velocity
                "F": 50.0,   # EDTA-Ca           ★ Peak Calcium: Critical factor for post-harvest crunch and quality
                "G":  0.0,   # EDTA-Mg           — Extinguished; bulk magnesium coverage remains sufficient
                "H": 250.0,  # Chelated Iron     — Sustained high Fe levels to maintain persistent leaf greenness
                "I": 100.0,  # Micronutrients    — Guarding enzyme system integrity through harvest ripples
            },
        ),
    }

    _VALID_STAGE_IDS: tuple[int, ...] = (1, 2, 3)

    # ------------------------------------------------------------------
    # Public Interface
    # ------------------------------------------------------------------

    def get_stage_formula(self, stage_id: int) -> StageFormula:
        """Retrieves the raw baseline formula object (100L reference) for a given stage."""
        self._validate_stage_id(stage_id)
        return self._STAGE_FORMULAS[stage_id]

    def calculate(
        self,
        stage_id: int,
        target_volume_l: float,
        custom_base_volume_l: Optional[float] = None,
    ) -> Dict[str, object]:
        """Computes linearly scaled raw material dosages for any arbitrary target water volume."""
        self._validate_stage_id(stage_id)
        target_volume_l = self._validate_volume(target_volume_l, param_name="target_volume_l")

        formula: StageFormula = self._STAGE_FORMULAS[stage_id]

        base_vol: float = (
            self._validate_volume(custom_base_volume_l, param_name="custom_base_volume_l")
            if custom_base_volume_l is not None
            else formula.base_volume_l
        )

        scale_factor: float = target_volume_l / base_vol

        scaled_dosages: Dict[str, float] = {
            key: round(dosage * scale_factor, 4)
            for key, dosage in formula.dosages.items()
        }

        return {
            "stage_id":        stage_id,
            "stage_name":      formula.stage_name,
            "target_ec":       formula.target_ec,
            "base_volume_l":   base_vol,
            "target_volume_l": target_volume_l,
            "scale_factor":    round(scale_factor, 6),
            "scaled_dosages":  scaled_dosages,
        }

    def print_recipe(
        self,
        result: Dict[str, object],
        show_base_reference: bool = True,
    ) -> None:
        """Prints the calculated batch results in a production-friendly format."""
        stage_id: int         = result["stage_id"]           # type: ignore[assignment]
        stage_name: str       = result["stage_name"]         # type: ignore[assignment]
        target_ec: float      = result["target_ec"]          # type: ignore[assignment]
        base_vol: float       = result["base_volume_l"]      # type: ignore[assignment]
        target_vol: float     = result["target_volume_l"]    # type: ignore[assignment]
        scale_factor: float   = result["scale_factor"]       # type: ignore[assignment]
        scaled: Dict[str, float] = result["scaled_dosages"]  # type: ignore[assignment]

        base_formula: StageFormula = self.get_stage_formula(stage_id)

        # ── Header ────────────────────────────────────────────────────────
        title = f"SAAFS Strawberry Batch Sheet — Stage {stage_id}: {stage_name}"
        width = 75
        print("\n" + "╔" + "═" * width + "╗")
        print("║" + title.center(width) + "║")
        print("╚" + "═" * width + "╝")

        # ── Operational Parameters ──────────────────────────────────────
        print(f"  {'Target Growth Stage':<22}: Stage {stage_id} — {stage_name}")
        print(f"  {'Target EC Value':<22}: ~{target_ec:.1f} mS/cm")
        print(f"  {'Baseline Volume':<22}: {base_vol:.1f} L")
        print(f"  {'Target Output Vol':<22}: {target_vol:.1f} L")
        print(f"  {'Scaling Factor':<22}: {scale_factor:.4f} ×")
        print("  " + "─" * (width - 2))

        # ── Table Header ────────────────────────────────────────────────
        if show_base_reference:
            print(f"  {'ID':<3}  {'Raw Material Name':<32}  {'Dosage':>10}  {'Unit':<4}  "
                  f"{'Base(100L)':>10}  {'Unit':<4}")
            print("  " + "─" * (width - 2))
        else:
            print(f"  {'ID':<3}  {'Raw Material Name':<32}  {'Dosage':>10}  {'Unit':<4}")
            print("  " + "─" * (width - 2))

        # ── Table Rows ──────────────────────────────────────────────────
        for key, ingredient in self.INGREDIENT_CATALOG.items():
            scaled_val:  float = scaled[key]
            base_val:    float = base_formula.dosages[key]
            unit:        str   = ingredient.unit

            if show_base_reference:
                print(
                    f"  {key:<3}  {ingredient.name_en:<32}"
                    f"  {scaled_val:>10.2f}  {unit:<4}"
                    f"  {base_val:>10.2f}  {unit:<4}"
                )
            else:
                print(
                    f"  {key:<3}  {ingredient.name_en:<32}"
                    f"  {scaled_val:>10.2f}  {unit:<4}"
                )

        # ── Operational Guidelines ────────────────────────────────────────
        print("  " + "─" * (width - 2))
        notes = textwrap.dedent(f"""\
            [Standard Operating Procedures]
            1. Weigh or measure each raw material independently based on the values above.
            2. Dissolution Sequence: Completely dissolve solid powders first (A→B→C→D→E→F→G), 
               then inject liquid solutions (H, I). Stir thoroughly until completely clear.
            3. Final EC Target ≈ {target_ec:.1f} mS/cm (Subject to physical validation, normalized to 25°C).
            4. pH Target: Adjust final tank mixture to 5.8–6.2 (Optimal nutrient absorption band).
            5. This batch sheet assumes pure water intake. If source water contains background minerals, 
               measure baseline background EC and subtract corresponding equivalents.
        """)
        for line in notes.strip().split("\n"):
            print(f"  {line}")
        print("╘" + "═" * width + "╛\n")

    def list_stages(self) -> None:
        """Prints an interactive summary overview of all available lifecycle stages."""
        print("\n┌─── SAAFS Strawberry Lifecycle Overview ────────────────────────────────┐")
        print(f"  {'ID':<4}  {'Stage Name':<24}  {'Target EC (mS/cm)':<22}  {'Base Volume'}")
        print("  " + "─" * 68)
        for sid, sf in self._STAGE_FORMULAS.items():
            print(
                f"  [{sid}]   {sf.stage_name:<24}  "
                f"~{sf.target_ec:.1f} mS/cm            "
                f"{sf.base_volume_l:.0f} L"
            )
        print("└────────────────────────────────────────────────────────────────────────┘\n")

    # ------------------------------------------------------------------
    # Internal Validation Methods (Private)
    # ------------------------------------------------------------------

    def _validate_stage_id(self, stage_id: int) -> None:
        if stage_id not in self._VALID_STAGE_IDS:
            raise ValueError(
                f"[SAAFS] Invalid Stage ID '{stage_id}'. "
                f"Allowed bounds are {self._VALID_STAGE_IDS}. "
                f"Verify input parameters."
            )

    @staticmethod
    def _validate_volume(value: object, param_name: str = "volume") -> float:
        try:
            vol = float(value)  # type: ignore[arg-type]
        except (TypeError, ValueError) as exc:
            raise TypeError(
                f"[SAAFS] Parameter '{param_name}' must be numeric. "
                f"Received type: {type(value).__name__!r} = {value!r}."
            ) from exc

        if vol <= 0:
            raise ValueError(
                f"[SAAFS] Parameter '{param_name}' must be strictly positive (> 0). "
                f"Received value: {vol}. Input actual liquid requirements in Liters."
            )
        return vol


# =============================================================================
# CLI Demonstration Entry Point
# =============================================================================

def _demo_single(calc: StrawberryFertigationCalculator, stage_id: int, volume: float) -> None:
    result = calc.calculate(stage_id=stage_id, target_volume_l=volume)
    calc.print_recipe(result, show_base_reference=True)


def main() -> None:
    calc = StrawberryFertigationCalculator()

    print("=" * 79)
    print("  SAAFS Solid Powder System · Strawberry Lifecycle Fertigation Calculator v1.0.0")
    print("  License: MIT | Application Domain: Open-Field Strawberry Precision Farming")
    print("=" * 79)

    calc.list_stages()

    print("\n[Scenario 1] Lifecycle Baseline Formulas (100 L Reference)")
    for sid in (1, 2, 3):
        _demo_single(calc, stage_id=sid, volume=100.0)

    print("\n[Scenario 2] Stage 3 Multi-Scale Vector — 250 L Target Volume Modification")
    _demo_single(calc, stage_id=3, volume=250.0)

    print("\n[Scenario 3] Exception Trapping & Boundary Telemetry")
    error_cases = [
        {"stage_id": 2, "target_volume_l": -50},
        {"stage_id": 2, "target_volume_l": "abc"},
        {"stage_id": 5, "target_volume_l": 100},
    ]
    for case in error_cases:
        try:
            calc.calculate(**case)  # type: ignore[arg-type]
        except (ValueError, TypeError) as exc:
            print(f"  ✗ Intercepted Expected Exception [{type(exc).__name__}]: {exc}")

    print("\n✓ Telemetry execution complete. For IoT platform integration, resolve calculate() directly.\n")


if __name__ == "__main__":
    main()