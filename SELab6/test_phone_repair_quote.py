
import pytest
from phone_repair_quote import repair_quote, repair_days, trade_in_value

# Example test cases
def test_budget_screen():
    assert repair_quote("screen", "budget", False, False) == 4600

def test_in_stock_quick():
    assert repair_days("battery", True, 2) == 1

# Repair quote test cases
def test_flagship_screen_express():
    assert repair_quote("screen", "flagship", False, True) == 9100

def test_battery_under_warranty():
    assert repair_quote("battery", "budget", True, False) == 300

def test_camera_flagship():
    assert repair_quote("camera", "flagship", False, False) == 5300

def test_charging_port_express():
    assert repair_quote("charging_port", "budget", False, True) == 1600

def test_unknown_part():
    with pytest.raises(ValueError, match="unknown part"):
        repair_quote("speaker", "budget", False, False)

def test_unknown_brand_tier():
    with pytest.raises(ValueError, match="unknown brand tier"):
        repair_quote("battery", "premium", False, False)

def test_screen_under_warranty():
    assert repair_quote("screen", "budget", True, False) == 4600

# Repair days test cases
def test_no_technicians():
    assert repair_days("battery", True, 0) == 3

def test_battery_out_of_stock():
    assert repair_days("battery", False, 2) == 3

def test_screen_out_of_stock():
    assert repair_days("screen", False, 2) == 6

def test_camera_out_of_stock_no_technicians():
    assert repair_days("camera", False, 0) == 8

# Trade-in test cases
def test_invalid_original_price():
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(0, 12, False)

def test_negative_age():
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(10000, -1, False)

def test_trade_in_over_48_months():
    assert trade_in_value(10000, 49, False) == 0

def test_trade_in_first_year():
    assert trade_in_value(10000, 12, False) == 6000

def test_trade_in_second_year():
    assert trade_in_value(10000, 24, False) == 4000

def test_trade_in_over_two_years():
    assert trade_in_value(10000, 36, False) == 2000

def test_trade_in_cracked_screen():
    assert trade_in_value(10000, 12, True) == 3000
