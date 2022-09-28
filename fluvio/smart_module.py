from enum import Enum
from typing import Optional
from pathlib import Path


class SmartModuleKind(Enum):
    FILTER = "filter"
    MAP = "map"
    FILTER_MAP = "filter_map"
    ARRAY_MAP = "array_map"


class FileExtensionError(Exception):
    """
    Custom error type to express incorrect extension types when passing in the wasm path to
    the SmartModule __init__ method.
    """


class SmartModule:
    """
    A representation of a Smart Module
    Should be bundled as a WASM module

    Exposes configuration options from the Rust API.
    """

    file_path: str
    kind: SmartModuleKind
    params: Optional[dict]

    def __init__(
        self,
        *,
        file_path: str,
        kind: SmartModuleKind,
        params: dict = None,
        **kwargs,
    ):
        """
        A Fluvio Smart Module can be used with a PartitionConsumer for adhoc filtering, mapping or
        other Smart Module features.

        This class represents the construction of a Smart Module. Upon initilisation it will verify
        the path correctness and file extension type. All smart module files should be packaged as a
        Web Assembly file with the .wasm extension.

        Args:
            file_path: str = The file path to the wasm module as a string
            kind: SmartModuleKind = An enum choice of avialable smart module types
            params: Optional[dict] = Other parameters that can be passed to the smart module

        Example:
            from fluvio.smart_module import SmartModule, SmartModuleKind

            smart_module = SmartModule("some/path/to/file.wasm", SmartModuleKind.FILTER)

        Raises:
            FileNotFoundError
            FileExtensionError


        Returns:
            SmartModule instance

        """

        if ".wasm" not in file_path:
            raise FileExtensionError(f"{file_path} is not the correct file type.")

        if Path(file_path).is_file():
            # Not too hot on this but verifies the path exists
            self.file_path = file_path
            self.kind = kind
            self.params = params
        else:
            raise FileNotFoundError(f"'{file_path}' could not be found, is this the correct path?")
