import os

import numpy as np
import pandas as pd

"""
To answer the following questions, make use of datasets: 
    'scheduled_loan_repayments.csv'
    'actual_loan_repayments.csv'
These files are located in the 'data' folder. 

'scheduled_loan_repayments.csv' contains the expected monthly payments for each loan. These values are constant regardless of what is actually paid.
'actual_loan_repayments.csv' contains the actual amount paid to each loan for each month.

All loans have a loan term of 2 years with an annual interest rate of 10%. Repayments are scheduled monthly.
A type 1 default occurs on a loan when any scheduled monthly repayment is not met in full.
A type 2 default occurs on a loan when more than 15% of the expected total payments are unpaid for the year.

Note: Do not round any final answers.

"""


def calculate_df_balances(df_scheduled, df_actual):
    """
    This is a utility function that creates a merged dataframe that will be used in the following questions.
    This function will not be graded, do not make changes to it.

    Args:
        df_scheduled (DataFrame): Dataframe created from the 'scheduled_loan_repayments.csv' dataset
        df_actual (DataFrame): Dataframe created from the 'actual_loan_repayments.csv' dataset

    Returns:
        DataFrame: A merged Dataframe with additional calculated columns to help with the following questions.

    """

    df_merged = pd.merge(df_actual, df_scheduled)

    def calculate_balance(group):
        r_monthly = 0.1 / 12
        group = group.sort_values("Month")
        balances = []
        interest_payments = []
        loan_start_balances = []
        for index, row in group.iterrows():
            if balances:
                interest_payment = balances[-1] * r_monthly
                balance_with_interest = balances[-1] + interest_payment
            else:
                interest_payment = row["LoanAmount"] * r_monthly
                balance_with_interest = row["LoanAmount"] + interest_payment
                loan_start_balances.append(row["LoanAmount"])

            new_balance = balance_with_interest - row["ActualRepayment"]
            interest_payments.append(interest_payment)

            new_balance = max(0, new_balance)
            balances.append(new_balance)

        loan_start_balances.extend(balances)
        loan_start_balances.pop()
        group["LoanBalanceStart"] = loan_start_balances
        group["LoanBalanceEnd"] = balances
        group["InterestPayment"] = interest_payments
        return group

    df_balances = (
        df_merged.groupby("LoanID", as_index=False)
        .apply(calculate_balance)
        .reset_index(drop=True)
    )

    df_balances["LoanBalanceEnd"] = df_balances["LoanBalanceEnd"].round(2)
    df_balances["InterestPayment"] = df_balances["InterestPayment"].round(2)
    df_balances["LoanBalanceStart"] = df_balances["LoanBalanceStart"].round(2)

    return df_balances


# Do not edit these directories
root = os.getcwd()

if "Task_2" in root:
    df_scheduled = pd.read_csv("data/scheduled_loan_repayments.csv")
    df_actual = pd.read_csv("data/actual_loan_repayments.csv")
else:
    df_scheduled = pd.read_csv("Task_2/data/scheduled_loan_repayments.csv")
    df_actual = pd.read_csv("Task_2/data/actual_loan_repayments.csv")

df_balances = calculate_df_balances(df_scheduled, df_actual)


def question_1(df_balances):
    """
    Calculate the percent of loans that defaulted as per the type 1 default definition.

    Args:
        df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function

    Returns:
        float: The percentage of type 1 defaulted loans (ie 50.0 not 0.5)

    """

    #A type 1 default occurs on a loan when any scheduled monthly repayment is not met in full. 
    #Check that the actual repayment is less than the scheduled repayment.
    #Get the unique loanID's of the defaulted loans.
    defaulted_loans = df_balances[df_balances['ActualRepayment'] < df_balances['ScheduledRepayment']]['LoanID'].nunique()

    #Get the total number of loans.
    total_loans = df_balances['LoanID'].nunique()
    
    #Calculate the percentage of defaulted loans.
    default_rate_percent = (defaulted_loans / total_loans) * 100

    return default_rate_percent


