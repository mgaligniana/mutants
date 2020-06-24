import unittest
import json

from app import app, db


class SignupTest(unittest.TestCase):

    WRONG_SEQUENCE = [
        "000000",
        "00AAAA",
        "000000"
    ]

    MUTANT_SEQUENCE_IN_ROW = [
        "000000",
        "00AAAA",
        "000000",
        "000000",
        "000000",
        "000000"
    ]

    MUTANT_SEQUENCE_IN_COLUMN = [
        "000000",
        "A00000",
        "A00000",
        "A00000",
        "A00000",
        "000000"
    ]

    MUTANT_SEQUENCE_IN_DIAGONAL = [
        "000000",
        "000000",
        "A00000",
        "0A0000",
        "00A000",
        "000A00"
    ]

    MUTANT_SEQUENCE_IN_DIAGONAL_INVERTED = [
        "00000A",
        "0000A0",
        "000A00",
        "00A000",
        "000000",
        "000000"
    ]

    HUMAN_SEQUENCE = [
        "000000",
        "000000",
        "000000",
        "000000",
        "000000",
        "000000"
    ]

    def setUp(self):
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_dna_not_presented(self):
        payload = json.dumps({
            "sarasa": self.MUTANT_SEQUENCE_IN_ROW         
        })
        response = self.app.post('/api/v1/mutant', data=payload, headers={"Content-Type": "application/json"})
        self.assertEqual(400, response.status_code)
        assert b"Please provide a DNA sequence" in response.data

    def test_invalid_dna_format(self):
        payload = json.dumps({
            "dna": self.WRONG_SEQUENCE
        })
        response = self.app.post('/api/v1/mutant', data=payload, headers={"Content-Type": "application/json"})
        self.assertEqual(400, response.status_code)
        assert b"DNA sequence should be NxN format" in response.data

    def test_mutant_dna_in_row(self):
        payload = json.dumps({
            "dna": self.MUTANT_SEQUENCE_IN_ROW
        })
        response = self.app.post('/api/v1/mutant', data=payload, headers={"Content-Type": "application/json"})
        self.assertEqual(200, response.status_code)

    def test_mutant_dna_in_column(self):
        payload = json.dumps({
            "dna": self.MUTANT_SEQUENCE_IN_COLUMN
        })
        response = self.app.post('/api/v1/mutant', data=payload, headers={"Content-Type": "application/json"})
        self.assertEqual(200, response.status_code)

    def test_mutant_dna_in_diagonal(self):
        payload = json.dumps({
            "dna": self.MUTANT_SEQUENCE_IN_DIAGONAL
        })
        response = self.app.post('/api/v1/mutant', data=payload, headers={"Content-Type": "application/json"})
        self.assertEqual(200, response.status_code)

    def test_mutant_dna_in_diagonal_inverted(self):
        payload = json.dumps({
            "dna": self.MUTANT_SEQUENCE_IN_DIAGONAL_INVERTED
        })
        response = self.app.post('/api/v1/mutant', data=payload, headers={"Content-Type": "application/json"})
        self.assertEqual(200, response.status_code)

    def test_human_dna(self):
        payload = json.dumps({
            "dna": self.HUMAN_SEQUENCE
        })
        response = self.app.post('/api/v1/mutant', data=payload, headers={"Content-Type": "application/json"})
        self.assertEqual(403, response.status_code)

    def test_get_all_dnas(self):
        self.test_mutant_dna_in_row()
        self.test_mutant_dna_in_column()
        self.test_mutant_dna_in_diagonal()
        self.test_mutant_dna_in_diagonal_inverted()
        self.test_human_dna()

        response = self.app.get('/api/v1/dnas', headers={"Content-Type": "application/json"})
        self.assertEqual(200, response.status_code)
        self.assertEqual(5, len(response.get_json()))

        self.assertEqual(1, response.get_json()[0]["id"])
        self.assertEqual(self.MUTANT_SEQUENCE_IN_ROW, response.get_json()[0]["sequence"])
        self.assertEqual(True, response.get_json()[0]["is_mutant"])

        self.assertEqual(2, response.get_json()[1]["id"])
        self.assertEqual(self.MUTANT_SEQUENCE_IN_COLUMN, response.get_json()[1]["sequence"])
        self.assertEqual(True, response.get_json()[1]["is_mutant"])

        self.assertEqual(3, response.get_json()[2]["id"])
        self.assertEqual(self.MUTANT_SEQUENCE_IN_DIAGONAL, response.get_json()[2]["sequence"])
        self.assertEqual(True, response.get_json()[2]["is_mutant"])

        self.assertEqual(4, response.get_json()[3]["id"])
        self.assertEqual(self.MUTANT_SEQUENCE_IN_DIAGONAL_INVERTED, response.get_json()[3]["sequence"])
        self.assertEqual(True, response.get_json()[3]["is_mutant"])

        self.assertEqual(5, response.get_json()[4]["id"])
        self.assertEqual(self.HUMAN_SEQUENCE, response.get_json()[4]["sequence"])
        self.assertEqual(False, response.get_json()[4]["is_mutant"])

    def test_get_stats(self):
        self.test_mutant_dna_in_row()
        self.test_mutant_dna_in_column()
        self.test_mutant_dna_in_diagonal()
        self.test_mutant_dna_in_diagonal_inverted()
        self.test_human_dna()

        response = self.app.get('/api/v1/stats', headers={"Content-Type": "application/json"})
        self.assertEqual(200, response.status_code)
        self.assertEqual(4, response.get_json()["count_mutant_dna"])
        self.assertEqual(1, response.get_json()["count_human_dna"])
        self.assertEqual(4 / 1, response.get_json()["ratio"])
