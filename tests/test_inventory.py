# tests/test_inventory.py
import pytest
from refinery.inventory_manager import InventoryManager

@pytest.fixture
def inventory_manager():
    return InventoryManager()

def test_add_to_inventory(inventory_manager):
    inventory_manager.add_to_inventory("Gasoline", 50)
    assert inventory_manager.get_inventory()["Gasoline"] == 50

def test_remove_from_inventory(inventory_manager):
    inventory_manager.add_to_inventory("Crude Oil", 80)
    assert inventory_manager.remove_from_inventory("Crude Oil", 30) is True
    assert inventory_manager.get_inventory()["Crude Oil"] == 50

def test_remove_more_than_exists(inventory_manager):
    inventory_manager.add_to_inventory("Diesel", 20)
    assert inventory_manager.remove_from_inventory("Diesel", 30) is False
    assert inventory_manager.get_inventory()["Diesel"] == 20
