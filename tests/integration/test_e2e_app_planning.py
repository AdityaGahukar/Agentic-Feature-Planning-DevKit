"""
Integration test suite for multi-archetype repository classification and planning.
Aligned with Verification Gate VG-5 and Implementation Plan Phase 5.
"""

import os
import shutil
import tempfile
import unittest

from tests.integration.integration_runner import classify_repository_archetype, simulate_feature_planning

class TestMultiArchetypeIntegration(unittest.TestCase):
    def setUp(self):
        self.fixtures_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "fixtures")
        )
        self.temp_output_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_output_dir)

    def test_classify_sample_app(self):
        app_path = os.path.join(self.fixtures_dir, "sample_app")
        archetype, score, scores = classify_repository_archetype(app_path)
        self.assertEqual(archetype, "Application")
        self.assertGreaterEqual(score, 8)
        self.assertGreater(scores["Application"], scores["Infrastructure"])

    def test_classify_sample_library(self):
        lib_path = os.path.join(self.fixtures_dir, "sample_library")
        archetype, score, scores = classify_repository_archetype(lib_path)
        self.assertEqual(archetype, "Library")
        self.assertGreaterEqual(score, 8)

    def test_classify_sample_data_eng(self):
        data_path = os.path.join(self.fixtures_dir, "sample_data_eng")
        archetype, score, scores = classify_repository_archetype(data_path)
        self.assertEqual(archetype, "Data Engineering")
        self.assertGreaterEqual(score, 8)

    def test_classify_sample_infra(self):
        infra_path = os.path.join(self.fixtures_dir, "sample_infra")
        archetype, score, scores = classify_repository_archetype(infra_path)
        self.assertEqual(archetype, "Infrastructure")
        self.assertGreaterEqual(score, 8)

    def test_classify_sample_monorepo(self):
        mono_path = os.path.join(self.fixtures_dir, "sample_monorepo")
        archetype, score, scores = classify_repository_archetype(mono_path)
        self.assertEqual(archetype, "Monorepo")
        self.assertGreaterEqual(score, 10)

    def test_end_to_end_planning_simulation_on_sample_app(self):
        app_path = os.path.join(self.fixtures_dir, "sample_app")
        feature_stmt = "Add avatar upload endpoint to user router"
        
        result = simulate_feature_planning(
            repo_root=app_path,
            feature_statement=feature_stmt,
            output_base_dir=self.temp_output_dir
        )

        self.assertEqual(result["archetype"], "Application")
        self.assertTrue(result["qg_traceability_pass"])
        self.assertTrue(result["qg_path_grounding_pass"])
        self.assertTrue(os.path.exists(os.path.join(result["plan_dir"], "feature-spec.md")))
        self.assertTrue(os.path.exists(os.path.join(result["plan_dir"], "task-breakdown.md")))
        self.assertTrue(os.path.exists(os.path.join(result["plan_dir"], "validation-plan.md")))

if __name__ == "__main__":
    unittest.main()
