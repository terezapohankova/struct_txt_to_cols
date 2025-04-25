# -*- coding: utf-8 -*-

import arcpy


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Structured text (DHL layer) to Columns"
        self.alias = "Structured text (DHL layer) to Columns"

        # List of tool classes associated with this toolbox
        self.tools = [dhl_to_cols]



class dhl_to_cols:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "DHL layer to columns"
        self.description = ""

    def getParameterInfo(self):
        """Define the tool parameters."""
        param0 = arcpy.Parameter(
            displayName="Input Layer or Table",  # Label for the input parameter
            name="input_layer",  # Name of the input parameter
            datatype=["GPFeatureLayer", "DEShapeFile"],  # Data type for input (customizable for each class)
            parameterType="Required",  # This parameter is required
            direction="Input"  # Direction of data flow (input)
        )
        # Define the second parameter (output layer or table)
        param1 = arcpy.Parameter(
            displayName="Field",  # Label for the output parameter
            name="field",  # Name of the output parameter
            datatype="Field",  # Data type for output (customizable for each class)
            parameterType="Required",  # This parameter is required
            direction="Input"  # Direction of data flow (output)
        )

        params = [param0, param1]

        params[1].filter.list = ['Text']  # Field data types
        params[1].parameterDependencies = [params[0].name]
        

        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
   
        # Get parameter values
        input_layer = parameters[0].valueAsText
        split_field = parameters[1].valueAsText

        # Initiate Empty Variabled
        max_parts = 0
        all_split_values = []


        # Find out how many new columns will be made, based on splitting by ; and _
        # The output number of columns is number of "_" * 2
        with arcpy.da.SearchCursor(input_layer, [split_field]) as cursor:
            for row in cursor:
                val = row[0]
                split_parts = [] # for the splitted values
                if val: #if the cell is not emptz, split the text bby ;
                    segments = val.split(";") # segments = ["M1.4_60", "K1_40"]
                    for seg in segments:
                        split_parts.extend(seg.split("_")) # split_parts = ["M1.4", "60", "K1", "40"]
                all_split_values.append(split_parts) 
                if len(split_parts) > max_parts: # check how many columns we need (2 for each split by _)
                    max_parts = len(split_parts)

        # Create the new fields
        new_fields = [f"{split_field}_{i+1}" for i in range(max_parts)] #generate name for fields inputlayer_1, inputlayer_2 etc
        existing_fields = [f.name for f in arcpy.ListFields(input_layer)] # get all already existing fields

        for field in new_fields:    # if the new field name is not in the already existing field names, add it as new field
            if field not in existing_fields:
                arcpy.AddField_management(input_layer, field, "TEXT")

        # Put splitted values into the new fields
        with arcpy.da.UpdateCursor(input_layer, new_fields + [split_field]) as cursor:
            for row in cursor:
                val = row[-1]  
                filled = [""] * max_parts # filled = ["", "", "", ""]
                if val: #if not none, split by ; and _ (same as above)
                    segments = val.split(";")
                    split_parts = []
                    for seg in segments:
                        split_parts.extend(seg.split("_"))
                    for i, part in enumerate(split_parts):
                        if i < max_parts:
                            filled[i] = part # filled = ["M1.4", "60", "K1", "40"]
                cursor.updateRow(filled + [val])  
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
