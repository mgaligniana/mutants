import numpy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql

from app import db


class DNA(db.Model):
    __tablename__ = "dnas"

    MUTANT_SEQUENCE = ["AAAA", "TTTT", "CCCC", "GGGG"]

    id = db.Column(db.Integer, primary_key=True)
    sequence = db.Column(postgresql.ARRAY(db.String))
    is_mutant = db.Column(db.Boolean, default=False)

    def __init__(self, sequence):
        self.sequence = sequence
        self.is_mutant = self.has_mutant_sequence(sequence)

    def serialize(self):
        return {"id": self.id, "sequence": self.sequence, "is_mutant": self.is_mutant}

    def has_mutant_sequence(self, sequence):
        return (
            self._check_rows(sequence)
            or self._check_columns(sequence)
            or self._check_diagonals(sequence)
        )

    def _check_rows(self, sequence):
        for row in sequence:
            for seq in self.MUTANT_SEQUENCE:
                if seq in row:
                    return True

        return False

    def _check_columns(self, sequence):
        n = len(sequence)

        for col in range(n):
            column = ""

            for row in sequence:
                column += row[col]

            for seq in self.MUTANT_SEQUENCE:
                if seq in column:
                    return True

        return False

    def _check_diagonals(self, sequence):
        n = len(sequence)
        matrix = numpy.array([list(row) for row in sequence])
        matrix_inverted = numpy.array([list(row)[::-1] for row in sequence])

        for m in [matrix, matrix_inverted]:
            for d in range(1 - n, n):
                diagonal = "".join(m.diagonal(d))

                for seq in self.MUTANT_SEQUENCE:
                    if seq in diagonal:
                        return True

        return False
