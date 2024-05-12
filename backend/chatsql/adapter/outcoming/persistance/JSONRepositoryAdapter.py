from typing import List, IO

from chatsql.application.port.outcoming.persistance.BaseJSONRepository import BaseJsonRepository

from chatsql.application.port.outcoming.EmbeddingGeneratorPort import EmbeddingGeneratorPort

from chatsql.utils.JSONValidator import JSONValidator

from chatsql.utils.Common import Settings
from chatsql.utils import Exceptions

import json
from os import listdir, remove, mkdir
from os.path import isfile, join, exists

from shutil import copyfileobj
from werkzeug.utils import secure_filename

class JSONRepositoryAdapter(BaseJsonRepository):

    def __init__(self) -> None:
        
        self._folder = Settings.folder
        self.__create_folder()


    def save(self, filename: str, stream: IO[bytes]) -> bool:

        if self.__already_present(filename=filename):
            raise Exceptions.FileAlreadyUploaded(f"`{filename}` è già stato caricato precedentemente")

        content = ''.join([chunk.decode() for chunk in stream])
        if not self.__is_valid(content=content):
            raise Exceptions.InvalidStructure(f"`{filename}` non rispetta la struttura")
        
        secured_filename = secure_filename(filename=filename)
        stream.seek(0)
        
        dst = join(self._folder, secured_filename)
        close_dst = False

        if isinstance(dst, str):
            dst = open(dst, "w+b")
            close_dst = True

        try:
            
            copyfileobj(stream, dst, 1024)

            return True
        finally:
            if close_dst:
                dst.close()
            return False

    def remove(self, filename: str) -> bool:
        
        if filename in self.list_all():
            remove(join(self._folder, filename))
            return True

        return False
        
    def list_all(self) -> List[str]:
        return [filename for filename in listdir(self._folder) 
                if isfile(join(self._folder, filename)) and
                    filename.split('.')[-1] == 'json']

    @staticmethod
    def open(filename: str):
        secured_filename = secure_filename(filename)
        with open(join(Settings.folder, secured_filename), "r") as file:
            return json.load(file)

    def __is_valid(self, content: str) -> bool:
        content = json.loads(content)
        return JSONValidator.is_valid_structure(content)

    def __already_present(self, filename: str) -> bool:
        secured_filename = secure_filename(filename)
        return secured_filename in self.list_all()

    def __create_folder(self) -> None:
        if not exists(self._folder):
            mkdir(self._folder)
