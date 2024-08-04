import streamlit as st
import pandas as pd
import numpy as np
import io

#Display Image
st.image("Image.jpg",use_column_width=True)

st.title("Monthly Expense Sheet")

# Writing a simple introduction
st.write("This is a customised app created for calculating the monthly expenses")

# Initialize session state variables if they don't exist
if 'num_fields' not in st.session_state:
    st.session_state.num_fields = 1
if 'additional_fields' not in st.session_state:
    st.session_state.additional_fields = [{'label': '', 'amount': 0}]

# Function to add a new field
def add_field():
    st.session_state.num_fields += 1
    st.session_state.additional_fields.append({'label': '', 'amount': 0})

# Button to add a new field
if st.button('Add another expense'):
    add_field()

# Input fields for various expenses
Total_salary_amount = st.number_input("Please enter Total Salary", min_value=0)
Milk = st.number_input("Please enter the amount of Milk", min_value=0)
House_EMI = st.number_input("Please enter EMI amount", min_value=0)
Investment = st.number_input("Please enter Investment amount", min_value=0)
Therapy_fee = st.number_input("Please enter the Therapy Fee", min_value=0)
Car_expense = st.number_input("Please enter expense of car", min_value=0)
Mobile_Bill = st.number_input("Please enter the Mobile Bill", min_value=0)
Electricity_Bill = st.number_input("Please enter the Electricity bill amount", min_value=0)
Gas_Bill = st.number_input("Please enter the Gas bill", min_value=0)
Car_Cleaning = st.number_input("Please enter the Car cleaning amount", min_value=0)

# Dynamically added fields
for i in range(st.session_state.num_fields):
    if i >= len(st.session_state.additional_fields):
        st.session_state.additional_fields.append({'label': '', 'amount': 0})

    label = st.text_input(f"Expense {i + 1} Label", value=st.session_state.additional_fields[i]['label'], key=f'label_{i}')
    amount = st.number_input(f"Expense {i + 1} Amount", value=st.session_state.additional_fields[i]['amount'], min_value=0, key=f'amount_{i}')
    st.session_state.additional_fields[i]['label'] = label
    st.session_state.additional_fields[i]['amount'] = amount

# Function to calculate the remaining amount
def amt_remain(Total_salary_amount, Milk, House_EMI, Investment, Therapy_fee, Car_expense, Mobile_Bill, Electricity_Bill, Gas_Bill, Car_Cleaning, additional_expenses):
    total_expenses = Milk + House_EMI + Investment + Therapy_fee + Car_expense + Mobile_Bill + Electricity_Bill + Gas_Bill + Car_Cleaning
    for expense in additional_expenses:
        total_expenses += expense['amount']
    remain = Total_salary_amount - total_expenses
    return remain, total_expenses

# Button to trigger calculation
if st.button("Calculate Remaining Amount"):
    remaining_amount, total_expenses = amt_remain(Total_salary_amount, Milk, House_EMI, Investment, Therapy_fee, Car_expense, Mobile_Bill, Electricity_Bill, Gas_Bill, Car_Cleaning, st.session_state.additional_fields)
    st.write(f"The remaining amount is: {remaining_amount}")

    # Prepare the data for export
    data = {
        'Total Salary': [Total_salary_amount],
        'Milk': [Milk],
        'House EMI': [House_EMI],
        'Investment': [Investment],
        'Therapy Fee': [Therapy_fee],
        'Car Expense': [Car_expense],
        'Mobile Bill': [Mobile_Bill],
        'Electricity Bill': [Electricity_Bill],
        'Gas Bill': [Gas_Bill],
        'Car Cleaning': [Car_Cleaning],
        'Total Expenses': [total_expenses],
        'Remaining Amount': [remaining_amount]
    }

    for i, expense in enumerate(st.session_state.additional_fields):
        data[f'Expense {i + 1} Label'] = [expense['label']]
        data[f'Expense {i + 1} Amount'] = [expense['amount']]

    df = pd.DataFrame(data)

    # Create an Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Monthly Expenses')
        writer.close()
        processed_data = output.getvalue()

    # Create a download button
    st.download_button(
        label="Download Excel File",
        data=processed_data,
        file_name="monthly_expenses.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Optionally, you can provide additional insights or a summary
    st.write(f"Total Expenses: {total_expenses}")
    st.write(f"Total Salary: {Total_salary_amount}")
    st.write(f"Remaining Amount: {remaining_amount}")

