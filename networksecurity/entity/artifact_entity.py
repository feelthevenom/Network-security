from dataclasses import dataclass
import sys

@dataclass
class DataIngetionArtifact:
    train_file_path:str
    test_file_path:str