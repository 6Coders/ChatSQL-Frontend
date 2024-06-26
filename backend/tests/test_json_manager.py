import os
import unittest
from datetime import datetime
from unittest.mock import MagicMock

from flask import Flask

from chatsql.adapter.incoming.web.ManagerController import ManagerController

class TestJSONManager(unittest.TestCase):

	def setUp(self):

		self.inserimentoDizionario = MagicMock()
		self.eliminazioneDizionario = MagicMock()
		self.visualizzaListaDizionari = MagicMock(return_value=[])
		self.visualizzaDizionarioCorrente = MagicMock()
		self.embeddingSaver = MagicMock()

		app = Flask(__name__)
		app.config['TESTING'] = True
		self.controller = ManagerController(
			inserimentoDizionarioUseCase=self.inserimentoDizionario,
			eliminazioneDizionarioUseCase=self.eliminazioneDizionario,
			visualizzaListaDizionariUseCase=self.visualizzaListaDizionari,
			visualizzaDizionarioCorrenteUseCase=self.visualizzaDizionarioCorrente,
			embeddingSaver=self.embeddingSaver,
		)

		app.route('/upload', methods=["POST"])(self.controller.handle_upload)
		app.route('/files', methods=["GET"])(self.controller.handle_list_files)
		app.route('/select', methods=["POST"])(self.controller.handle_selection)
		app.route('/delete', methods=["DELETE"])(self.controller.handle_delete)

		self.client = app.test_client()

	def test_handle_upload_success(self):

		filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'json', 'dbmusica.json')

		response = self.client.post('/upload', data={
			'file': open(filepath, 'rb')
		})

		self.assertEqual(response.status_code, 200)
		self.inserimentoDizionario.add.assert_called_once()
		self.embeddingSaver.save.assert_called_once()

	def test_handle_upload_fail(self):

		response = self.client.post('/upload', data={
			'file': None
		})

		self.assertEqual(response.status_code, 200)
		self.inserimentoDizionario.add.assert_not_called()
		self.embeddingSaver.save.assert_not_called()

	def test_handle_list_files_empty(self):

		self.visualizzaListaDizionari.list_all = MagicMock(return_value=[])

		response = self.client.get('/files')

		self.assertEqual(response.status_code, 200)
		self.visualizzaListaDizionari.list_all.assert_called_once()

	def test_handle_list_files_example(self):

		self.visualizzaListaDizionari.list_all = MagicMock(return_value=[{
				'name': 'test',
				'extension': 'json',
				'date': datetime.now(),
				'size': '69 Kb',
			}
		])

		response = self.client.get('/files')

		self.assertEqual(response.status_code, 200)
		self.visualizzaListaDizionari.list_all.assert_called_once()


	def test_handle_selection_success(self):

		self.visualizzaDizionarioCorrente.selected = MagicMock()

		response = self.client.post('/select', data={
			'selected': 'test'
		})

		self.assertEqual(response.status_code, 200)

	def test_handle_delete_success(self):

		self.eliminazioneDizionario.remove = MagicMock()

		response = self.client.delete('/delete', data=b'ad')

		self.assertEqual(response.status_code, 200)
		self.eliminazioneDizionario.remove.assert_called_once()

if __name__ == '__main__':
	unittest.main()


