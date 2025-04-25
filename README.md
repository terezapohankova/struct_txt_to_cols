# Structured Text (DHL Layer) to Columns Tool

This Python toolbox for ArcGIS will convert structured text data from a DHL layer into multiple columns. It processes data that contains delimiter-separated values (`;` and `_`) 
and splits it into individual columns for each part of the string.

## Tool Description
- Reads a field from the input layer that contains structured text data.
- Splits the text into multiple parts using delimiters (`;` and `_`).
- Creates new columns in the layer for each part of the split text.
- Fills the new columns with the corresponding values.

## Parameters

- **Input Layer or Table (Required)**: The layer or table containing the field with structured text.
- **Field (Required)**: The field in the input layer containing the structured text to be split. The field should be of the "Text" data type.

### Example
- **M1.4_60;K1_40**

  The tool will create two new columns:
- `field_1` (M1.4)
- `field_2` (60)
- `field_3` (K1)
- `field_4` (40)


