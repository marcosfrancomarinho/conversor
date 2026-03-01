class Type:
    def __init__(self, value:str) -> None:
        self.__validate(value)
        self.__value = value
    
    def __validate(self,value:str)->None:
        if not value or value.isspace():
            raise Exception("o tipo do arquivo não foi definido")
        
    def get_value(self)->str:
        return self.__value.upper()