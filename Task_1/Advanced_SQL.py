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
The database will be reset when grading each section. Any changes made to the database in the previous `SQL` section can be ignored.
Each question in this section is isolated unless it is stated that questions are linked.
Remember to clean your data

"""


def question_1():
    """
    Make use of a JOIN to find the `AverageIncome` per `CustomerClass`
    """

    #The two tables needed are the customers and credit tables.
    #Use JOIN to combine the two tables on the CustomerID column.
    #Group the results by CustomerClass.
    #Use AVG to calculate the average income per CustomerClass.
    qry = """SELECT credit.CustomerClass, AVG(customers.Income) AS AverageIncome
            FROM credit
            JOIN customers ON credit.CustomerID = customers.CustomerID
            GROUP BY credit.CustomerClass
        """

    return qry


def question_2():
    """
    Make use of a JOIN to return a breakdown of the number of 'RejectedApplications' per 'Province'.
    Ensure consistent use of either the abbreviated or full version of each province, matching the format found in the customer table.
    """

    # #Join the two tables on the CustomerID column.
    # #Filter the results to only include rejected applications.
    # #Count the number of rejected applications per province.
    # #Group the results by province.
    # #This query shows the regions abbreviated or full version
    # #Change Region to Province.
    # 
    # qry = """SELECT Region AS Province, COUNT(*) as RejectedApplications
    #         FROM loans
    #         JOIN customers ON loans.CustomerID = customers.CustomerID
    #         WHERE loans.ApprovalStatus = 'Rejected'
    #         GROUP BY customers.Region
    #     """

    #Since we need to use the full version or abbreviated version of the province, we can use a CASE statement to return the full version.
    #To ensure clarity and to avoid confusion, we choose to use the full version.
    #Noticed that NW did not have a full version, chose "NW" as "NorthWest"
    qry = """SELECT 
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
    Making use of the `INSERT` function, create a new table called `financing` which will include the following columns:
    `CustomerID`,`Income`,`LoanAmount`,`LoanTerm`,`InterestRate`,`ApprovalStatus` and `CreditScore`

    Do not return the new table, just create it.
    """

    #Create a new table called financing.
    #Select the CustomerID, Income, LoanAmount, LoanTerm, InterestRate, ApprovalStatus and CreditScore from the customers, loans and credit tables.
    #Join the tables on the CustomerID column.
    qry = """CREATE TABLE financing AS
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


# Question 4 and 5 are linked


def question_4():
    """
    Using a `CROSS JOIN` and the `months` table, create a new table called `timeline` that sumarises Repayments per customer per month.
    Columns should be: `CustomerID`, `MonthName`, `NumberOfRepayments`, `AmountTotal`.
    Repayments should only occur between 6am and 6pm London Time.
    Null values to be filled with 0.

    Hint: there should be 12x CustomerID = 1.
    """
    #Create a new table called timeline.
    #We need to select the CustomerID and MonthName from the customers and months tables.
    #The NumberOfRepayments is calculated as the count of the RepaymentID's
    #The AmountTotal is calculated as the sum of the Amount's
    #Use COALESCE to fill in the null values with 0.
    #Cross join the customers and months tables to be able to get all the months for each customer.
    #Left join the repaymnets table on CustomerID, where the monthID is the same as the monthID in the months table 
    # and the repayment time is between 6am and 6pm. 6pm is inclusive. Could change the BETWEEN to >= '06' and < '18'to make it exclusive.
    #Group the results by CustomerID and MonthName.
    qry = """CREATE TABLE timeline AS
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
    Make use of conditional aggregation to pivot the `timeline` table such that the columns are as follows:
    `CustomerID`, `JanuaryRepayments`, `JanuaryTotal`,...,`DecemberRepayments`, `DecemberTotal`,...etc
    MonthRepayments columns (e.g JanuaryRepayments) should be integers

    Hint: there should be 1x CustomerID = 1
    """
    #Use conditional aggregation to pivot the timeline table.
    #Group the results by CustomerID.
    #Use SUM to calculate the total number of repayments and amount total for each month.
    #Use CASE WHEN to check if the month is January, February, etc.
    #Use ELSE 0 to fill in the null values with 0.
    qry = """SELECT
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


# QUESTION 6 and 7 are linked, Do not be concerned with timezones or repayment times for these question.


def question_6():
    """
    The `customers` table was created by merging two separate tables: one containing data for male customers and the other for female customers.
    Due to an error, the data in the age columns were misaligned in both original tables, resulting in a shift of two places upwards in
    relation to the corresponding CustomerID.

    Create a table called `corrected_customers` with columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender`
    Utilize a window function to correct this mistake in the new `CorrectedAge` column.
    Null values can be input manually - i.e. values that overflow should loop to the top of each gender.

    Also return a result set for this table (ie SELECT * FROM corrected_customers)
    """
    #create a new table called corrected_customers.
    #Create a CTE called numbered_customers.
    #The CTE is used to number the customers in each gender and to get the count of the customers in each gender.
    #The row_in_gender is the row number in each gender.
    #The gender_count is the count of the customers in each gender.
    #Select the original CustomerID, Age and Gender columns from the customers table.
    #We need to join the customers table with the numbered_customers CTE on the Gender column.
    #When joining we find the customer that is 2 rows ahead of the current customer.
    #This is done by using the modulo operator to wrap around or get the correct row number.
    #The +2 is for two rows ahead. The minus 1 is to make it 0 indexed to perform the modulo operation.
    #The +1 is to make it 1 indexed to get the correct row number.

    #One big issue with this logic is that it assumed that there was no duplicated CustomerID's in the customers table.
    #After initial testing, there is duplicated CustomerID's in the customers table such as customerID = 999
    #To fix this we can use a CTE to filter out the duplicated CustomerID's.
    qry = """CREATE TABLE corrected_customers AS
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
    Create a column in corrected_customers called 'AgeCategory' that categorizes customers by age.
    Age categories should be as follows:
        - `Teen`: CorrectedAge < 20
        - `Young Adult`: 20 <= CorrectedAge < 30
        - `Adult`: 30 <= CorrectedAge < 60
        - `Pensioner`: CorrectedAge >= 60

    Make use of a windows function to assign a rank to each customer based on the total number of repayments per age group. Add this into a "Rank" column.
    The ranking should not skip numbers in the sequence, even when there are ties, i.e. 1,2,2,2,3,4 not 1,2,2,2,5,6
    Customers with no repayments should be included as 0 in the result.

    Return columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender`, `AgeCategory`, `Rank`
    """
    #Create a new column called AgeCategory.
    #Use a CASE statement to categorize the customers by age.
    #Use DENSE_RANK function to rank the customers by the total number of repayments per age group.
    #The DENSE_RANK function is used to ensure that the ranking does not skip numbers in the sequence, even when there are ties.
    
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