def question_2(df_scheduled, df_balances):
    """
    Calculate the percent of loans that defaulted as per the type 2 default definition

    Args:
        df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function
        df_scheduled (DataFrame): Dataframe created from the 'scheduled_loan_repayments.csv' dataset

    Returns:
        float: The percentage of type 2 defaulted loans (ie 50.0 not 0.5)

    """
    #A type 2 default occurs on a loan when more than 15% of the expected total payments are unpaid for the year.
    #First calculate the total expected payments and the total actual payments for each loan.
    #It is assumed that it is only 1 year since months only go up to 12
    yearly_totals = df_balances.groupby('LoanID').agg({'ScheduledRepayment': 'sum', 'ActualRepayment': 'sum'}).reset_index()

    #Calculate the shortfall for each loan.
    yearly_totals['Shortfall'] = yearly_totals['ScheduledRepayment'] - yearly_totals['ActualRepayment']

    #Calculate the percentage shortfall for each loan.
    yearly_totals['ShortfallPercentage'] = (yearly_totals['Shortfall'] / yearly_totals['ScheduledRepayment']) * 100

    #Find the loans that defaulted (shortfall > 15%).
    defaulted_loans = yearly_totals[yearly_totals['ShortfallPercentage'] > 15]['LoanID'].nunique()

    #Get the total number of loans.
    total_loans = yearly_totals['LoanID'].nunique()

    #Calculate the percentage of defaulted loans.
    default_rate_percent = (defaulted_loans / total_loans) * 100

    return default_rate_percent


def question_3(df_balances):
    """
    Calculate the anualized portfolio CPR (As a %) from the geometric mean SMM.
    SMM is calculated as: (Unscheduled Principal)/(Start of Month Loan Balance)
    SMM_mean is calculated as (∏(1+SMM))^(1/12) - 1
    CPR is calcualted as: 1 - (1- SMM_mean)^12

    Args:
        df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function

    Returns:
        float: The anualized CPR of the loan portfolio as a percent.
    """
    #first copy and clean the dataframe to remove any rows with a zero loan balance.
    df = df_balances.copy()
    df = df[df['LoanBalanceStart'] > 0].dropna()

    # Calculate Unscheduled Principal
    df['UnscheduledPrincipal'] = df['ActualRepayment'] - df['ScheduledRepayment']

    #Ensure no negative Unscheduled Principal values
    df['UnscheduledPrincipal'] = df['UnscheduledPrincipal'].clip(lower=0)
    
    # Calculate total portfolio metrics by month
    portfolio_monthly = df.groupby('Month').agg({
        'UnscheduledPrincipal': 'sum',
        'LoanBalanceStart': 'sum'
    }).reset_index()
    
    # Calculate SMM for the portfolio each month
    portfolio_monthly['SMM'] = portfolio_monthly['UnscheduledPrincipal'] / portfolio_monthly['LoanBalanceStart']
    
    # Calculate the geometric mean across all months
    smm_mean = (1 + portfolio_monthly['SMM']).prod() ** (1/12) - 1
    
    # Calculate CPR
    cpr = 1 - (1 - smm_mean) ** 12
    
    # Convert to percentage
    cpr_percent = cpr * 100
    
    return cpr_percent


def question_4(df_balances):
    """
    Calculate the predicted total loss for the second year in the loan term.
    Use the equation: probability_of_default * total_loan_balance * (1 - recovery_rate).
    The probability_of_default value must be taken from either your question_1 or question_2 answer.
    Decide between the two answers based on which default definition you believe to be the more useful metric.
    Assume a recovery rate of 80%

    Args:
        df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function

    Returns:
        float: The predicted total loss for the second year in the loan term.

    """
    # Type 1 is more conservative as it picks up any missed payment.
    # Early risk assessment but could overstate the loss.
    probability_of_default = question_1(df_balances) / 100
    
    # Calculate the total loan balance at the end of year 1 (month 12)
    year1_end_balance = df_balances[df_balances['Month'] == 12]['LoanBalanceEnd'].sum()
    
    # Calculate the total loan balance for year 2
    # Since we have a 2-year term with 10% annual interest, we can calculate the expected
    # balance at the end of year 2 using the remaining principal and interest
    total_loan_balance = year1_end_balance * (1 + 0.10)
    
    # Calculate the predicted loss using the formula
    # probability_of_default * total_loan_balance * (1 - recovery_rate)
    # 80% recovery rate as specified
    recovery_rate = 0.80  
    predicted_loss = probability_of_default * total_loan_balance * (1 - recovery_rate)
    
    return predicted_loss
