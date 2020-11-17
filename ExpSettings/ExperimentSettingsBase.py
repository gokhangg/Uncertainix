

import abc

class ExperimentSettingsBase(abc.ABC):
            
    @abc.abstractmethod    
    def GetMethodSettings(self) -> dict:
        pass
    
    @abc.abstractmethod   
    def GetModeSettings(self) -> dict:
        pass
    
    @abc.abstractmethod   
    def SetParameters(self):
        pass