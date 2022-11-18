import sys
sys.path.insert(0, '../src')
from cws_heuristic import *

def test_first_solution():
    assert sol.cost == 1860.9424980238105, "Solution is not okey"

def test_BR():
    assert len(savingsList) == 0, "BR not applied"

if __name__ == "__main__":
    test_first_solution()
    test_BR()
    print("Everything passed")