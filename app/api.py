from flask import Blueprint, Response, jsonify, request

from app import db

from .models import DNA

bp = Blueprint("api", __name__, url_prefix="/api/v1")


@bp.route("/dnas", methods=["GET"])
def get_dnas():
    dnas = DNA.query.all()

    return jsonify([dna.serialize() for dna in dnas])


@bp.route("/mutant", methods=["POST"])
def add_sequence():
    sequence = request.get_json().get("dna")

    if not sequence:
        return Response("Please provide a DNA sequence", status=400)

    for row in sequence:
        if len(sequence) != len(row):
            return Response("DNA sequence should be NxN format", status=400)

    dna = DNA(sequence=sequence)
    dna.save()

    return Response(status=200 if dna.is_mutant else 403)


@bp.route("/stats", methods=["GET"])
def get_stats():
    total_mutants = DNA.query.filter_by(is_mutant=True).count()
    total_humans = DNA.query.filter_by(is_mutant=False).count()

    return jsonify(
        count_mutant_dna=total_mutants,
        count_human_dna=total_humans,
        ratio=total_mutants / total_humans,
    )
