"""Unit tests for the PQC manager. liboqs is not required: without it the manager returns
placeholder numbers, and these tests check that those are labelled as not measured."""
import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest

from src.crypto import pqc_manager as pm
from src.crypto.pqc_manager import PQCAlgorithm, PQCManager


def run(coro):
    return asyncio.run(coro)


@pytest.fixture
def manager(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)  # benchmark results are written to ./data/performance
    monkeypatch.setattr(pm, "liboqs", None)  # force the no-liboqs path
    return PQCManager()


def test_security_levels_match_the_nist_category_names(manager):
    assert manager._get_security_level("Kyber512") == 128
    assert manager._get_security_level("Kyber1024") == 256
    assert manager._get_security_level("Dilithium3") == 192
    assert manager._get_security_level("unknown-alg") == 128  # documented default


def test_rsa_and_ecc_are_critical_and_aes256_is_not(manager):
    result = {a.algorithm: a for a in run(manager.analyze_crypto_migration(["RSA-2048", "ECC-256", "AES-256", "AES-128"]))}
    assert result["RSA-2048"].migration_priority == "CRITICAL" and result["RSA-2048"].risk_level == "EXTREME"
    assert result["ECC-256"].quantum_security == 0
    assert result["AES-128"].quantum_security == 64 and result["AES-128"].migration_priority == "HIGH"
    assert result["AES-256"].quantum_security == 128 and result["AES-256"].migration_priority == "MEDIUM"


def test_without_liboqs_results_are_marked_not_measured_and_saved_that_way(manager, tmp_path):
    perf = run(manager.evaluate_pqc_performance())
    assert set(perf) == set(manager.supported_algorithms)
    assert all(p.measured is False for p in perf.values())
    saved = [f for f in os.listdir(tmp_path / "data" / "performance") if f.endswith(".json")]
    assert len(saved) == 1
    data = json.load(open(tmp_path / "data" / "performance" / saved[0]))
    assert all(v["measured"] is False for v in data.values())


def test_recommendations_respect_min_security_and_return_at_most_three(manager):
    recs = run(manager.recommend_pqc_algorithms("v2x_security", {"min_security": 192}))
    assert 0 < len(recs) <= 3
    assert all(manager._get_security_level(a.value) >= 192 for a in recs)
    assert PQCAlgorithm.KYBER512 not in recs


def test_unknown_use_case_still_ranks(manager):
    assert run(manager.recommend_pqc_algorithms("something-else", {}))
