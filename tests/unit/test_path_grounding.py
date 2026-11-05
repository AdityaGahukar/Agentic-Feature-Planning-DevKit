"""
Unit tests for path_grounding.py (Quality Gate QG-H1).
"""

import os
import shutil
import tempfile
import unittest

from tests.unit.path_grounding import extract_target_paths_from_task_breakdown, verify_path_grounding

class TestPathGrounding(unittest.TestCase):
    def setUp(self):
        self.repo_dir = tempfile.mkdtemp()
        # Create sample existing repository files
        os.makedirs(os.path.join(self.repo_dir, "src", "models"))
        os.makedirs(os.path.join(self.repo_dir, "src", "routes"))
        with open(os.path.join(self.repo_dir, "src", "models", "user.ts"), "w") as f:
            f.write("// User model")
        with open(os.path.join(self.repo_dir, "src", "routes", "api.ts"), "w") as f:
            f.write("// API routes")

    def tearDown(self):
        shutil.rmtree(self.repo_dir)

    def test_valid_grounded_paths(self):
        sample_md = """
### TASK-001: Extend user model
- **Target Files:**
  - Modify: `src/models/user.ts`
  - Create: `[NEW FILE: src/models/avatar.ts]`

### TASK-002: Add avatar route
- **Target Files:**
  - Modify: `src/routes/api.ts`
  - Create: `[NEW FILE: src/services/avatarService.ts]`
"""
        targets = extract_target_paths_from_task_breakdown(sample_md)
        is_valid, errors = verify_path_grounding(targets, self.repo_dir)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_hallucinated_modify_path(self):
        sample_md = """
### TASK-001: Edit non-existent file
- **Target Files:**
  - Modify: `src/models/ghost.ts`
  - Create: `[NEW FILE: src/models/avatar.ts]`
"""
        targets = extract_target_paths_from_task_breakdown(sample_md)
        is_valid, errors = verify_path_grounding(targets, self.repo_dir)
        self.assertFalse(is_valid)
        self.assertEqual(len(errors), 1)
        self.assertIn("Hallucinated modify path: 'src/models/ghost.ts'", errors[0])

    def test_create_path_already_exists(self):
        sample_md = """
### TASK-001: Try to create existing file as NEW FILE
- **Target Files:**
  - Create: `[NEW FILE: src/models/user.ts]`
"""
        targets = extract_target_paths_from_task_breakdown(sample_md)
        is_valid, errors = verify_path_grounding(targets, self.repo_dir)
        self.assertFalse(is_valid)
        self.assertEqual(len(errors), 1)
        self.assertIn("marked [NEW FILE] but already exists", errors[0])

if __name__ == "__main__":
    unittest.main()
