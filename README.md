# GlobalExchange

GlobalExchange is a global company that operates in Europe, South America, North America, and Asia. Due to the nature of the company's operations, at the end of each month, the firm needs to transfer money to cover its cash requirements, maybe to pay its employees, pay its suppliers in different countries or balance its accounts.
For this month, the company ended up with five currency requirements: USD, GBP, EUR, CNY, and BRL.

The cash requirements **in millions** of monetary units can be found in the table below:

| Symbol |       Currency        | Surplus | Max Surplus | Requirements | Balance |
| :----: | :-------------------: | :-----: | :---------: | :----------: | :-----: |
|  BRL   |    Brazilian Real     |   8.5   |      6      |     1.3      |   7.2   |
|  CNY   | Chinese Yuan Renminbi |  23.5   |    15.5     |      3       |  20.5   |
|  EUR   |         Euro          |   6.8   |     30      |     0.7      |   6.1   |
|  GBP   |         Pound         |    0    |    10.5     |     2.1      |  -2.1   |
|  USD   |       US Dollar       |    0    |     200     |      5       |   -5    |

For example, in order to satisfy the requirement of 2.1 million Pounds, GlobalEx could use one of the currencies in which it has a surplus, namely BRL, CNY, or EUR. More than that, it could choose to exchange between any of the currencies to then satisfy the requirements.

To do this transfer, the company works with a bank. The currency exchange rates offered by the bank GlobalEx works are given below:

| Symbol |   USD    |   GBP   |   EUR    |   CNY    |   BRL    |
| :----: | :------: | :-----: | :------: | :------: | :------: |
|  USD   |    1     | 1.23561 | 1.08251  | 0.147429 | 0.192022 |
|  GBP   | 0.809242 |    1    | 0.876083 | 0.119322 | 0.155225 |
|  EUR   | 0.923776 | 1.14149 |    1     | 0.136199 | 0.177097 |
|  CNY   | 6.78293  | 8.38067 | 7.34219  |    1     | 1.30038  |
|  BRL   | 5.20774  | 6.43826 | 5.64662  | 0.769005 |    1     |

For each operation, the bank charges two fees: one "_national_" and one "_international_". On the other hand, depending on the amount being traded, the bank gives a discount over the international fee. For example, for the Brazilian Real the bank offers the following fee table:

| From | To  | Tier ID | Exchange Rate | National Fee | Tier Start | Tier End | International Fee |
| :--: | :-: | :-----: | :-----------: | :----------: | :--------: | :------: | :---------------: |
| BRL  | CNY |    1    |    1.30038    |    0.014     |     0      |    4     |       0.012       |
| BRL  | CNY |    2    |    1.30038    |    0.014     |     4      |   750    |       0.007       |
| BRL  | EUR |    1    |   0.177097    |    0.014     |     0      |    4     |       0.02        |
| BRL  | EUR |    2    |   0.177097    |    0.014     |     4      |   750    |       0.015       |
| BRL  | GBP |    1    |   0.155225    |    0.014     |     0      |    4     |       0.025       |
| BRL  | GBP |    2    |   0.155225    |    0.014     |     4      |   750    |       0.02        |
| BRL  | USD |    1    |   0.192022    |    0.014     |     0      |    4     |       0.018       |
| BRL  | USD |    2    |   0.192022    |    0.014     |     4      |   750    |       0.013       |

So, if GlobalExchange decided to exchange 2 Million BRL for CNY it would receive

$$2 \cdot 1.30038 \cdot (1-0.014 - 0.012) = 2.533 \text{Million CNY}.$$

On the other hand, if it chooses to exchange 4 Million BRL for CNY it would receive

$$4 \cdot 1.30038 \cdot (1-0.014 - 0.007) = 5.0922 \text{Million CNY}$$

How can GlobalExchange satisfy the requirements for the next month minimizing the amount paid in fees?

## Formulation

See our proposed formulation in the [global_exchange_formulation.ipynb](docs/global-exchange_formulation.ipynb) Jupyter Notebook.

### Additional Complexities

The real scenario can have numerous complexities that can be added to the model as additional rules.

- What if the company works with 20 currencies instead of 5?
- The company could use different banks instead of only one, and choose to trade different pairs between different banks.
