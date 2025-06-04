class Measurement:
    """
    Class to represent a single measurement from a file
    """
    def __init__(self, time, value):
        self.time = time
        self.value = float(value)

    def __str__(self):
        return f"{self.time}: {self.value}"

class MeasurementFile:
    """
    Class to represent a measurement file, containing metadata and measurements
    """
    def __init__(self, file_path, metadata=None):
        self.file_path = file_path
        self.metadata = metadata or {}
        self.measurements = []
        
    def add_measurement(self, measurement):
        """Add a measurement to this file's data"""
        self.measurements.append(measurement)
        
    def get_values(self):
        """Return a list of all measurement values"""
        return [m.value for m in self.measurements]
        
    def __str__(self):
        return f"{self.metadata.get('id', 'unknown')} - {self.metadata.get('type', 'unknown')}" 