from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from directories import get_root, list, reset, run_full_command


class TestDirectories(TestCase):
    def setUp(self) -> None:
        reset()
        return super().setUp()

    def test_initial(self):
        self.assertDictEqual({}, get_root())

    def test_create(self):
        run_full_command("create 1/2/3")
        self.assertDictEqual({"1": {"2": {"3": {}}}}, get_root())
        run_full_command("create 1/2")  # This gets ignored - already created
        self.assertDictEqual({"1": {"2": {"3": {}}}}, get_root())
        run_full_command("create 2/3")
        self.assertDictEqual({"1": {"2": {"3": {}}}, "2": {"3": {}}}, get_root())

    def test_delete(self):
        run_full_command("create 1/2/3")
        self.assertDictEqual({"1": {"2": {"3": {}}}}, get_root())
        run_full_command("delete 1/2/3")
        self.assertDictEqual({"1": {"2": {}}}, get_root())
        run_full_command("delete 1/2/3")  # ignored already deleted
        self.assertDictEqual({"1": {"2": {}}}, get_root())

    def test_move(self):
        run_full_command("create 1/2/3/4")
        self.assertDictEqual({"1": {"2": {"3": {"4": {}}}}}, get_root())
        run_full_command("move 1/2 5/6")
        self.assertDictEqual(
            {"1": {}, "5": {"6": {"3": {"4": {}}}}},
            get_root(),
        )

    def test_list(self):
        run_full_command("create 1/2")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            list()
            self.assertEqual(fake_out.getvalue(), "1\n  2\n")
