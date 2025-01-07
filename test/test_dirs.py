import pathlib
import os

import unittest
import tempfile

import teachershare as share


class DirectoryTest(unittest.TestCase):

    def setUp(self) -> None:
        self.dir = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.dir.name)

        # some students in classes
        (self.root / '06B' / 'teichler').mkdir(parents=True)
        (self.root / '05A' / 'fschreiber').mkdir(parents=True)
        (self.root / '06B' / 'abraun1').mkdir()
        (self.root / '05A' / 'aberg').mkdir()
        (self.root / '06B' / 'mmueller').mkdir()
        (self.root / '10C' / 'sniemann').mkdir(parents=True)
        (self.root / '09B').mkdir()  # empty class folder
        (self.root / 'example.txt').touch()  # file that does not matter

    def tearDown(self) -> None:
        self.dir.cleanup()
    
    # ---------------------------------------------------------------------------------------------

    def test_get_dirs_inside_returns_sorted_list_of_path_objects_for_each_directory(self) -> None:
        result = share.get_dirs_inside(self.root)

        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].name, '05A')
        self.assertEqual(result[1].name, '06B')
        self.assertEqual(result[2].name, '09B')
        self.assertEqual(result[3].name, '10C')

    def test_get_dirs_inside_returns_empty_list_on_empty_folder(self) -> None:
        result = share.get_dirs_inside(self.root / '09B')

        self.assertEqual(len(result), 0)

    def test_get_dirs_inside_raises_exception_on_missing_folder(self) -> None:
        with self.assertRaises(OSError):
            share.get_dirs_inside(self.root / '09F')
    
    # ---------------------------------------------------------------------------------------------

    def test_get_students_returns_dict_of_classnames_with_list_of_studentnames(self) -> None:
        result = share.get_students(self.root)

        self.assertEqual(len(result.keys()), 4)
        self.assertIn('05A', result)
        self.assertIn('06B', result)
        self.assertIn('09B', result)
        self.assertIn('10C', result)

        self.assertEqual(len(result['05A']), 2)
        self.assertEqual(result['05A'][0].name, 'aberg')
        self.assertEqual(result['05A'][1].name, 'fschreiber')

        self.assertEqual(len(result['06B']), 3)
        self.assertEqual(result['06B'][0].name, 'abraun1')
        self.assertEqual(result['06B'][1].name, 'mmueller')
        self.assertEqual(result['06B'][2].name, 'teichler')

        self.assertEqual(len(result['09B']), 0)

        self.assertEqual(len(result['10C']), 1)
        self.assertEqual(result['10C'][0].name, 'sniemann')

    # ---------------------------------------------------------------------------------------------
    
    def test_copy_element_copies_file_into_destination_dir(self) -> None:
        src = self.root / 'example.txt'
        dst = self.root / '05A' / 'aberg'
        dst_file = dst / 'example.txt'
        self.assertFalse(dst_file.exists())

        share.copy_element(src, dst)
        self.assertTrue(dst_file.exists())
        
    def test_copy_element_cannot_copy_file_to_destination_file(self) -> None:
        src = self.root / 'example.txt'
        dst = self.root / '05A' / 'aberg' / 'example.txt'

        with self.assertRaises(AssertionError):
            share.copy_element(src, dst)
        
    def test_copy_element_copies_dir_into_destination_dir(self) -> None:
        src = self.root / '06B'
        dst = self.root / '05A' / 'aberg'
        dst_tree = dst / '06B'
        dst_tree_sub = dst / '06B' / 'mmueller'
        self.assertFalse(dst_tree.exists())
        self.assertFalse(dst_tree_sub.exists())

        share.copy_element(src, dst)
        self.assertTrue(dst_tree.exists())
        self.assertTrue(dst_tree_sub.exists())
        
    def test_copy_element_cannot_copy_dir_to_destination_file(self) -> None:
        src = self.root / '06B'
        dst = self.root / '05A' / 'aberg' / 'example.txt'

        with self.assertRaises(AssertionError):
            share.copy_element(src, dst)
        

    # copy_element