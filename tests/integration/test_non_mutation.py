"""
Safety test verifying strict source code non-mutation during feature planning.
Aligned with Quality Gate QG-H5 and Implementation Plan TASK-025.
"""

import hashlib
import os
import shutil
import tempfile
import unittest

from tests.integration.integration_runner import simulate_feature_planning

def compute_dir_fingerprint(directory: str) -> dict:
    """Computes SHA-256 hashes for all files in directory tree, excluding .devkit."""
    fingerprint = {}
    for root, dirs, files in os.walk(directory):
        if ".devkit" in root:
            continue
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, directory)
            with open(full_path, "rb") as fp:
                fingerprint[rel_path] = hashlib.sha256(fp.read()).hexdigest()
    return fingerprint

class TestSourceCodeNonMutation(unittest.TestCase):
    def setUp(self):
        self.fixtures_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "fixtures")
        )
        self.test_repo = tempfile.mkdtemp()
        # Copy sample_app to temporary repo location
        shutil.copytree(os.path.join(self.fixtures_dir, "sample_app"), self.test_repo, dirs_exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_repo)

    def test_zero_application_source_mutation(self):
        # 1. Take pre-planning snapshot
        pre_hashes = compute_dir_fingerprint(self.test_repo)
        self.assertGreater(len(pre_hashes), 0, "Repo should contain source files")

        # 2. Execute planning run
        feature_stmt = "Add avatar upload endpoint to user router"
        result = simulate_feature_planning(
            repo_root=self.test_repo,
            feature_statement=feature_stmt
        )

        # 3. Take post-planning snapshot
        post_hashes = compute_dir_fingerprint(self.test_repo)

        # 4. Assert source code is completely untouched
        self.assertEqual(
            pre_hashes,
            post_hashes,
            "Application source files or existing tests were modified during planning!"
        )

        # 5. Verify all written files are strictly confined to .devkit/
        for root, dirs, files in os.walk(self.test_repo):
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, self.test_repo)
                if rel_path not in pre_hashes:
                    self.assertTrue(
                        rel_path.startswith(".devkit"),
                        f"Unexpected file created outside .devkit/: {rel_path}"
                    )

if __name__ == "__main__":
    unittest.main()
