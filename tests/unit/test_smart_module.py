import unittest
from fluvio.smart_module import SmartModule, SmartModuleKind, FileExtensionError


class TestFluvioSmartModuleErrors(unittest.TestCase):
    def test_invalid_path_raises_exception(self):
        with self.assertRaises(FileNotFoundError):
            SmartModule(file_path="some/wrong/path/file.wasm", kind=SmartModuleKind.FILTER)

    def test_invalid_extension_raises_exception(self):
        with self.assertRaises(FileExtensionError):
            SmartModule(file_path="some/wrong/path/file.notawasm", kind=SmartModuleKind.FILTER)

    def test_keyword_arguments_only(self):
        with self.assertRaises(TypeError):
            # Pylint will show an error here, temporary disabling them
            # pylint: disable=missing-kwoa
            # pylint: disable=too-many-function-args
            SmartModule("some/path.wasm", SmartModuleKind.FILTER)
