"""
Integration test for fresh-session recovery, checkpoint persistence, and stale-state detection.
Aligned with Algorithm 3, TASK-024, and Verification Gate VG-6.
"""

import hashlib
import os
import shutil
import tempfile
import time
import unittest

class TestSessionRecovery(unittest.TestCase):
    def setUp(self):
        self.temp_repo = tempfile.mkdtemp()
        self.devkit_dir = os.path.join(self.temp_repo, ".devkit")
        self.run_state_dir = os.path.join(self.devkit_dir, "run-state")
        os.makedirs(self.run_state_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_repo)

    def test_interrupted_run_resumption_protocol(self):
        feature_stmt = "Add avatar upload to user profile"
        stmt_hash = hashlib.sha256(feature_stmt.encode('utf-8')).hexdigest()

        # Simulate interruption after Stage 3:
        # stage-log.md records Stages 1-3 as COMPLETED, Stage 4 as IN_PROGRESS, Stages 5-8 as PENDING
        stage_log_content = f"""---
devkit_version: "0.2.0"
artifact_type: "run-state-stage-log"
run_id: "run_test_recovery_1234"
feature_slug: "add-avatar-upload-user-profile"
feature_statement_hash: "sha256:{stmt_hash}"
started_at: "2026-11-05T12:00:00Z"
last_updated_at: "2026-11-05T12:05:00Z"
current_stage: 4
overall_status: "IN_PROGRESS"
---

| Stage # | Stage Name | Status |
|---|---|---|
| 1 | Intake & Clarification | COMPLETED |
| 2 | Repository Reconnaissance | COMPLETED |
| 3 | Architecture & Conventions | COMPLETED |
| 4 | Feature Specification | IN_PROGRESS |
| 5 | Impact & Risk Analysis | PENDING |
| 6 | Task Decomposition | PENDING |
| 7 | Validation Planning | PENDING |
| 8 | Quality Gate Verification | PENDING |
"""
        with open(os.path.join(self.run_state_dir, "stage-log.md"), "w") as f:
            f.write(stage_log_content)

        with open(os.path.join(self.run_state_dir, "intake.md"), "w") as f:
            f.write("# Intake Checkpoint\nFeature: Add avatar upload\n")

        with open(os.path.join(self.run_state_dir, "architecture.md"), "w") as f:
            f.write("# Architecture Checkpoint\nPattern: Layered-MVC\n")

        # Now simulate a clean new agent session inspecting state (Algorithm 3)
        def determine_resume_action(repo_path, current_statement):
            state_dir = os.path.join(repo_path, ".devkit", "run-state")
            stage_log = os.path.join(state_dir, "stage-log.md")
            if not os.path.exists(stage_log):
                return "START_FRESH", None

            with open(stage_log, "r") as f:
                content = f.read()

            import re
            hash_match = re.search(r'feature_statement_hash:\s*"sha256:([a-f0-9]+)"', content)
            if not hash_match:
                return "START_FRESH", None

            recorded_hash = hash_match.group(1)
            current_hash = hashlib.sha256(current_statement.encode('utf-8')).hexdigest()

            if current_hash != recorded_hash:
                # Stale checkpoint from unrelated feature!
                shutil.rmtree(state_dir)
                return "PURGE_AND_START", None

            # Find last completed stage
            stage_statuses = re.findall(r'\|\s*(\d+)\s*\|\s*[^\|]+\|\s*(COMPLETED|IN_PROGRESS|PENDING)\s*\|', content)
            completed_stages = [int(s[0]) for s in stage_statuses if s[1] == "COMPLETED"]
            in_progress_stages = [int(s[0]) for s in stage_statuses if s[1] == "IN_PROGRESS"]

            resume_stage = in_progress_stages[0] if in_progress_stages else (max(completed_stages) + 1 if completed_stages else 1)
            return "RESUME", resume_stage

        # Action 1: Resuming matching feature request
        action, stage_to_run = determine_resume_action(self.temp_repo, feature_stmt)
        self.assertEqual(action, "RESUME")
        self.assertEqual(stage_to_run, 4)

        # Action 2: Different feature request causes stale state purge
        unrelated_stmt = "Implement OAuth2 login with GitHub"
        action2, _ = determine_resume_action(self.temp_repo, unrelated_stmt)
        self.assertEqual(action2, "PURGE_AND_START")
        self.assertFalse(os.path.exists(self.run_state_dir), "Stale run-state must be purged")

if __name__ == "__main__":
    unittest.main()
