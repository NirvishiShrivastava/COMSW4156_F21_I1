from unittest import TestCase
import db
from sqlite3 import Error


class Test_TestGameboard(TestCase):

    def setUp(self):
        db.clear()
        db.init_db()

    def test_add_move(self):
        test_tuple = ('p2', "[[0, 0, 0, 0, 0, 0, 0],"
                            " [0, 0, 0, 0, 0, 0, 0],"
                            " [0, 0, 0, 0, 0, 0, 0],"
                            " [0, 0, 0, 0, 0, 0, 0],"
                            " [0, 0, 0, 0, 0, 0, 0],"
                            " ['red', 0, 0, 0, 0, 0, 0]]",
                      '', 'red', 'yellow', 41)
        db.add_move(test_tuple)
        state = db.getMove()
        self.assertEqual(state[0], 'p2')
        db.clear()

    def test_init_exception(self):
        with self.assertRaises(Error):
            db.init_db()

    def test_add_after_clear(self):
        db.clear()
        test_tuple = ('p2', "[[0, 0, 0, 0, 0, 0, 0],"
                            " [0, 0, 0, 0, 0, 0, 0],"
                            " [0, 0, 0, 0, 0, 0, 0],"
                            " [0, 0, 0, 0, 0, 0, 0],"
                            " [0, 0, 0, 0, 0, 0, 0],"
                            " ['red', 0, 0, 0, 0, 0, 0]]",
                      '', 'red', 'yellow', 41)
        with self.assertRaises(Error):
            db.add_move(test_tuple)


