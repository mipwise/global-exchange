# GlobalEx Co.

GlobalEx Co. is a global company that operates in Europe, South America, North America, and Asia. Due to the nature of the company's operations, at the end of each month, the firm needs to transfer money to cover its cash requirements.

The cash requirements in millions of monetary units can be found in the table below:

| Symbol |       Currency        | Surplus | Requirements |
| :----: | :-------------------: | :-----: | :----------: |
|  BRL   |    Brazilian Real     |   8.5   |     0.0      |
|  CNY   | Chinese Yuan Renminbi |  23.0   |     0.0      |
|  EUR   |         Euro          |   6.8   |     0.0      |
|  GBP   |         Pound         |   0.0   |     2.1      |
|  USD   |       US Dollar       |   0.0   |     5.0      |

The currency exchange rates offered by the bank GlobalEx works are given below:

| Symbol |   USD    |   GBP   |   EUR    |   CNY    |   BRL    |
| :----: | :------: | :-----: | :------: | :------: | :------: |
|  USD   |    1     | 1.23561 | 1.08251  | 0.147429 | 0.192022 |
|  GBP   | 0.809242 |    1    | 0.876083 | 0.119322 | 0.155225 |
|  EUR   | 0.923776 | 1.14149 |    1     | 0.136199 | 0.177097 |
|  CNY   | 6.78293  | 8.38067 | 7.34219  |    1     | 1.30038  |
|  BRL   | 5.20774  | 6.43826 | 5.64662  | 0.769005 |    1     |

For this month, the company ended up with five currencies: USD, GBP, EUR, CNY, and BRL.

For example, in order to satisfy the requirement of 2.1 million Pounds, GlobalEx could use one of the currencies in which it has a surplus, namely BRL, CNY, or EUR. More than that, it could choose to exchange between any of the currencies for then satisfy the requirements.

On top of the exchange rate, the bank charges different fees for different pairs of currencies:

| From | To  | Exchange Rate | Fixed Fee | Variable Fee Tier 1 | Amount Tier 2 (Millions) | Variable Fee Tier 2 |
| :--: | :-: | :-----------: | :-------: | :-----------------: | :----------------------: | :-----------------: |
| BRL  | BRL |       1       |     0     |          0          |            0             |          0          |
| BRL  | CNY |    1.30038    |   0.014   |        0.012        |            4             |        0.007        |
| BRL  | EUR |   0.177097    |   0.014   |        0.02         |            4             |        0.015        |
| BRL  | GBP |   0.155225    |   0.014   |        0.025        |            4             |        0.02         |
| BRL  | USD |   0.192022    |   0.014   |        0.018        |            4             |        0.013        |
| CNY  | BRL |   0.769005    |   0.015   |        0.012        |            5             |        0.007        |
| CNY  | CNY |       1       |     0     |          0          |            0             |          0          |
| CNY  | EUR |   0.136199    |   0.015   |        0.021        |            5             |        0.016        |
| CNY  | GBP |   0.119322    |   0.015   |        0.025        |            5             |        0.02         |
| CNY  | USD |   0.147429    |   0.015   |        0.017        |            5             |        0.012        |
| EUR  | BRL |    5.64662    |   0.011   |        0.02         |           1.5            |        0.015        |
| EUR  | CNY |    7.34219    |   0.011   |        0.021        |           1.5            |        0.016        |
| EUR  | EUR |       1       |     0     |          0          |            0             |          0          |
| EUR  | GBP |   0.876083    |   0.011   |        0.012        |           1.5            |        0.007        |
| EUR  | USD |    1.08251    |   0.011   |        0.015        |           1.5            |        0.01         |
| GBP  | BRL |    6.43826    |   0.01    |        0.025        |            1             |        0.02         |
| GBP  | CNY |    8.38067    |   0.01    |        0.025        |            1             |        0.02         |
| GBP  | EUR |    1.14149    |   0.01    |        0.012        |            1             |        0.007        |
| GBP  | GBP |       1       |     0     |          0          |            0             |          0          |
| GBP  | USD |    1.23561    |   0.01    |        0.014        |            1             |        0.01         |
| USD  | BRL |    5.20774    |   0.013   |        0.018        |            2             |        0.013        |
| USD  | CNY |    6.78293    |   0.013   |        0.017        |            2             |        0.012        |
| USD  | EUR |   0.923776    |   0.013   |        0.015        |            2             |        0.01         |
| USD  | GBP |   0.809242    |   0.013   |        0.014        |            2             |        0.01         |
| USD  | USD |       1       |     0     |          0          |            0             |          0          |

So, if GlobalEx decided to exchange 1 EUR per BRL it would receive $1 * 5.64662 * (1-0.007) = 5.60709 \, \text{BRL}$.
How can GlobalEx satisfy the requirements for the month minimizing the amount paid in fees?

## Formulation

Se our proposed formulation in the [globalex.ipynb](docs/globalex.ipynb) Jupyter Notebook.
