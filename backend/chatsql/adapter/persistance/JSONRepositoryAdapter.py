from typing import List, IO
from chatsql.application.port.outcoming.persistance.BaseJSONRepository import BaseJsonRepository

from chatsql.utils.JSONValidator import JSONValidator

import json
from os import listdir
from os.path import isfile, join, exists

from shutil import copy2
from werkzeug.utils import secure_filename

class JSONRepositoryAdapter(BaseJsonRepository):

    def __init__(self, folder: str) -> None:
        
        self._folder = folder

    def save(self, filename: str, stream: IO[bytes]) -> bool:

        if self.__is_valid(filename=filename, content=stream):
            raise ValueError(f"`{filename}` non rispetta la struttura")

        filepath = join(self._folder, filename)

        dst = secure_filename(filepath)
        close_dst = False

        if isinstance(dst, str):
            dst = open(dst, "wb")
            close_dst = True

        try:
            copy2(stream, dst, 1024)
            return True
        finally:
            if close_dst:
                dst.close()
            return False

    def remove(self, filename: str):
        raise NotImplementedError()
    
    def list_all(self) -> List[str]:
        return [filename for filename in listdir(self._folder) 
                if isfile(join(self._folder, filename)) and
                    filename.split('.')[-1] == 'json']


    def __is_valid(self, filename: str, content: IO[bytes]) -> bool:
        content = json.loads(content)
        return JSONValidator.is_valid_structure(content)
