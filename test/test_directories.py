from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from directories import directory, run_full_command


def run_list_command_and_return_print_output():
    with patch("sys.stdout", new=StringIO()) as fake_out:
        run_full_command("LIST")
        return fake_out.getvalue()


EXPECTED_OUTPUT_1 = """fruits
  apples
    fuji
grains
vegetables
"""
EXPECTED_OUTPUT_2 = """foods
  fruits
    apples
      fuji
  grains
  vegetables
    squash
"""
EXPECTED_OUTPUT_3 = """foods
  fruits
  grains
  vegetables
    squash
"""


class TestDirectories(TestCase):
    def setUp(self) -> None:
        directory.reset()
        return super().setUp()

    def test_initial(self):
        self.assertDictEqual({}, directory.root)

    def test_create(self):
        run_full_command("create 1/2/3")
        self.assertDictEqual({"1": {"2": {"3": {}}}}, directory.root)
        run_full_command("create 1/2")  # This gets ignored - already created
        self.assertDictEqual({"1": {"2": {"3": {}}}}, directory.root)
        run_full_command("create 2/3")
        self.assertDictEqual({"1": {"2": {"3": {}}}, "2": {"3": {}}}, directory.root)

    def test_delete(self):
        run_full_command("create 1/2/3")
        self.assertDictEqual({"1": {"2": {"3": {}}}}, directory.root)
        run_full_command("delete 1/2/3")
        self.assertDictEqual({"1": {"2": {}}}, directory.root)
        run_full_command("delete 1/2/3")  # ignored already deleted
        self.assertDictEqual({"1": {"2": {}}}, directory.root)

    def test_move(self):
        run_full_command("create 1/2/3/4")
        self.assertDictEqual({"1": {"2": {"3": {"4": {}}}}}, directory.root)
        run_full_command("move 1/2 5/6")
        self.assertDictEqual(
            {"1": {}, "5": {"6": {"2": {"3": {"4": {}}}}}},
            directory.root,
        )

    def test_list(self):
        run_full_command("create 1/2")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            run_full_command("list")
            self.assertEqual(fake_out.getvalue(), "1\n  2\n")

    def test_all(self):
        run_full_command("CREATE fruits")
        run_full_command("CREATE vegetables")
        run_full_command("CREATE grains")
        run_full_command("CREATE fruits/apples")
        run_full_command("CREATE fruits/apples/fuji")
        self.assertEqual(run_list_command_and_return_print_output(), EXPECTED_OUTPUT_1)

        run_full_command("CREATE grains/squash")
        run_full_command("MOVE grains/squash vegetables")
        run_full_command("CREATE foods")
        run_full_command("MOVE grains foods")
        run_full_command("MOVE fruits foods")
        run_full_command("MOVE vegetables foods")
        self.assertEqual(run_list_command_and_return_print_output(), EXPECTED_OUTPUT_2)
        run_full_command("DELETE fruits/apples")
        run_full_command("DELETE foods/fruits/apples")

        self.assertEqual(run_list_command_and_return_print_output(), EXPECTED_OUTPUT_3)
