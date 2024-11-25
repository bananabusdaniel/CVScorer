import project
from Candidate import Candidate
import pytest
import os
import sys

def main():

    print(os.path.abspath(__file__))
    test_file_analyzed()
    test_format_text()
    test_output_dict()

def test_file_analyzed():
    mock_candidates = []
    mock_candidates.append(Candidate("MelissaMNoritz", "MelissaMoritzCV2024.pdf", "Little experience", "Reichman", "0555555", "NA", "Good candidate", 75))
    mock_candidates.append(Candidate("DanielNama", "DanielsCV.pdf", "Lots of experience", "Boogy", "0555555", "NA", "Good candidate", 75))
    
    assert project.file_analyzed("MelissaMoritzCV2024.pdf", mock_candidates) == True
    assert project.file_analyzed("MelissaMoritzCV2024", mock_candidates) == False
    assert project.file_analyzed("RandomDocument", mock_candidates) == False
    # assert project.file_analyzed([]) == False

def test_output_dict():

    assert project.output_dict('{"full_name":"daniel", "num":3}') == {"full_name":"daniel", "num":3}
    assert project.output_dict('{"full_name":"melissa", "num":3}') == {"full_name":"melissa", "num":3}
    with pytest.raises(SystemExit):
        project.output_dict('{')

def test_format_text():    hello = "hello!"    test_text = project.read_txt_file("test_txt_file.txt")    assert project.format_text(test_text, hello=hello) == f"This should say hello!, hello!"if __name__ == "__main__":    main()