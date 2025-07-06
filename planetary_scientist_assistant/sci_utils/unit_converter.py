# planetary_scientist_assistant/sci_utils/unit_converter.py

# Conversion factors are based on common standards.
# For high-precision scientific work, official sources for conversion factors should be consulted.

CONVERSION_FACTORS = {
    "length": {
        "meter": 1.0,
        "kilometer": 1000.0,
        "centimeter": 0.01,
        "millimeter": 0.001,
        "micrometer": 1e-6,
        "nanometer": 1e-9,
        "mile": 1609.34,
        "yard": 0.9144,
        "foot": 0.3048,
        "inch": 0.0254,
        "nautical_mile": 1852.0
    },
    "mass": {
        "kilogram": 1.0,
        "gram": 0.001,
        "milligram": 1e-6,
        "microgram": 1e-9,
        "metric_ton": 1000.0,
        "pound": 0.453592,
        "ounce": 0.0283495
    },
    "temperature": {
        # Temperature is special as conversions are not simple factors for Celsius/Fahrenheit
        # We'll handle these with dedicated functions.
        # Kelvin is the base unit for direct factor conversion if we were to define one.
        "celsius": None, # Handled by specific functions
        "fahrenheit": None, # Handled by specific functions
        "kelvin": None # Handled by specific functions
    },
    "time": {
        "second": 1.0,
        "minute": 60.0,
        "hour": 3600.0,
        "day": 86400.0,
        "week": 604800.0,
        "year": 31536000.0 # Average Gregorian year, for general use
    },
    "pressure": { # Pascals as base
        "pascal": 1.0,
        "kilopascal": 1000.0,
        "megapascal": 1e6,
        "bar": 100000.0,
        "psi": 6894.76, # Pound per square inch
        "atm": 101325.0, # Standard atmosphere
        "torr": 133.322 # Millimeter of mercury
    }
    # Add more categories like 'volume', 'speed', 'energy', 'data_size' as needed.
}

def get_supported_categories():
    """Returns a list of supported unit categories."""
    return list(CONVERSION_FACTORS.keys())

def get_supported_units(category):
    """
    Returns a list of supported units for a given category.
    Args:
        category (str): The category name (e.g., "length", "mass").
    Returns:
        list: A list of unit names, or an empty list if category is not found.
    """
    return list(CONVERSION_FACTORS.get(category, {}).keys())


def convert_unit(value, from_unit, to_unit, category):
    """
    Converts a value from one unit to another within a given category.

    Args:
        value (float): The numerical value to convert.
        from_unit (str): The unit to convert from (e.g., "meter").
        to_unit (str): The unit to convert to (e.g., "kilometer").
        category (str): The category of the units (e.g., "length").

    Returns:
        float or None: The converted value, or None if conversion is not possible
                       (e.g., unknown unit/category, or special handling like temperature).
        str: A message indicating success or error.
    """
    if category not in CONVERSION_FACTORS:
        return None, f"Error: Category '{category}' not supported."

    # Handle temperature separately due to offset conversions
    if category == "temperature":
        return _convert_temperature(value, from_unit, to_unit)

    units_in_category = CONVERSION_FACTORS[category]
    if from_unit not in units_in_category or to_unit not in units_in_category:
        unsupported_units = []
        if from_unit not in units_in_category: unsupported_units.append(from_unit)
        if to_unit not in units_in_category: unsupported_units.append(to_unit)
        return None, f"Error: Unit(s) '{', '.join(unsupported_units)}' not supported in category '{category}'."

    # Convert 'from_unit' to the base unit of the category (factor = 1.0)
    value_in_base_unit = value * units_in_category[from_unit]

    # Convert from base unit to 'to_unit'
    # Since factors are relative to base, to get to 'to_unit', we divide by its factor from base.
    if units_in_category[to_unit] == 0: # Avoid division by zero, though unlikely with physical units
        return None, f"Error: Conversion factor for '{to_unit}' is zero, cannot convert."

    converted_value = value_in_base_unit / units_in_category[to_unit]
    return converted_value, f"{value} {from_unit} is {converted_value} {to_unit}."

