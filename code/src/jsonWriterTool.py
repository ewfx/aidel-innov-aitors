import json

class JSONWriterTool:
    def __init__(self, file_path='finalOutput.json'):
        """
        Initializes the JSONWriterTool with a specified file path.
        """
        self.file_path = file_path

    def run(self, data):
        """
        Writes the provided JSON data to the specified file path.
        
        Args:
        - data (dict): JSON data to write to file
        
        Returns:
        - str: Confirmation message or error details
        """
        try:
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=4)
            return f"Data successfully written to {self.file_path}"
        except Exception as e:
            return f"Error writing JSON data: {str(e)}"