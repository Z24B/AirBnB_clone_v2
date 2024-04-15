import unittest
from unittest.mock import patch
from console import HBNBCommand


class TestCreateCommand(unittest.TestCase):
    @patch('sys.stdout', return_value='')
    def test_create_with_valid_params(self, mock_stdout):
        console = HBNBCommand()
        console.onecmd("create State name=\"California\"")
        console.onecmd("create State name=\"Arizona\"")
        console.onecmd("create Place city_id=\"0001\" user_id=\"0001\" "
                       "name=\"My_little_house\" number_rooms=4 "
                       "number_bathrooms=2 max_guest=10 price_by_night=300 "
                       "latitude=37.773972 longitude=-122.431297")
        result = mock_stdout.getvalue()
        self.assertTrue(len(result.strip()) == 36)

    @patch('sys.stdout', return_value='')
    def test_create_with_invalid_params(self, mock_stdout):
        console = HBNBCommand()
        console.onecmd("create State invalid_param")
        console.onecmd("create Place invalid_param")
        result = mock_stdout.getvalue()
        self.assertEqual(result.strip(), "** class doesn't exist **")


if __name__ == '__main__':
    unittest.main()
