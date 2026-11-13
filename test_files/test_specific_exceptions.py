import ast
from pathlib import Path
import unittest


class SpecificExceptionsTests(unittest.TestCase):
    def test_application_has_no_bare_or_catch_all_handlers(self) -> None:
        project = Path(__file__).resolve().parent.parent
        handlers_checked = 0
        for path in sorted(project.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8-sig"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ExceptHandler):
                    with self.subTest(file=path.name, line=node.lineno):
                        self.assertIsNotNone(node.type)
                        names = [name.id for name in ast.walk(node.type) if isinstance(name, ast.Name)]
                        self.assertNotIn("Exception", names)
                        self.assertNotIn("BaseException", names)
                    handlers_checked += 1
        self.assertGreater(handlers_checked, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
