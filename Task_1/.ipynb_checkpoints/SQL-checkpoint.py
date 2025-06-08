"""
The database loan.db consists of 5 tables:
   1. customers - table containing customer data
   2. loans - table containing loan data pertaining to customers
   3. credit - table containing credit and creditscore data pertaining to customers
   4. repayments - table containing loan repayment data pertaining to customers
   5. months - table containing month name and month ID data

You are required to make use of your knowledge in SQL to query the database object (saved as loan.db) and return the requested information.
Simply fill in the vacant space wrapped in triple quotes per question (each function represents a question)


NOTE:
Each question in this section is isolated, for example, you do not need to consider how Q5 may affect Q4.
Remember to clean your data.

"""


def question_1():
    """
    Find the name, surname and customer ids for all the duplicated customer ids in the customers dataset.
    Return the `Name`, `Surname` and `CustomerID`
    """

    # The inner query is used to find the duplicated customer IDs. It returns a list of customer IDs that appear more than once.
    # The outer query checks the customers table for the IDs from the inner query and returns the name, surname and customer ID of the customers.
    qry = """SELECT DISTINCT Name, Surname, CustomerID FROM customers
            WHERE CustomerID IN (
                SELECT CustomerID FROM customers
                GROUP BY CustomerID
                HAVING COUNT(*)>1
            )
            """
    return qry


def question_2():
    """
    Return the `Name`, `Surname` and `Income` of all female customers in the dataset in descending order of income
    """

    # Select the name, surname and income where the gender is female and order the results by income in descending order.
    qry = """SELECT Name, Surname, Income 
            FROM customers
            WHERE Gender = 'Female'
            ORDER BY Income DESC
        """

    return qry


def question_3():
    """
    Calculate the percentage of approved loans by LoanTerm, with the result displayed as a percentage out of 100.
    ie 50 not 0.5
    There is only 1 loan per customer ID.
    """

    #Use a case statement to count the number of approved loans
    #Count all the loans 
    #Divide the number of approved loans by the total number of loans and multiply by 100 to get the percentage.
    #Group the results by LoanTerm.
    qry = """SELECT LoanTerm,
        100.0*SUM(CASE WHEN ApprovalStatus = 'Approved' THEN 1 ELSE 0 END)/COUNT(*) AS PercentageApproved
        FROM loans
        GROUP BY LoanTerm
      """

    return qry


def question_4():
    """
    Return a breakdown of the number of customers per CustomerClass in the credit data
    Return columns `CustomerClass` and `Count`
    """
    #Select the CustomerClass and Count number of clients 
    qry = """SELECT CustomerClass, COUNT(*) AS Count
            FROM credit
            GROUP BY CustomerClass
        """

    return qry


def question_5():
    """
    Make use of the UPDATE function to amend/fix the following: Customers with a CreditScore between and including 600 to 650 must be classified as CustomerClass C.
    """

    #Update the credit table to set the CustomerClass to C where the CreditScore is between 600 and 650.
    #Alternatively could use "WHERE CreditScore >= 600 AND CreditScore <= 650" but BETWEEN is easier to read.
    qry = """UPDATE credit
            SET CustomerClass = 'C'
            WHERE CreditScore BETWEEN 600 AND 650
        """

    return qry
