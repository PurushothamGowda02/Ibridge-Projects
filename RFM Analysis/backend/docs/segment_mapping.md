# Customer Segment Mapping

This document describes how RFM scores are mapped to customer segment labels in the RFM Analysis system.

## Segment Mapping Rules

The mapping uses a priority-ordered rule list. The first rule that matches a customer's R_Score and F_Score determines their segment. The final rule ("Others") is a catch-all that matches any remaining customers.

| Priority | Segment | R_Score | F_Score | Description |
|----------|---------|---------|---------|-------------|
| 1 | **Champions** | ≥ 4 | ≥ 4 | Your best customers. Recent, frequent, high-spending. Prioritize retention and loyalty programs. |
| 2 | **Loyal Customers** | ≥ 2 | ≥ 4 | Frequent buyers with good spending. Maintain engagement with regular offers and updates. |
| 3 | **Potential Loyalists** | ≥ 3 | ≥ 2 | Recent and moderately frequent. Nurture with personalized offers to increase frequency and spend. |
| 4 | **New Customers** | ≥ 4 | = 1 | Recent first-time or rare buyers. Welcome them and encourage repeat purchases. |
| 5 | **At Risk** | ≤ 2 | ≥ 3 | Used to be frequent but haven't purchased recently. Re-engagement campaigns needed. |
| 6 | **Lost** | ≤ 2 | ≤ 2 | Haven't purchased recently and rarely bought. Consider win-back campaigns or remove from active lists. |
| 7 | **Others** | — | — | All remaining combinations. Monitor for trends. |

## Segment Descriptions

### 1. Champions (R ≥ 4, F ≥ 4)
**Profile:** Your most valuable customers.
- **Characteristics:** Recent purchases, frequent transactions, high lifetime value.
- **Behavior:** Loyal, engaged, likely to recommend.
- **Action:** 
  - Reward with VIP programs, exclusive offers, and early access to new products.
  - Encourage referrals and testimonials.
  - Maintain regular communication.

### 2. Loyal Customers (F ≥ 4, R ≥ 2)
**Profile:** Consistent, reliable customers.
- **Characteristics:** Frequent buyers, good spending, but may not be the most recent.
- **Behavior:** Stable, predictable purchase patterns.
- **Action:**
  - Maintain engagement with regular newsletters and offers.
  - Upsell premium products or services.
  - Recognize loyalty with rewards programs.

### 3. Potential Loyalists (R ≥ 3, F ≥ 2)
**Profile:** Customers with growth potential.
- **Characteristics:** Recent activity, moderate purchase frequency, room to increase spend.
- **Behavior:** Showing interest but not yet fully committed.
- **Action:**
  - Personalized recommendations based on purchase history.
  - Incentivize larger purchases or higher frequency.
  - Nurture with targeted campaigns.

### 4. New Customers (R ≥ 4, F = 1)
**Profile:** First-time or very rare buyers.
- **Characteristics:** Recent purchase, but minimal transaction history.
- **Behavior:** Testing the brand, not yet committed.
- **Action:**
  - Welcome campaigns and onboarding.
  - Encourage repeat purchases with first-time buyer discounts.
  - Gather feedback to improve experience.

### 5. At Risk (R ≤ 2, F ≥ 3)
**Profile:** Customers who are slipping away.
- **Characteristics:** Used to purchase frequently but haven't recently.
- **Behavior:** Engagement declining, may be switching to competitors.
- **Action:**
  - Win-back campaigns with special offers.
  - Personalized re-engagement emails.
  - Survey to understand reasons for inactivity.
  - Consider loyalty incentives.

### 6. Lost (R ≤ 2, F ≤ 2)
**Profile:** Inactive, low-value customers.
- **Characteristics:** Haven't purchased recently, rarely bought in the past.
- **Behavior:** Minimal engagement, low lifetime value.
- **Action:**
  - Consider removing from active marketing lists.
  - Occasional win-back campaigns (low investment).
  - Focus marketing budget on higher-value segments.
  - Archive for future re-engagement if business model changes.

### 7. Others
**Profile:** Miscellaneous combinations not covered by above rules.
- **Characteristics:** Varies; typically edge cases or unusual patterns.
- **Behavior:** Requires individual analysis.
- **Action:**
  - Monitor for trends.
  - May warrant custom strategies based on specific patterns.

## Implementation Notes

1. **Priority Matters:** Rules are evaluated in order. For example, a customer with R=5, F=5 matches both "Champions" and "Loyal Customers," but is assigned "Champions" because that rule is evaluated first.

2. **Catch-All Rule:** The "Others" segment ensures every customer receives a segment label, even if they don't match any specific rule.

3. **Dynamic Scoring:** As new transaction data arrives, customers' RFM scores change, and they may move to different segments. Monitor segment transitions to identify trends.

4. **Customization:** These rules are based on industry best practices but can be customized based on your business model, product type, and strategic goals.

## Example Scenarios

### Scenario 1: High-Value Customer
- **R_Score:** 5 (purchased last week)
- **F_Score:** 5 (50+ purchases)
- **M_Score:** 5 (£10,000+ spent)
- **RFM_Score:** 555
- **Segment:** Champions
- **Action:** VIP treatment, exclusive offers, loyalty rewards.

### Scenario 2: Declining Customer
- **R_Score:** 2 (last purchase 3 months ago)
- **F_Score:** 4 (20+ purchases historically)
- **M_Score:** 3 (£2,000 spent)
- **RFM_Score:** 243
- **Segment:** At Risk
- **Action:** Win-back campaign, special offer, check-in email.

### Scenario 3: New Buyer
- **R_Score:** 5 (purchased last week)
- **F_Score:** 1 (first purchase)
- **M_Score:** 2 (£50 spent)
- **RFM_Score:** 512
- **Segment:** New Customers
- **Action:** Welcome email, encourage repeat purchase, gather feedback.

### Scenario 4: Inactive Customer
- **R_Score:** 1 (last purchase 1 year ago)
- **F_Score:** 1 (only 1 purchase ever)
- **M_Score:** 1 (£20 spent)
- **RFM_Score:** 111
- **Segment:** Lost
- **Action:** Archive or occasional win-back attempt; focus budget elsewhere.

## Monitoring & Optimization

1. **Segment Size:** Monitor the distribution of customers across segments. Significant shifts may indicate business changes.
2. **Segment Transitions:** Track how customers move between segments over time. Upward movement is positive; downward movement requires attention.
3. **Revenue by Segment:** Calculate revenue contribution by segment to validate that Champions and Loyal Customers are indeed your most valuable.
4. **Campaign Performance:** Measure ROI of campaigns targeted at each segment to optimize strategy.
