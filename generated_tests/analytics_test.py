
import pandas as pd
import pytest
from analytics import CustomerAnalytics

def test_customer_analytics_init_valid():
    data = pd.DataFrame({'customer_id': [1, 2, 3], 'purchase_amount': [100, 200, 300]})
    ca = CustomerAnalytics(data)
    assert isinstance(ca, CustomerAnalytics)
    assert ca.cleaned == False

def test_customer_analytics_init_invalid_type():
    with pytest.raises(TypeError):
        CustomerAnalytics([1,2,3])

def test_customer_analytics_init_missing_columns():
    data = pd.DataFrame({'customer_id': [1, 2, 3]})
    with pytest.raises(ValueError):
        CustomerAnalytics(data)
    data = pd.DataFrame({'purchase_amount': [100, 200, 300]})
    with pytest.raises(ValueError):
        CustomerAnalytics(data)


def test_clean_data():
    data = pd.DataFrame({'customer_id': [1, 1, 2, 3], 'purchase_amount': [100, 100, 200, None]})
    ca = CustomerAnalytics(data)
    ca.clean_data()
    assert ca.cleaned == True
    assert len(ca.data) == 3
    assert ca.data['purchase_amount'].isnull().sum() == 0
    assert ca.data['purchase_amount'][ca.data['customer_id'] == 3] == 0


def test_calculate_total_spent_uncleaned():
    data = pd.DataFrame({'customer_id': [1, 2, 3], 'purchase_amount': [100, 200, 300]})
    ca = CustomerAnalytics(data)
    with pytest.raises(RuntimeError):
        ca.calculate_total_spent()

def test_calculate_total_spent():
    data = pd.DataFrame({'customer_id': [1, 2, 3], 'purchase_amount': [100, 200, 300]})
    ca = CustomerAnalytics(data)
    ca.clean_data()
    totals = ca.calculate_total_spent()
    assert len(totals) == 3
    assert totals['total_spent'].sum() == 600

def test_get_top_customers():
    data = pd.DataFrame({'customer_id': [1, 2, 3, 4,5], 'purchase_amount': [100, 200, 300, 400,500]})
    ca = CustomerAnalytics(data)
    ca.clean_data()
    top_customers = ca.get_top_customers(n=2)
    assert len(top_customers) == 2
    assert top_customers['customer_id'].iloc[0] in [4,5]
    assert top_customers['customer_id'].iloc[1] in [4,5]


def test_flag_high_value_customers():
    data = pd.DataFrame({'customer_id': [1, 2, 3], 'purchase_amount': [100, 2000, 300]})
    ca = CustomerAnalytics(data)
    ca.clean_data()
    high_value_customers = ca.flag_high_value_customers(threshold=500)
    assert len(high_value_customers) == 3
    assert high_value_customers['high_value'][high_value_customers['customer_id'] == 2] == True
    assert high_value_customers['high_value'][high_value_customers['customer_id'] == 1] == False

