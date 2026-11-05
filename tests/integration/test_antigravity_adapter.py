"""
Integration test for Antigravity Adapter packaging and parameter handling.
Aligned with TASK-023 and LLD Section 9.
"""

import os
import re
import unittest

class TestAntigravityAdapter(unittest.TestCase):
    def setUp(self):
        self.root_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )
        self.skill_path = os.path.join(self.root_dir, "adapters", "antigravity", "SKILL.md")
        self.handler_path = os.path.join(self.root_dir, "adapters", "antigravity", "handler.md")

    def test_skill_manifest_validity(self):
        self.assertTrue(os.path.exists(self.skill_path), "SKILL.md must exist")
        with open(self.skill_path, "r") as f:
            content = f.read()

        # Check front-matter
        self.assertIn("name: feature-planner", content)
        self.assertIn("version: 0.2.0", content)
        self.assertIn("- read_file", content)
        self.assertIn("- write_file", content)
        self.assertIn("- run_command", content)

    def test_handler_presentation_format(self):
        self.assertTrue(os.path.exists(self.handler_path), "handler.md must exist")
        with open(self.handler_path, "r") as f:
            content = f.read()

        # Check file protocol URI format requirement
        self.assertIn("file://", content)
        self.assertIn("feature-spec.md", content)
        self.assertIn("task-breakdown.md", content)
        self.assertIn("run-summary.md", content)

    def test_parameter_extraction_simulation(self):
        # Test simulated prompt parser matching handler.md rules
        def parse_chat_prompt(prompt: str, active_cwd: str):
            # Extract depth
            depth = "auto"
            if "--depth shallow" in prompt:
                depth = "shallow"
            elif "--depth deep" in prompt:
                depth = "deep"

            # Extract stack hint
            stack_hint = None
            stack_match = re.search(r'using\s+([\w\s\+\-\.]+?)(?:\.|$|,|--)', prompt, re.IGNORECASE)
            if stack_match:
                stack_hint = stack_match.group(1).strip()

            # Clean feature statement
            clean_stmt = re.sub(r'--depth\s+\w+', '', prompt).strip()

            return {
                "repo_root": active_cwd,
                "feature_statement": clean_stmt,
                "depth": depth,
                "stack_hint": stack_hint
            }

        mock_prompt = "Add user avatar upload using S3 + Sharp --depth deep"
        parsed = parse_chat_prompt(mock_prompt, "/workspace/my-app")
        self.assertEqual(parsed["repo_root"], "/workspace/my-app")
        self.assertEqual(parsed["depth"], "deep")
        self.assertEqual(parsed["stack_hint"], "S3 + Sharp")
        self.assertIn("Add user avatar upload", parsed["feature_statement"])

if __name__ == "__main__":
    unittest.main()
