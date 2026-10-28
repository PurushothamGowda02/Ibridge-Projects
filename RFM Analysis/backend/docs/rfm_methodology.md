# RFM Methodology

## What is RFM Analysis?

RFM (Recency, Frequency, Monetary) is a customer segmentation technique used in retail and e-commerce to identify and categorize customers based on their purchasing behavior. It helps businesses understand customer value and engagement patterns.

## The Three Metrics

### 1. Recency (R)
**Definition:** The number of days since a customer's most recent purchase.

- **Lower Recency = Better** — A customer who purchased recently is more engaged and likely to respond to marketing.
- **Higher Recency = Worse** — A customer who hasn't purchased in a long time may be at risk of churning.

**Example:** If today is December 31, 2023, and a customer's last purchase was December 15, 2023, their Recency is 16 days.

### 2. Frequency (F)
**Definition:** The total number of distinct transactions (invoices) a customer has made within the analysis period.

- **Higher Frequency = Better** — A customer who purchases often is loyal and engaged.
- **Lower Frequency = Worse** — A customer who purchases rarely may be a one-time buyer.

**Example:** A customer with 8 separate invoices over the year has a Frequency of 8.

### 3. Monetary (M)
**Definition:** The total amount of money a customer has spent across all their purchases.

- **Higher Monetary = Better** — A customer who spends more is more valuable to the business.
- **Lower Monetary = Worse** — A customer who spends little may not be worth significant marketing investment.

**Example:** A customer who has spent £1,234.56 across all their purchases has a Monetary value of 1234.56.

## Scoring System

Each metric (R, F, M) is assigned a score from **1 to 5** using quantile binning:

- **Score 5** = Top 20% (most favorable)
- **Score 4** = 20–40%
- **Score 3** = 40–60% (middle)
- **Score 2** = 60–80%
- **Score 1** = Bottom 20% (least favorable)

### Recency Scoring (Inverted)
Recency is **inverted** because lower recency is better:
- **R_Score 5** = Lowest Recency (most recent purchases)
- **R_Score 1** = Highest Recency (oldest purchases)

### Frequency & Monetary Scoring (Direct)
- **F_Score 5** = Highest Frequency (most purchases)
- **F_Score 1** = Lowest Frequency (fewest purchases)
- **M_Score 5** = Highest Monetary (most spending)
- **M_Score 1** = Lowest Monetary (least spending)

## RFM Score

The **RFM_Score** is a three-digit string formed by concatenating the three individual scores:

```
RFM_Score = R_Score + F_Score + M_Score
```

**Examples:**
- `555` = Most valuable customer (recent, frequent, high-spending)
- `111` = Least valuable customer (old, infrequent, low-spending)
- `451` = Recent, frequent, but low-spending customer

## Why Quantile Binning?

Quantile binning divides customers into equal-sized groups based on their metric values, rather than using fixed thresholds. This approach:

1. **Handles skewed distributions** — Real-world data often has outliers; quantiles adapt to the actual data distribution.
2. **Ensures balanced segments** — Each score level represents roughly 20% of the customer base.
3. **Is interpretable** — A score of 5 always means "top 20% in this metric."

## Interpreting Scores

- **555 (Champions)** — Your best customers. Recent, frequent, high-spending. Prioritize retention.
- **111 (Lost)** — Your worst customers. Haven't purchased recently, rarely buy, low spend. Consider win-back campaigns.
- **451 (Potential Loyalists)** — Recent and frequent but low-spending. Upsell opportunities.
- **154 (At Risk)** — High-spending but haven't purchased recently. Re-engagement campaigns needed.

## Use Cases

1. **Customer Retention** — Identify at-risk customers and target them with retention offers.
2. **Upselling & Cross-selling** — Target high-frequency, low-monetary customers with premium products.
3. **Marketing Budget Allocation** — Invest more in high-value segments (Champions, Loyal Customers).
4. **Churn Prediction** — Monitor customers moving from high to low recency scores.
5. **Personalization** — Tailor messaging and offers based on customer segment.

## Limitations

- **Doesn't account for product type** — All purchases are weighted equally.
- **Doesn't consider profit margins** — High-spending customers may not be the most profitable.
- **Static snapshot** — RFM scores are calculated at a point in time; they change as new data arrives.
- **No causation** — RFM identifies patterns but doesn't explain why customers behave a certain way.

## Further Reading

- [RFM Analysis on Wikipedia](https://en.wikipedia.org/wiki/RFM_(customer_value))
- [Customer Segmentation Best Practices](https://www.investopedia.com/terms/c/customer_segmentation.asp)
