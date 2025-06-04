import statistics
import os
import math
from abc import ABC, abstractmethod
from collections import Counter

class StatisticsStrategy(ABC):
    """
    Abstract strategy for statistical calculations
    Strategy Pattern: Defines different algorithms for calculation
    """
    @abstractmethod
    def calculate(self, values):
        """Calculate statistics for a list of values"""
        pass
    
    @abstractmethod
    def get_name(self):
        """Get the name of this calculation strategy"""
        pass
    
    @abstractmethod
    def format_result(self, result):
        """Format the calculation result as a string"""
        pass


class AverageStrategy(StatisticsStrategy):
    """Strategy for calculating average/mean"""
    def calculate(self, values):
        if not values:
            return 0
        return sum(values) / len(values)
    
    def get_name(self):
        return "average"
    
    def format_result(self, result):
        # Format with no decimal places if it's a whole number
        return f"avg: {result if result == int(result) else result:.2f}"


class MaximumStrategy(StatisticsStrategy):
    """Strategy for finding maximum value"""
    def calculate(self, values):
        if not values:
            return 0
        return max(values)
    
    def get_name(self):
        return "maximum"
    
    def format_result(self, result):
        # Format with no decimal places if it's a whole number
        return f"max: {result if result == int(result) else result:.2f}"


class MinimumStrategy(StatisticsStrategy):
    """Strategy for finding minimum value"""
    def calculate(self, values):
        if not values:
            return 0
        return min(values)
    
    def get_name(self):
        return "minimum"
    
    def format_result(self, result):
        # Format with no decimal places if it's a whole number
        return f"min: {result if result == int(result) else result:.2f}"


class StandardDeviationStrategy(StatisticsStrategy):
    """Strategy for calculating standard deviation"""
    def calculate(self, values):
        if len(values) < 2:
            return 0
        return statistics.stdev(values)
    
    def get_name(self):
        return "standarddeviation"
    
    def format_result(self, result):
        # Format with no decimal places if it's a whole number
        return f"std: {result if result == int(result) else result:.2f}"


class FrequencyStrategy(StatisticsStrategy):
    """Strategy for calculating frequency of values"""
    def calculate(self, values):
        if not values:
            return {}
        return dict(Counter(values))
    
    def get_name(self):
        return "frequency"
    
    def format_result(self, result):
        # This will be overridden by the measurement-type specific formatting
        # in the ResultWriter class
        formatted = []
        for value, count in sorted(result.items()):
            formatted.append(f"{value} {count} defa ölçüldü")
        return "\n".join(formatted)


class MedianStrategy(StatisticsStrategy):
    """Strategy for calculating median"""
    def calculate(self, values):
        if not values:
            return 0
        return statistics.median(values)
    
    def get_name(self):
        return "median"
    
    def format_result(self, result):
        # Format with no decimal places if it's a whole number
        return f"median: {result if result == int(result) else result:.2f}"


class CalculatorContext:
    """
    Context class that manages the strategies
    Strategy Pattern: Context that uses concrete strategies
    """
    def __init__(self, strategy=None):
        self.strategy = strategy
    
    def set_strategy(self, strategy):
        self.strategy = strategy
    
    def calculate(self, values):
        if self.strategy:
            return self.strategy.calculate(values)
        return None


class CalculatorFactory:
    """
    Factory class for creating calculators
    Factory Method Pattern: Creates appropriate calculator strategies
    """
    @staticmethod
    def create_calculator(calculation_type):
        calculators = {
            'average': AverageStrategy(),
            'maximum': MaximumStrategy(),
            'minimum': MinimumStrategy(),
            'standard_deviation': StandardDeviationStrategy(),
            'frequency': FrequencyStrategy(),
            'median': MedianStrategy()
        }
        
        return calculators.get(calculation_type.lower())


class ResultWriter:
    """
    Class to write calculation results to files
    """
    @staticmethod
    def write_file_result(output_dir, measurement_type, strategy, file_results):
        """Write results for individual files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Create directory for measurement type if it doesn't exist
        measurement_dir = os.path.join(output_dir, measurement_type)
        os.makedirs(measurement_dir, exist_ok=True)
        
        # Write results to file
        filename = f"{strategy.get_name()}degerler.txt"
        file_path = os.path.join(measurement_dir, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            for file_obj, result in file_results:
                if isinstance(result, dict):  # For frequency results
                    f.write(f"{ResultWriter._format_file_metadata(file_obj)}\n")
                    
                    # Format frequency results with appropriate unit based on measurement type
                    formatted = []
                    measurement_unit = ResultWriter._get_measurement_unit(measurement_type)
                    
                    for value, count in sorted(result.items()):
                        formatted.append(f"{value} {measurement_unit} {count} defa ölçüldü")
                    
                    f.write("\n".join(formatted))
                    f.write("\n---------------\n")
                else:
                    f.write(f"{ResultWriter._format_file_metadata(file_obj)} , {strategy.format_result(result)}\n")
    
    @staticmethod
    def write_global_result(output_dir, measurement_type, strategy, result):
        """Write global calculation results"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Create directory for measurement type if it doesn't exist
        measurement_dir = os.path.join(output_dir, measurement_type)
        os.makedirs(measurement_dir, exist_ok=True)
        
        # Write results to file
        filename = f"global{strategy.get_name()}.txt"
        file_path = os.path.join(measurement_dir, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            if isinstance(result, dict):  # For frequency results
                # Format frequency results with appropriate unit based on measurement type
                formatted = []
                measurement_unit = ResultWriter._get_measurement_unit(measurement_type)
                
                for value, count in sorted(result.items()):
                    formatted.append(f"{value} {measurement_unit} {count} defa ölçüldü")
                
                f.write("\n".join(formatted))
            else:
                f.write(strategy.format_result(result))
    
    @staticmethod
    def _format_file_metadata(file_obj):
        """Format file metadata for output"""
        metadata = file_obj.metadata
        return f"id:{metadata.get('id', 'unknown')} ölçüm: {metadata.get('type', 'unknown')} - yer: {metadata.get('location', 'unknown')} - tarih: {metadata.get('date', 'unknown')}"
    
    @staticmethod
    def _get_measurement_unit(measurement_type):
        """Get the appropriate unit for the measurement type"""
        if measurement_type == 'temperature':
            return "Derece"
        elif measurement_type == 'humidity':
            return "%"  # Percent symbol for humidity
        else:
            return ""  # Default empty string for unknown types 