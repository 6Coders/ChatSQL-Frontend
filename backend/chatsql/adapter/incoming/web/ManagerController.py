
from chatsql.application.port.incoming.InserimentoDizionarioUseCase import InserimentoDizionarioUseCase
from chatsql.application.port.incoming.EliminazioneDizionarioUseCase import EliminazioneDizionarioUseCase
from chatsql.application.port.incoming.VisualizzaListaDizionariUseCase import VisualizzaListaDizionariUseCase
from chatsql.application.port.incoming.VisualizzaDizionarioCorrenteUseCase import VisualizzaDizionarioCorrenteUseCase
from chatsql.application.EmbeddingSaver import EmbeddingSaver

from chatsql.utils import Exceptions
from chatsql.utils.Common import Settings

from flask import Blueprint, request, jsonify 
import os
import datetime

class ManagerController:

    blueprint = None

    def __init__(self,
                 inserimentoDizionarioUseCase: InserimentoDizionarioUseCase,
                 eliminazioneDizionarioUseCase: EliminazioneDizionarioUseCase,
                 visualizzaListaDizionariUseCase: VisualizzaListaDizionariUseCase,
                 visualizzaDizionarioCorrenteUseCase: VisualizzaDizionarioCorrenteUseCase,
                 embeddingSaver: EmbeddingSaver) -> None:
        
        self._inserimentoDizionarioUseCase = inserimentoDizionarioUseCase
        self._eliminazioneDizionarioUseCase = eliminazioneDizionarioUseCase
        self._visualizzaListaDizionariUseCase = visualizzaListaDizionariUseCase
        self._visualizzaDizionarioCorrenteUseCase = visualizzaDizionarioCorrenteUseCase
        self._embeddingSaver = embeddingSaver

    def handle_upload(self):

        try:

            file = request.files['file']

            self._inserimentoDizionarioUseCase.add(file.filename, file.stream)
            self._embeddingSaver.save(file.filename)

            return 'File aggiunto correttamente'

        except BaseException as e:
            if hasattr(e, 'message'):
                return e.message
            else:
                return 'Non è possibile caricare il file'

    def handle_list_files(self):

        data = self._visualizzaListaDizionariUseCase.list_all()

        for file in data:
            file['loaded'] = file['name'] == self._visualizzaDizionarioCorrenteUseCase.selected

        return data

    def handle_selection(self):

        self._visualizzaDizionarioCorrenteUseCase.selected = request.form['selected']

        return 'ok'

    def handle_delete(self):

        filename = request.data.decode()

        if self._visualizzaDizionarioCorrenteUseCase.selected == filename:
            self._visualizzaDizionarioCorrenteUseCase.selected = None

        self._eliminazioneDizionarioUseCase.remove(filename)
        self._embeddingSaver.remove(filename)

        return 'ok'


