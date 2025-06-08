"""
Advanced SQL Analysis Module

This module contains complex SQL queries for advanced analysis of a loan database (loan.db).
The database consists of the following tables:
1. customers - Customer demographic and personal information
2. loans - Loan application and approval data
3. credit - Credit score and customer classification data
4. repayments - Loan repayment transaction records
5. months - Month reference data

Each function represents a specific analysis query. The queries are independent unless
explicitly stated as linked. The database state is reset between each section during grading.

Author: [Your Name]
Date: [Current Date]
"""


def question_1():
    """
    Calculates average income per customer credit class using table joins.
    
    Returns:
        str: SQL query that returns CustomerClass and the average income for each class
    """
    qry = """
    SELECT 
        credit.CustomerClass, 
        AVG(customers.Income) AS AverageIncome
    FROM credit
    JOIN customers ON credit.CustomerID = customers.CustomerID
    GROUP BY credit.CustomerClass
    """
    return qry


def question_2():
    """
    Analyzes loan rejection patterns by province.
    
    Returns:
        str: SQL query that returns Province (full name) and count of rejected applications
    """
    qry = """
    SELECT 
        CASE 
            WHEN Region = 'LP' THEN 'Limpopo'
            WHEN Region = 'GT' THEN 'Gauteng'
            WHEN Region = 'KZN' THEN 'KwaZulu-Natal'
            WHEN Region = 'MP' THEN 'Mpumalanga'
            WHEN Region = 'NC' THEN 'NorthernCape'
            WHEN Region = 'WC' THEN 'WesternCape'
            WHEN Region = 'EC' THEN 'EasternCape'
            WHEN Region = 'FS' THEN 'FreeState'
            WHEN Region = 'NW' THEN 'NorthWest'
            ELSE Region
        END AS Province,
        COUNT(*) as RejectedApplications
    FROM loans
    JOIN customers ON loans.CustomerID = customers.CustomerID
    WHERE loans.ApprovalStatus = 'Rejected'
    GROUP BY Province
    """
    return qry


def question_3():
    """
    Creates a consolidated financing table combining customer, loan, and credit data.
    
    Returns:
        str: SQL query that creates a new table 'financing' with combined customer,
             loan, and credit information
    """
    qry = """
    CREATE TABLE financing AS
    SELECT 
        customers.CustomerID,
        customers.Income,
        loans.LoanAmount,
        loans.LoanTerm,
        loans.InterestRate,
        loans.ApprovalStatus,
        credit.CreditScore
    FROM customers
    JOIN loans ON customers.CustomerID = loans.CustomerID
    JOIN credit ON customers.CustomerID = credit.CustomerID
    """
    return qry


def question_4():
    """
    Creates a timeline table summarizing customer repayments by month.
    Only includes repayments between 6am and 6pm London Time.
    
    Returns:
        str: SQL query that creates a new table 'timeline' with monthly repayment summaries
    """
    qry = """
    CREATE TABLE timeline AS
    SELECT
        customers.CustomerID,
        months.MonthName,
        COALESCE(COUNT(repayments.RepaymentID), 0) AS NumberOfRepayments,
        COALESCE(SUM(repayments.Amount), 0) AS AmountTotal
    FROM customers
    CROSS JOIN months
    LEFT JOIN repayments
        ON customers.CustomerID = repayments.CustomerID
        AND CAST(strftime('%m', repayments.RepaymentDate) AS INTEGER) = months.MonthID
        AND strftime('%H', repayments.RepaymentDate) BETWEEN '06' AND '18'
    GROUP BY customers.CustomerID, months.MonthName
    """
    return qry


