import os
from src.core.calculator import CalculatorFactory, CalculatorContext, ResultWriter

class CalculationProcessor:
    """
    Class that orchestrates the calculation process
    Template Method Pattern: Defines the skeleton of the algorithm
    """
    def __init__(self, directory):
        self.directory = directory
        self.output_directory = os.path.join(directory, 'result')
        self.calculator_context = CalculatorContext()
    
    def process_calculations(self, measurement_files, operations, use_global=False):
        """
        Process calculations on measurement files
        
        Args:
            measurement_files: Dictionary with 'temperature' and 'humidity' keys
            operations: List of operation names to perform
            use_global: Whether to perform global calculations
            
        Returns:
            Dictionary with results and status message
        """
        results = {}
        status = "Success"
        
        try:
            # Process each measurement type (temperature, humidity)
            for measurement_type, files in measurement_files.items():
                if not files:
                    continue
                
                # Process each requested operation
                for operation in operations:
                    strategy = CalculatorFactory.create_calculator(operation)
                    if not strategy:
                        continue
                    
                    self.calculator_context.set_strategy(strategy)
                    
                    # Calculate for each file
                    file_results = []
                    for file_obj in files:
                        values = file_obj.get_values()
                        if values:
                            result = self.calculator_context.calculate(values)
                            file_results.append((file_obj, result))
                    
                    # Write individual file results
                    ResultWriter.write_file_result(
                        self.output_directory, 
                        measurement_type,
                        strategy, 
                        file_results
                    )
                    
                    # Calculate and write global results if requested
                    if use_global:
                        # Combine all values from all files for global calculation
                        all_values = []
                        for file_obj in files:
                            all_values.extend(file_obj.get_values())
                        
                        if all_values:
                            global_result = self.calculator_context.calculate(all_values)
                            ResultWriter.write_global_result(
                                self.output_directory,
                                measurement_type,
                                strategy,
                                global_result
                            )
            
            message = f"The calculations were successfully performed. Folder containing results: {self.output_directory}"
            
        except Exception as e:
            message = f"An error occurred during the calculation: {str(e)}. Please try again."
            status = "Error"
            
        return {
            "status": status,
            "message": message
        } 