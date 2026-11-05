"""
Unit tests for slug_generator.py
"""

import os
import shutil
import tempfile
import unittest

from tests.unit.slug_generator import generate_feature_slug

class TestSlugGenerator(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_basic_slug_generation(self):
        stmt = "Add user profile avatar upload with S3 storage"
        slug = generate_feature_slug(stmt)
        self.assertEqual(slug, "add-user-profile-avatar-upload-s3-storage")
        self.assertLessEqual(len(slug), 60)

    def test_stop_words_filtering(self):
        stmt = "Implement a new authentication system for the admin dashboard in the app"
        # stop words like a, for, the, in are filtered
        slug = generate_feature_slug(stmt)
        self.assertNotIn("-the-", slug)
        self.assertNotIn("-for-", slug)
        self.assertNotIn("-in-", slug)
        self.assertTrue(slug.startswith("implement-new-authentication"))

    def test_special_characters_and_punctuation(self):
        stmt = "Fix: User's profile doesn't update (HTTP 500 error!)"
        slug = generate_feature_slug(stmt)
        self.assertRegex(slug, r'^[a-z0-9]+(-[a-z0-9]+)*$')
        self.assertNotIn("'", slug)
        self.assertNotIn("!", slug)
        self.assertNotIn("(", slug)

    def test_length_truncation(self):
        stmt = "Refactor exceptionally complicated distributed event streaming telemetry processor subsystem architecture"
        slug = generate_feature_slug(stmt)
        self.assertLessEqual(len(slug), 60)
        self.assertFalse(slug.endswith("-"))

    def test_empty_statement_fallback(self):
        self.assertEqual(generate_feature_slug(""), "unnamed-feature")
        self.assertEqual(generate_feature_slug("   "), "unnamed-feature")

    def test_collision_detection(self):
        stmt = "Add user avatar upload"
        # First creation
        slug1 = generate_feature_slug(stmt, self.test_dir)
        self.assertEqual(slug1, "add-user-avatar-upload")
        os.makedirs(os.path.join(self.test_dir, slug1))

        # Second creation (collision)
        slug2 = generate_feature_slug(stmt, self.test_dir)
        self.assertEqual(slug2, "add-user-avatar-upload-2")
        os.makedirs(os.path.join(self.test_dir, slug2))

        # Third creation (collision)
        slug3 = generate_feature_slug(stmt, self.test_dir)
        self.assertEqual(slug3, "add-user-avatar-upload-3")

if __name__ == "__main__":
    unittest.main()