def _convert_temperature(value, from_unit, to_unit):
    """Handles temperature conversions which include offsets."""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    # Check if units are supported for temperature
    supported_temp_units = ["celsius", "fahrenheit", "kelvin"]
    if from_unit not in supported_temp_units or to_unit not in supported_temp_units:
        unsupported = []
        if from_unit not in supported_temp_units: unsupported.append(from_unit)
        if to_unit not in supported_temp_units: unsupported.append(to_unit)
        return None, f"Error: Temperature unit(s) '{', '.join(unsupported)}' not supported."

    if from_unit == to_unit:
        return value, f"{value} {from_unit} is {value} {to_unit} (no conversion needed)."

    # Convert input to Celsius first (as an intermediate)
    temp_celsius = 0.0
    if from_unit == "celsius":
        temp_celsius = value
    elif from_unit == "fahrenheit":
        temp_celsius = (value - 32) * 5.0/9.0
    elif from_unit == "kelvin":
        temp_celsius = value - 273.15
    else: # Should be caught by the check above
        return None, f"Error: Unknown 'from' temperature unit: {from_unit}"

    # Convert from Celsius to the target unit
    result = 0.0
    if to_unit == "celsius":
        result = temp_celsius
    elif to_unit == "fahrenheit":
        result = (temp_celsius * 9.0/5.0) + 32
    elif to_unit == "kelvin":
        result = temp_celsius + 273.15
    else: # Should be caught by the check above
        return None, f"Error: Unknown 'to' temperature unit: {to_unit}"

    return result, f"{value} {from_unit} is {result} {to_unit}."


if __name__ == '__main__':
    print("--- Testing Unit Converter ---")

    print("\nSupported Categories:")
    cats = get_supported_categories()
    print(cats)
    for cat in cats:
        print(f"  Units in '{cat}': {get_supported_units(cat)}")

    print("\n--- Length Conversions ---")
    val, msg = convert_unit(10, "meter", "kilometer", "length") # 10 meters to km
    print(msg) # Expected: 0.01 km
    assert val is not None and abs(val - 0.01) < 1e-9

    val, msg = convert_unit(1, "mile", "meter", "length") # 1 mile to meters
    print(msg) # Expected: 1609.34 m
    assert val is not None and abs(val - 1609.34) < 1e-9

    val, msg = convert_unit(12, "inch", "centimeter", "length") # 12 inches to cm
    print(msg) # Expected: 30.48 cm
    assert val is not None and abs(val - 30.48) < 1e-9

    print("\n--- Mass Conversions ---")
    val, msg = convert_unit(1000, "gram", "kilogram", "mass") # 1000g to kg
    print(msg) # Expected: 1 kg
    assert val is not None and abs(val - 1.0) < 1e-9

    val, msg = convert_unit(1, "pound", "kilogram", "mass") # 1 lb to kg
    print(msg) # Expected: ~0.453592 kg
    assert val is not None and abs(val - 0.453592) < 1e-9

    print("\n--- Temperature Conversions ---")
    val, msg = convert_unit(0, "celsius", "fahrenheit", "temperature") # 0 C to F
    print(msg) # Expected: 32 F
    assert val is not None and abs(val - 32.0) < 1e-9

    val, msg = convert_unit(32, "fahrenheit", "celsius", "temperature") # 32 F to C
    print(msg) # Expected: 0 C
    assert val is not None and abs(val - 0.0) < 1e-9

    val, msg = convert_unit(100, "celsius", "kelvin", "temperature") # 100 C to K
    print(msg) # Expected: 373.15 K
    assert val is not None and abs(val - 373.15) < 1e-9

    val, msg = convert_unit(273.15, "kelvin", "celsius", "temperature") # 273.15 K to C
    print(msg) # Expected: 0 C
    assert val is not None and abs(val - 0.0) < 1e-9

    val, msg = convert_unit(212, "fahrenheit", "kelvin", "temperature") # 212 F (100C) to K
    print(msg) # Expected: 373.15 K
    assert val is not None and abs(val - 373.15) < 1e-9

    print("\n--- Time Conversions ---")
    val, msg = convert_unit(3600, "second", "hour", "time") # 3600s to hr
    print(msg) # Expected: 1 hr
    assert val is not None and abs(val - 1.0) < 1e-9

    print("\n--- Pressure Conversions ---")
    val, msg = convert_unit(101325, "pascal", "atm", "pressure") # Pascals to atm
    print(msg) # Expected: 1 atm
    assert val is not None and abs(val - 1.0) < 1e-9

    val, msg = convert_unit(1, "bar", "kilopascal", "pressure") # 1 bar to kPa
    print(msg) # Expected: 100 kPa
    assert val is not None and abs(val - 100.0) < 1e-9


    print("\n--- Error Handling ---")
    val, msg = convert_unit(10, "meter", "kilogram", "length") # Mismatched category implied by units
    print(f"Test (meter to kg in 'length'): {msg}") # Should be error about kg not in length
    assert val is None

    val, msg = convert_unit(10, "meter", "foot", "mass") # Wrong category for units
    print(f"Test (meter to foot in 'mass'): {msg}") # Should be error about category
    assert val is None

    val, msg = convert_unit(10, "celsius", "meter", "temperature") # meter not a temp unit
    print(f"Test (celsius to meter in 'temperature'): {msg}")
    assert val is None

    print("\nUnit converter tests completed.")
