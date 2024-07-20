import pytest
from src.core.holon import Holon

def test_holon_creation():
    holon = Holon("TestHolon", ["capability1", "capability2"])
    assert holon.name == "TestHolon"
    assert holon.capabilities == ["capability1", "capability2"]
    assert holon.parent is None
    assert len(holon.children) == 0

def test_holon_hierarchy():
    parent = Holon("Parent", ["parent_capability"])
    child = Holon("Child", ["child_capability"])
    parent.add_child(child)
    assert child in parent.children
    assert child.parent == parent

def test_holon_task_execution():
    holon = Holon("Worker", ["process_data"])
    task = {"type": "process_data", "data": "sample"}
    result = holon.execute_task(task)
    assert result["status"] == "success"

    invalid_task = {"type": "invalid_task"}
    result = holon.execute_task(invalid_task)
    assert result["status"] == "failure"

if __name__ == "__main__":
    pytest.main()
