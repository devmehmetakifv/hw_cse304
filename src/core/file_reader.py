import os
from src.models.measurement import Measurement, MeasurementFile

class FileReader:
    """
    Class to read measurement files and extract data
    """
    @staticmethod
    def parse_metadata(header_line):
        """Parse metadata from the first line of a measurement file"""
        metadata = {}
        parts = header_line.strip().split(' - ')
        
        # Parse the first part which contains id and measurement type
        if parts and ':' in parts[0]:
            id_parts = parts[0].split(':')
            if len(id_parts) > 1:
                metadata['id'] = id_parts[0].strip()
                measurement_parts = id_parts[1].strip().split(' ')
                if len(measurement_parts) > 1:
                    metadata['type'] = measurement_parts[1].strip()
        
        # Parse location if available
        if len(parts) > 1 and 'yer:' in parts[1]:
            metadata['location'] = parts[1].split(':')[1].strip()
            
        # Parse date if available
        if len(parts) > 2 and 'tarih:' in parts[2]:
            metadata['date'] = parts[2].split(':')[1].strip()
            
        return metadata
    
    @staticmethod
    def read_file(file_path):
        """Read a measurement file and return a MeasurementFile object"""
        measurement_file = MeasurementFile(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
                if not lines:
                    return measurement_file
                
                # Parse metadata from the first line
                metadata = FileReader.parse_metadata(lines[0])
                measurement_file.metadata = metadata
                
                # Parse measurements from remaining lines
                for line in lines[1:]:
                    line = line.strip()
                    if line and ',' in line:
                        time, value = line.split(',')
                        measurement = Measurement(time.strip(), value.strip())
                        measurement_file.add_measurement(measurement)
                        
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            
        return measurement_file
    
    @staticmethod
    def scan_directory(directory):
        """
        Scan a directory for measurement data
        Returns a dictionary with 'temperature' and 'humidity' keys, each containing lists of MeasurementFile objects
        """
        result = {
            'temperature': [],
            'humidity': []
        }
        
        try:
            # Check for temperature subdirectory
            temp_dir = os.path.join(directory, 'sıcaklık')
            if os.path.isdir(temp_dir):
                for filename in os.listdir(temp_dir):
                    if filename.endswith('.txt'):
                        file_path = os.path.join(temp_dir, filename)
                        measurement_file = FileReader.read_file(file_path)
                        result['temperature'].append(measurement_file)
                        
            # Check for humidity subdirectory
            humidity_dir = os.path.join(directory, 'nem')
            if os.path.isdir(humidity_dir):
                for filename in os.listdir(humidity_dir):
                    if filename.endswith('.txt'):
                        file_path = os.path.join(humidity_dir, filename)
                        measurement_file = FileReader.read_file(file_path)
                        result['humidity'].append(measurement_file)
                        
        except Exception as e:
            print(f"Error scanning directory {directory}: {e}")
            
        return result 