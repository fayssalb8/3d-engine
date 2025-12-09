"""
Configuration management for Machine Shop Suite - 3D Printing Quote Engine
"""
import os
import json
from pathlib import Path


class Config:
    """Application configuration with support for JSON file storage"""

    # Default slicer path - PrusaSlicer supports both FDM (--export-gcode) and SLA/DLP (--export-sla)
    DEFAULT_SLICER_PATH = "prusa-slicer"  # Assumes prusa-slicer is in PATH

    def __init__(self, config_file='config.json'):
        """Initialize configuration from file or defaults"""
        self.config_file = config_file
        self.config_data = self._load_config()

    def _load_config(self):
        """Load configuration from JSON file or return defaults"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config file: {e}")
                return self._default_config()
        return self._default_config()

    def _default_config(self):
        """Return default configuration"""
        return {
            "application": {
                "name": "Machine Shop Suite",
                "version": "1.0.0",
                "description": "3D Printing Quote Engine"
            },
            "slicer": {
                "path": os.getenv("PRUSA_SLICER_PATH", self.DEFAULT_SLICER_PATH),
                "timeout_seconds": 300
            },
            "materials": {
                "pla": {
                    "name": "PLA (Polylactic Acid)",
                    "type": "fdm",
                    "description": "Easy to print, biodegradable, good for prototypes",
                    "density_g_cm3": 1.24,
                    "price_per_kg": 800,
                    "per_gram_price": 1.0,
                    "bed_temp": 55,
                    "extruder_temp": 215,
                    "perimeter_speed": 100,
                    "infill_speed": 180,
                    "solid_infill_speed": 160,
                    "colors": ["White", "Black", "Red", "Blue", "Green", "Yellow", "Orange", "Gray"]
                },
                "abs": {
                    "name": "ABS (Acrylonitrile Butadiene Styrene)",
                    "type": "fdm",
                    "description": "Strong and durable, heat resistant, good for functional parts",
                    "density_g_cm3": 1.04,
                    "price_per_kg": 1000,
                    "per_gram_price": 1.2,
                    "bed_temp": 90,
                    "extruder_temp": 245,
                    "perimeter_speed": 80,
                    "infill_speed": 160,
                    "solid_infill_speed": 140,
                    "colors": ["White", "Black", "Red", "Blue", "Natural"]
                },
                "petg": {
                    "name": "PETG (Polyethylene Terephthalate Glycol)",
                    "type": "fdm",
                    "description": "Strong, flexible, chemical resistant, food-safe option",
                    "density_g_cm3": 1.27,
                    "price_per_kg": 1000,
                    "per_gram_price": 1.2,
                    "bed_temp": 70,
                    "extruder_temp": 240,
                    "perimeter_speed": 70,
                    "infill_speed": 150,
                    "solid_infill_speed": 120,
                    "colors": ["Clear", "White", "Black", "Blue", "Red"]
                },
                "tpu": {
                    "name": "TPU (Thermoplastic Polyurethane)",
                    "type": "fdm",
                    "description": "Flexible and elastic, excellent for grips and cushioning",
                    "density_g_cm3": 1.21,
                    "price_per_kg": 1500,
                    "per_gram_price": 2.0,
                    "bed_temp": 60,
                    "extruder_temp": 230,
                    "perimeter_speed": 30,
                    "infill_speed": 40,
                    "solid_infill_speed": 35,
                    "colors": ["Black", "White", "Red", "Blue", "Clear"]
                },
                "nylon": {
                    "name": "Nylon (Polyamide)",
                    "type": "fdm",
                    "description": "Very strong and durable, excellent layer adhesion",
                    "density_g_cm3": 1.14,
                    "price_per_kg": 1800,
                    "per_gram_price": 2.5,
                    "bed_temp": 80,
                    "extruder_temp": 250,
                    "perimeter_speed": 60,
                    "infill_speed": 100,
                    "solid_infill_speed": 80,
                    "colors": ["Natural", "Black", "White"]
                },
                "standard_resin": {
                    "name": "Standard Resin",
                    "type": "dlp",
                    "description": "General purpose photopolymer resin for detailed prints",
                    "density_g_ml": 1.1,
                    "price_per_liter": 25000,
                    "per_ml_price": 25.0,
                    "exposure_time_s": 8,
                    "bottom_exposure_s": 60,
                    "lift_speed_mm_s": 3,
                    "colors": ["Grey", "White", "Black", "Clear"]
                },
                "tough_resin": {
                    "name": "Tough Resin",
                    "type": "dlp",
                    "description": "High-strength resin for functional parts",
                    "density_g_ml": 1.15,
                    "price_per_liter": 35000,
                    "per_ml_price": 35.0,
                    "exposure_time_s": 10,
                    "bottom_exposure_s": 70,
                    "lift_speed_mm_s": 2.5,
                    "colors": ["Grey", "Black"]
                },
                "flexible_resin": {
                    "name": "Flexible Resin",
                    "type": "dlp",
                    "description": "Rubber-like elastomer for flexible parts",
                    "density_g_ml": 1.08,
                    "price_per_liter": 40000,
                    "per_ml_price": 40.0,
                    "exposure_time_s": 12,
                    "bottom_exposure_s": 80,
                    "lift_speed_mm_s": 2,
                    "colors": ["Black", "Clear"]
                }
            },
            "print_quality": {
                "draft": {
                    "name": "Draft (Fast)",
                    "layer_height": 0.3,
                    "description": "Fastest print, visible layers, good for prototypes"
                },
                "standard": {
                    "name": "Standard (Balanced)",
                    "layer_height": 0.2,
                    "description": "Good balance of speed and quality"
                },
                "fine": {
                    "name": "Fine (Detailed)",
                    "layer_height": 0.15,
                    "description": "Higher detail, longer print time"
                },
                "ultra_fine": {
                    "name": "Ultra Fine (Maximum Detail)",
                    "layer_height": 0.1,
                    "description": "Best quality, slowest print, minimal layer lines"
                }
            },
            "infill_options": {
                "min_percentage": 5,
                "max_percentage": 100,
                "default_percentage": 20,
                "recommended": {
                    "prototype": 10,
                    "standard": 20,
                    "functional": 40,
                    "structural": 80,
                    "solid": 100
                }
            },
            "pricing": {
                "pricing_mode": "custom",
                "base_cost": 150,
                "electricity_rate_per_kwh": 7,
                "printer_power_watts": 1000,
                "depreciation_per_hour": 50,
                "other_costs_per_print": 20,
                "gst_rate": 0.18,
                "currency": "INR",
                "currency_symbol": "₹"
            },
            "printers": {
                "prusa_mk3s": {
                    "name": "Prusa i3 MK3S+",
                    "type": "fdm",
                    "description": "Original Prusa i3 MK3S+ FDM printer",
                    "bed_size_mm": [250, 210, 210],
                    "nozzle_diameter_mm": 0.4,
                    "max_print_speed_mm_s": 200,
                    "markup_multiplier": 1.3,
                    "enabled": True
                },
                "ender3_v2": {
                    "name": "Creality Ender 3 V2",
                    "type": "fdm",
                    "description": "Creality Ender 3 V2 budget FDM printer",
                    "bed_size_mm": [220, 220, 250],
                    "nozzle_diameter_mm": 0.4,
                    "max_print_speed_mm_s": 180,
                    "markup_multiplier": 1.25,
                    "enabled": True
                },
                "bambu_x1": {
                    "name": "Bambu Lab X1 Carbon",
                    "type": "fdm",
                    "description": "Bambu Lab X1 Carbon high-speed printer",
                    "bed_size_mm": [256, 256, 256],
                    "nozzle_diameter_mm": 0.4,
                    "max_print_speed_mm_s": 500,
                    "markup_multiplier": 1.4,
                    "enabled": True
                },
                "elegoo_mars": {
                    "name": "Elegoo Mars 3 Pro",
                    "type": "dlp",
                    "description": "High-resolution MSLA 3D printer",
                    "build_volume_mm": [143, 89, 175],
                    "xy_resolution_um": 35,
                    "layer_height_um": [10, 100],
                    "markup_multiplier": 1.35,
                    "enabled": True
                },
                "anycubic_photon": {
                    "name": "Anycubic Photon Mono X",
                    "type": "dlp",
                    "description": "Large format resin printer with 4K LCD",
                    "build_volume_mm": [192, 120, 245],
                    "xy_resolution_um": 50,
                    "layer_height_um": [10, 150],
                    "markup_multiplier": 1.4,
                    "enabled": True
                },
                "creality_halot": {
                    "name": "Creality Halot-One Plus",
                    "type": "dlp",
                    "description": "Budget-friendly resin printer",
                    "build_volume_mm": [172, 102, 160],
                    "xy_resolution_um": 50,
                    "layer_height_um": [10, 100],
                    "markup_multiplier": 1.25,
                    "enabled": True
                }
            },
            "post_processing": {
                "sanding": {
                    "name": "Sanding & Smoothing",
                    "description": "Manual sanding for smooth surface finish",
                    "price": 500,
                    "enabled": True
                },
                "painting": {
                    "name": "Painting",
                    "description": "Professional spray painting with primer and topcoat",
                    "price": 1500,
                    "enabled": True
                },
                "polishing": {
                    "name": "Polishing",
                    "description": "High-gloss polishing for aesthetic finish",
                    "price": 800,
                    "enabled": True
                },
                "threading": {
                    "name": "Threading/Tapping",
                    "description": "Adding threads to holes for screws/bolts",
                    "price": 300,
                    "enabled": True
                }
            },
            "file_settings": {
                "max_file_size_mb": 100,
                "allowed_extensions": ["stl"],
                "upload_timeout_seconds": 300
            }
        }

    def save(self):
        """Save current configuration to JSON file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def get(self, *keys, default=None):
        """Get nested configuration value using dot notation or keys"""
        data = self.config_data
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return default
        return data

    def set(self, value, *keys):
        """Set nested configuration value"""
        data = self.config_data
        for key in keys[:-1]:
            if key not in data:
                data[key] = {}
            data = data[key]
        data[keys[-1]] = value

    def get_materials(self):
        """Get all available materials"""
        return self.config_data.get('materials', {})

    def get_material(self, material_key):
        """Get specific material configuration"""
        return self.config_data.get('materials', {}).get(material_key)

    def get_print_qualities(self):
        """Get all print quality options"""
        return self.config_data.get('print_quality', {})

    def get_pricing_config(self):
        """Get pricing configuration"""
        return self.config_data.get('pricing', {})

    def get_pricing_mode(self):
        """Get pricing mode (custom or per_gram)"""
        return self.config_data.get('pricing', {}).get('pricing_mode', 'custom')

    def get_slicer_path(self):
        """Get PrusaSlicer executable path"""
        return self.config_data.get('slicer', {}).get('path', self.DEFAULT_SLICER_PATH)

    def get_printers(self):
        """Get all available printers"""
        return self.config_data.get('printers', {})

    def get_enabled_printers(self):
        """Get only enabled printers"""
        all_printers = self.get_printers()
        return {key: printer for key, printer in all_printers.items() if printer.get('enabled', True)}

    def get_printer(self, printer_key):
        """Get specific printer configuration"""
        return self.config_data.get('printers', {}).get(printer_key)

    def get_post_processing_options(self):
        """Get all available post-processing options"""
        return self.config_data.get('post_processing', {})

    def get_enabled_post_processing(self):
        """Get only enabled post-processing options"""
        all_options = self.get_post_processing_options()
        return {key: option for key, option in all_options.items() if option.get('enabled', True)}

    def get_post_processing(self, key):
        """Get specific post-processing option"""
        return self.config_data.get('post_processing', {}).get(key)


# Global configuration instance
config = Config()
