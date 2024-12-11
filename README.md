# -Automated-Sales-Payout-System-for-MIS-Report-Processing-
Automated the processing of 60+ daily MIS reports using Python, ensuring accurate sales payouts to customer wallets with 87% reduced manual workload, 100% payout accuracy, and enhanced transparency and scalability.
![image](https://github.com/user-attachments/assets/43e598ec-f7af-4cb6-9e91-02c125b7c5a2)

![image](https://github.com/user-attachments/assets/e5cec431-3939-4c84-b0d6-b43a92a92cce)

ShiftPay, a new fintech startup, aims to empower individuals with financial independence through their innovative platform. By partnering with established financial organizations, ShiftPay offers a diverse range of financial products and services through their mobile app. Through the ShiftPay app, individuals can create profiles and become Shift Partners (SPs). These SPs have the opportunity to sell the financial products and services offered by ShiftPay to themselves and others. Each successful sale made by an SP triggers a commission payout process. When a sale is completed according to predefined rules, the affiliated financial organization pays a predetermined amount to ShiftPay. ShiftPay then deducts a commission from this amount and disburses the remaining funds to the respective Shift Partner. In summary, ShiftPay facilitates financial independence by allowing individuals to become SPs, sell financial products, and earn commissions on successful sales through their mobile app.

# Problem Statement:

As the ShiftPay app gains popularity and the number of Shift Partners (SPs) increases, managing the payout process for successful sales becomes increasingly challenging. Currently, ShiftPay relies on manually processing the MIS reports from financial organizations to determine successful sales events based on predetermined criteria. However, with the continuous growth of the app and the addition of more financial products and services, the manual handling of MIS reports becomes inefficient and there are more chances of errors in payout calculations. To address this issue, ShiftPay aims to automate the payout process using Python. By building an Automated Payout System, ShiftPay can streamline the calculation and disbursement of commissions to SPs, allowing the company to focus on other tasks. The automated system will be designed to handle incoming MIS reports, identify successful sales events, calculate the appropriate payouts based on predetermined rules, and disburse commissions to SPs. Moreover, ShiftPay wants to ensure that the automation model is flexible and scalable, allowing for easy incorporation of new services in the future. This means designing the system in a modular and adaptable way so that new financial products and services can be seamlessly integrated into the automation model without requiring significant rework.
In summary, ShiftPay seeks to build an Automated Payout System in Python to efficiently manage the increasing number of SPs and sales transactions, while also ensuring flexibility for future expansion of services.

# Data Sets And Success Event Calculations:
**1. MIS Integration:**
ShiftPay receives MIS reports from different financial organizations on daily, bi-weekly and weekly basis, currently limited to Savings Accounts and Personal Loans. These reports contain information about successful sales events. These MIS received through mails from the listed financial organizations. After receiving of these MIS, one dedicated team will upload these .csv files to the Azure container (for the simplicity of this project, we’ll read/write these files from/on local machine). In production, whenever there is any storage event occur in Azure container, a data pipeline will be triggered and run this model and calculate the payout for SPs.

**2. Data Processing:**
ShiftPay's database contains miscellaneous leads data, including details about Shift Partners (SPs) and the leads generated through the ShiftPay app. It's important to note that while MIS reports may include additional leads, the system should filter and fetch only the leads generated through the ShiftPay app. Payouts will only be made for these specific leads.

**3. Payout Events:**
Whenever there is a status update for a lead ID from "Pending" to "Success," a payout event should be triggered. This payout event will transfer the payout money to the SP's wallet. SPs can then choose to transfer the funds instantly to their bank account.

**4. Final Calculation:**
After processing the MIS and miscellaneous leads data, a final calculation table will be generated to serve as the basis for calculating payouts to Shift Partners (SPs). A data pipeline will be developed to handle the integration, processing, and updating of this table in the database. Once the final calculation table is updated in the database, the tech team will take over responsibility for executing the final payout to the SPs. This separation of tasks ensures a clear and efficient workflow, with the data pipeline handling the data processing and table updating, while the tech team manages the payout execution.

**5. Error Handling:**
In every iteration, there might be some errors while calculating the success events for any MIS, to handle most of these situation, we did the exception handling for calculations, in case of no error, all good, or if there is any error, then a message will be attached to the automated email with the MIS details in which we got the error while calculating the payouts. Also these error logs will be save to another file named as error_logs.csv with actual error description.

# Note:

All the payin and payout rules are defined in payin_payout_rules.csv file with success criteria.
Miscellaneous Leads table will act as a truth of source, at any point of time, we can refer this table to check the status of LeadId.
After every iteration of the model, we need to generate a summary report for successful sales and an error report in case if there is any error in payout calculations. Both reports should be included with an automated email to the concerned departments. <br>
A final table should have the following columns to push records into database:

a. CreatedAt <br>
b. SourceType <br>
c. MediumType <br>
d. ProductType <br>
e. SPId <br>
f. LeadId <br>
g. Status <br>
h. SubStatus <br>
i. DateOfSale <br>
j. DateOfRevenue <br>
k. KPI1PayinAmount <br>
l. KPI1PayoutAmount <br>
m. KPI2PayinAmount <br>
n. KPI2PayoutAmount <br>
o. TotalPayin <br>
p. TotalPayout