def question_5():
    """
    Pivots the timeline table to show monthly repayment statistics per customer.
    
    Returns:
        str: SQL query that returns customer repayment data in a pivoted format
    """
    qry = """
    SELECT
        CustomerID,
        SUM(CASE WHEN MonthName = 'January' THEN NumberOfRepayments ELSE 0 END) AS JanuaryRepayments,
        SUM(CASE WHEN MonthName = 'January' THEN AmountTotal ELSE 0 END) AS JanuaryTotal,
        SUM(CASE WHEN MonthName = 'February' THEN NumberOfRepayments ELSE 0 END) AS FebruaryRepayments,
        SUM(CASE WHEN MonthName = 'February' THEN AmountTotal ELSE 0 END) AS FebruaryTotal,
        SUM(CASE WHEN MonthName = 'March' THEN NumberOfRepayments ELSE 0 END) AS MarchRepayments,
        SUM(CASE WHEN MonthName = 'March' THEN AmountTotal ELSE 0 END) AS MarchTotal,
        SUM(CASE WHEN MonthName = 'April' THEN NumberOfRepayments ELSE 0 END) AS AprilRepayments,
        SUM(CASE WHEN MonthName = 'April' THEN AmountTotal ELSE 0 END) AS AprilTotal,
        SUM(CASE WHEN MonthName = 'May' THEN NumberOfRepayments ELSE 0 END) AS MayRepayments,
        SUM(CASE WHEN MonthName = 'May' THEN AmountTotal ELSE 0 END) AS MayTotal,
        SUM(CASE WHEN MonthName = 'June' THEN NumberOfRepayments ELSE 0 END) AS JuneRepayments,
        SUM(CASE WHEN MonthName = 'June' THEN AmountTotal ELSE 0 END) AS JuneTotal,
        SUM(CASE WHEN MonthName = 'July' THEN NumberOfRepayments ELSE 0 END) AS JulyRepayments,
        SUM(CASE WHEN MonthName = 'July' THEN AmountTotal ELSE 0 END) AS JulyTotal,
        SUM(CASE WHEN MonthName = 'August' THEN NumberOfRepayments ELSE 0 END) AS AugustRepayments,
        SUM(CASE WHEN MonthName = 'August' THEN AmountTotal ELSE 0 END) AS AugustTotal,
        SUM(CASE WHEN MonthName = 'September' THEN NumberOfRepayments ELSE 0 END) AS SeptemberRepayments,
        SUM(CASE WHEN MonthName = 'September' THEN AmountTotal ELSE 0 END) AS SeptemberTotal,
        SUM(CASE WHEN MonthName = 'October' THEN NumberOfRepayments ELSE 0 END) AS OctoberRepayments,
        SUM(CASE WHEN MonthName = 'October' THEN AmountTotal ELSE 0 END) AS OctoberTotal,
        SUM(CASE WHEN MonthName = 'November' THEN NumberOfRepayments ELSE 0 END) AS NovemberRepayments,
        SUM(CASE WHEN MonthName = 'November' THEN AmountTotal ELSE 0 END) AS NovemberTotal,
        SUM(CASE WHEN MonthName = 'December' THEN NumberOfRepayments ELSE 0 END) AS DecemberRepayments,
        SUM(CASE WHEN MonthName = 'December' THEN AmountTotal ELSE 0 END) AS DecemberTotal
    FROM timeline
    GROUP BY CustomerID
    """
    return qry


def question_6():
    """
    Creates a corrected customers table to fix age data misalignment.
    Uses window functions to shift age data by two positions within each gender group.
    
    Returns:
        str: SQL query that creates and populates the corrected_customers table
    """
    qry = """
    CREATE TABLE corrected_customers AS
    WITH distinct_customers AS (
        SELECT
            CustomerID,
            Age,
            Gender,
            ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY (SELECT 1)) AS rn
        FROM customers
    ),
    unique_filtered_customers AS (
        SELECT CustomerID, Age, Gender
        FROM distinct_customers
        WHERE rn = 1
    ),
    numbered_customers AS (
        SELECT
            CustomerID,
            Age,
            Gender,
            ROW_NUMBER() OVER (PARTITION BY Gender ORDER BY CustomerID) AS row_in_gender,
            COUNT(*) OVER (PARTITION BY Gender) AS gender_count
        FROM unique_filtered_customers
    )
    SELECT
        original.CustomerID,
        original.Age,
        shifted.Age AS CorrectedAge,
        original.Gender
    FROM numbered_customers AS original
    JOIN numbered_customers AS shifted
        ON original.Gender = shifted.Gender
        AND shifted.row_in_gender = ((original.row_in_gender + 2 - 1) % original.gender_count) + 1
    ORDER BY original.Gender, original.CustomerID;

    SELECT * FROM corrected_customers;
    """
    return qry


def question_7():
    """
    Analyzes customer repayment patterns by age category.
    Categorizes customers into age groups and ranks them by total repayments.
    
    Returns:
        str: SQL query that returns customer analysis with age categories and repayment rankings
    """
    qry = """
    SELECT
        corrected_customers.CustomerID,
        corrected_customers.Age,
        corrected_customers.CorrectedAge,
        corrected_customers.Gender,
        CASE
            WHEN corrected_customers.CorrectedAge < 20 THEN 'Teen'
            WHEN corrected_customers.CorrectedAge >= 20 AND corrected_customers.CorrectedAge < 30 THEN 'Young Adult'
            WHEN corrected_customers.CorrectedAge >= 30 AND corrected_customers.CorrectedAge < 60 THEN 'Adult'
            ELSE 'Pensioner'
        END AS AgeCategory,
        DENSE_RANK() OVER (PARTITION BY
            CASE
                WHEN corrected_customers.CorrectedAge < 20 THEN 'Teen'
                WHEN corrected_customers.CorrectedAge >= 20 AND corrected_customers.CorrectedAge < 30 THEN 'Young Adult'
                WHEN corrected_customers.CorrectedAge >= 30 AND corrected_customers.CorrectedAge < 60 THEN 'Adult'
                ELSE 'Pensioner'
            END
            ORDER BY COALESCE(SUM(r.Amount), 0) DESC
        ) AS Rank
    FROM corrected_customers
    LEFT JOIN repayments AS r
        ON corrected_customers.CustomerID = r.CustomerID
    GROUP BY
        corrected_customers.CustomerID,
        corrected_customers.Age,
        corrected_customers.CorrectedAge,
        corrected_customers.Gender
    ORDER BY
        AgeCategory, Rank, corrected_customers.CustomerID
    """
    return qry
