from unittest import TestCase

from directories import reset, run_full_command, get_root


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
