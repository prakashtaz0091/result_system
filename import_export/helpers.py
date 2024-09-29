def auto_fit_column_width(ws):
    from openpyxl.utils import get_column_letter
    from openpyxl.styles import Alignment  # Import Alignment for setting cell alignment


    # Auto-adjust column width based on the content
    for column_cells in ws.columns:
        max_length = 0
        column = get_column_letter(column_cells[0].column)  # Get the column letter
        for cell in column_cells:
            try:
                if cell.value:  # Check if the cell has a value
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
            # Apply center alignment (both horizontal and vertical)
            cell.alignment = Alignment(horizontal='center', vertical='center')
            
        adjusted_width = (max_length + 2)  # Add padding for readability
        ws.column_dimensions[column].width = adjusted_width