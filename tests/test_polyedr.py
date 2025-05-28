import unittest
from unittest.mock import patch, mock_open
from math import sqrt

from shadow.polyedr import Polyedr


# Тестирует простой параллелепипед
class TestPolyedr1(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        fake_file_content = """1.0	0.0	0.0	0.0
8	6	24
0.0 1.0 0.0
3.0 1.0 0.0
3.0 -1.0 0.0
0.0 -1.0 0.0
0.0 1.0 1.0
3.0 1.0 1.0
3.0 -1.0 1.0
0.0 -1.0 1.0
4	1    2    3    4
4	5    6    7    8
4   5    1    4    8
4	2    6    7    3
4	1    2    6    5
4   3    4    8    7"""
        fake_file_path = 'data/holey_box.geom'
        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)

    def test_num_vertexes(self):
        self.assertEqual(len(self.polyedr.vertexes), 8)

    def test_num_facets(self):
        self.assertEqual(len(self.polyedr.facets), 6)

    def test_num_edges(self):
        self.assertEqual(len(self.polyedr.edges), 24)

    def test_num_good_facets(self):
        self.assertAlmostEqual(self.polyedr.good_area(), 12.0, places=5)


# Тестирует его же, но с гомотетией и углами Эйлера
class TestPolyedr2(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        fake_file_content = """40.0	30.0	-30.0	45.0
8	6	24
0.0 1.0 0.0
3.0 1.0 0.0
3.0 -1.0 0.0
0.0 -1.0 0.0
0.0 1.0 1.0
3.0 1.0 1.0
3.0 -1.0 1.0
0.0 -1.0 1.0
4	1    2    3    4
4	5    6    7    8
4   5    1    4    8
4	2    6    7    3
4	1    2    6    5
4   3    4    8    7"""
        fake_file_path = 'data/idk.geom'
        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)

    def test_num_vertexes(self):
        self.assertEqual(len(self.polyedr.vertexes), 8)

    def test_num_facets(self):
        self.assertEqual(len(self.polyedr.facets), 6)

    def test_num_edges(self):
        self.assertEqual(len(self.polyedr.edges), 24)

    def test_num_good_facets(self):
        self.assertAlmostEqual(self.polyedr.good_area(), 12.0, places=5)


# Тестирует ccc (а также deconvert_point)
class TestPolyedr3(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        fake_file_content = """10.0	45.0	0.0	0.0
8	2	8
0.0 0.0 0.0
5.0 0.0 0.0
5.0 5.0 0.0
0.0 5.0 0.0
1.0 1.0 3.0
6.0 1.0 3.0
6.0 6.0 3.0
1.0 6.0 3.0
4	1    2    3    4
4	5    6    7    8"""
        fake_file_path = 'data/hz.geom'
        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)

    def test_num_vertexes(self):
        self.assertEqual(len(self.polyedr.vertexes), 8)

    def test_num_facets(self):
        self.assertEqual(len(self.polyedr.facets), 2)

    def test_num_edges(self):
        self.assertEqual(len(self.polyedr.edges), 8)

    def test_deconvert_point(self):
        self.assertAlmostEqual(self.polyedr.deconvert_point(
            self.polyedr.facets[0].vertexes[2]).x, 5.0, places=5)
        self.assertAlmostEqual(self.polyedr.deconvert_point(
            self.polyedr.facets[0].vertexes[2]).y, 5.0, places=5)
        self.assertAlmostEqual(self.polyedr.deconvert_point(
            self.polyedr.facets[0].vertexes[2]).z, 0.0, places=5)

    def test_num_good_facets(self):
        self.assertAlmostEqual(self.polyedr.good_area(), 0.0, places=5)
