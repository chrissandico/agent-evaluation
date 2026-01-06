# Creating a Custom Test Suite - Step-by-Step Guide

## Overview

This guide walks you through creating a custom test suite based on real customer questions and store-specific scenarios. This ensures your agent is tested against actual use cases rather than generic scenarios.

## Phase 1: Discovery & Data Collection

### Step 1: Meet with Store Owner

**Prepare for the Meeting:**

Create a discovery document to guide the conversation:

```markdown
# Store Discovery Questions

## Current Customer Interactions
1. What are the top 10 most common questions customers ask?
2. What questions do customers ask that are hardest to answer?
3. What questions lead to the most sales?
4. What questions indicate a customer is frustrated or confused?

## Existing Chatbot Data (if applicable)
1. Can we access chat logs from the current chatbot?
2. What are the most frequent conversation topics?
3. What questions does the current bot fail to answer well?
4. What percentage of chats end in escalation to human support?

## Store-Specific Scenarios
1. What are your unique selling points?
2. What products/categories get the most questions?
3. What are common objections or concerns?
4. What seasonal or promotional questions come up?

## Success Criteria
1. What would make this chatbot successful for your business?
2. What metrics matter most (sales, support reduction, satisfaction)?
3. What customer behaviors should the bot encourage?
```

### Step 2: Gather Data Sources

**Collect from Multiple Sources:**

1. **Chat Logs** (if existing chatbot):
   - Export conversation transcripts
   - Identify patterns and common questions
   - Note failed interactions

2. **Customer Support Tickets**:
   - Review email support requests
   - Identify recurring themes
   - Note complex scenarios

3. **Store Analytics**:
   - Most viewed products
   - Common search terms
   - Cart abandonment reasons

4. **Social Media/Reviews**:
   - Common questions in comments
   - Frequently mentioned concerns
   - Product-specific inquiries

### Step 3: Categorize Questions

**Organize collected questions into categories:**

```
Categories:
├── Product Information
│   ├── Availability
│   ├── Specifications
│   ├── Pricing
│   └── Comparisons
├── Orders & Shipping
│   ├── Order status
│   ├── Shipping times
│   ├── Tracking
│   └── Delivery issues
├── Returns & Exchanges
│   ├── Return policy
│   ├── Refund process
│   ├── Exchange options
│   └── Damaged items
├── Store Policies
│   ├── Payment methods
│   ├── Store hours
│   ├── Contact information
│   └── Warranties
└── Product-Specific (e.g., One Piece Cards)
    ├── Card availability
    ├── Deck building
    ├── Set information
    └── Competitive play
```

## Phase 2: Test Suite Design

### Step 4: Create Test Scenarios Template

For each question, create a test scenario with this structure:

```yaml
test_name:
  steps:
  - "Customer's actual question"
  - "Follow-up question (if multi-turn)"
  expected_results:
  - "What the agent should do/say"
  - "What information should be provided"
  - "What action should be offered"
  max_turns: 3  # Adjust based on complexity
  priority: high  # high, medium, low
  category: product_information
  notes: "Any special context or requirements"
```

### Step 5: Prioritize Test Scenarios

**Use this prioritization matrix:**

| Priority | Criteria | Example |
|----------|----------|---------|
| **High** | - Frequently asked (>10% of questions)<br>- Directly impacts sales<br>- Critical for customer satisfaction | "Do you have [popular product] in stock?"<br>"What's your return policy?" |
| **Medium** | - Moderately frequent (5-10%)<br>- Important but not critical<br>- Standard store operations | "What are your store hours?"<br>"Do you ship internationally?" |
| **Low** | - Rarely asked (<5%)<br>- Edge cases<br>- Nice-to-have functionality | "Can I get a custom engraving?"<br>"Do you offer gift wrapping?" |

## Phase 3: Implementation

### Step 6: Create Your Custom Test File

Create a new file: `shopify-agent-evaluation/store_specific_tests.yml`

```yaml
# Store-Specific Test Suite
# Based on actual customer questions from [Store Name]
# Created: [Date]
# Last Updated: [Date]

evaluator:
  model: claude-3

target:
  type: shopify_extensions.targets.shopify_agent_target.ShopifyAgentTarget
  base_url: https://localhost:3458
  shop_id: test-shop
  shop_domain: https://your-store.myshopify.com
  timeout: 30

tests:
  # HIGH PRIORITY TESTS
  # These represent the most common customer questions
  
  most_common_question_1:
    steps:
    - "[Actual customer question from data]"
    expected_results:
    - "[What agent should do]"
    - "[Information to provide]"
    priority: high
    category: product_information
    
  most_common_question_2:
    steps:
    - "[Actual customer question]"
    expected_results:
    - "[Expected behavior]"
    priority: high
    category: orders_shipping
  
  # MEDIUM PRIORITY TESTS
  
  # LOW PRIORITY TESTS
  
  # EDGE CASES
```

### Step 7: Example - Converting Real Questions to Tests

**Real Customer Question:**
> "I'm looking for the Luffy starter deck but I don't know which one to get. Can you help me choose?"

**Convert to Test:**

```yaml
luffy_starter_deck_recommendation:
  steps:
  - "I'm looking for the Luffy starter deck but I don't know which one to get"
  - "What's the difference between them?"
  expected_results:
  - "Agent identifies there are multiple Luffy starter decks"
  - "Agent explains the differences between available Luffy decks"
  - "Agent provides recommendations based on play style or budget"
  - "Agent offers to show specific deck details or pricing"
  max_turns: 4
  priority: high
  category: one_piece_cards
  notes: "Common question for new players. Should demonstrate product knowledge."
```

### Step 8: Create Category-Specific Test Files

Organize tests by category for better management:

```
shopify-agent-evaluation/
└── store_specific_tests/
    ├── high_priority_tests.yml          # Top 20 most common questions
    ├── product_questions.yml             # Product-specific inquiries
    ├── order_shipping_tests.yml          # Order and shipping scenarios
    ├── returns_exchanges_tests.yml       # Return/exchange scenarios
    ├── one_piece_specific_tests.yml      # Card game specific questions
    └── edge_cases_tests.yml              # Unusual or complex scenarios
```

## Phase 4: Test Creation Workshop

### Step 9: Conduct Test Creation Session

**Schedule a 2-hour workshop with store owner:**

**Hour 1: Question Review**
- Review top 20 most common questions
- Discuss ideal responses for each
- Identify multi-turn conversation flows
- Note any special handling requirements

**Hour 2: Test Creation**
- Convert questions to test scenarios together
- Define expected results for each test
- Prioritize tests
- Identify gaps in coverage

**Workshop Template:**

```markdown
# Test Creation Workshop Notes

## Date: [Date]
## Attendees: [Names]

## Top Questions Reviewed:
1. [Question] → Test: [test_name]
   - Expected behavior: [description]
   - Priority: [high/medium/low]
   - Notes: [any special requirements]

2. [Question] → Test: [test_name]
   ...

## Multi-Turn Scenarios Identified:
1. [Scenario description]
   - Turn 1: [customer says]
   - Turn 2: [agent should respond]
   - Turn 3: [customer follow-up]
   ...

## Special Requirements:
- [Any unique handling needed]
- [Product-specific knowledge required]
- [Integration requirements]

## Action Items:
- [ ] Create test file for high-priority questions
- [ ] Gather additional data for [category]
- [ ] Schedule follow-up review
```

## Phase 5: Validation & Iteration

### Step 10: Run Initial Tests

```bash
cd shopify-agent-evaluation

# Run your custom test suite
python -m agenteval.cli run --config store_specific_tests.yml

# Or run specific category
python -m agenteval.cli run --config store_specific_tests/high_priority_tests.yml
```

### Step 11: Review Results with Store Owner

**Create a results review document:**

```markdown
# Test Results Review

## Test Run Date: [Date]
## Tests Executed: [Number]
## Pass Rate: [Percentage]

## High Priority Tests:
| Test Name | Status | Notes |
|-----------|--------|-------|
| [test_1]  | ✅ Pass | Agent handled perfectly |
| [test_2]  | ❌ Fail | Needs improvement: [details] |
| [test_3]  | ⚠️ Partial | Works but could be better |

## Failed Tests - Action Required:
1. **[Test Name]**
   - Issue: [What went wrong]
   - Customer Impact: [How this affects customers]
   - Recommended Fix: [What to change]
   - Priority: [High/Medium/Low]

## Recommendations:
1. [Improvement suggestion]
2. [Training data needed]
3. [Feature request]
```

### Step 12: Iterate and Improve

**Continuous improvement cycle:**

1. **Weekly**: Run high-priority test suite
2. **Bi-weekly**: Review failed tests and update agent
3. **Monthly**: Add new tests based on recent customer questions
4. **Quarterly**: Full test suite review with store owner

## Phase 6: Maintenance

### Step 13: Keep Tests Updated

**Create a test maintenance schedule:**

```markdown
# Test Suite Maintenance Schedule

## Weekly Tasks:
- [ ] Run high-priority test suite
- [ ] Review any new customer questions
- [ ] Update tests if products/policies change

## Monthly Tasks:
- [ ] Analyze chat logs for new patterns
- [ ] Add tests for new products/categories
- [ ] Remove outdated tests
- [ ] Update expected results if needed

## Quarterly Tasks:
- [ ] Full test suite review with store owner
- [ ] Reprioritize tests based on frequency data
- [ ] Archive obsolete tests
- [ ] Plan new test scenarios
```

### Step 14: Document Test Rationale

For each test, document why it exists:

```yaml
test_name:
  steps:
  - "Customer question"
  expected_results:
  - "Expected behavior"
  metadata:
    created_date: "2025-01-15"
    created_by: "Store Owner"
    frequency: "Asked 50+ times per month"
    business_impact: "High - directly affects sales"
    last_updated: "2025-01-20"
    update_reason: "Product line expanded"
    related_products: ["Product A", "Product B"]
```

## Quick Start Template

### Minimal Viable Test Suite

Start with just 10 tests covering the absolute essentials:

```yaml
# Minimal Store-Specific Test Suite
# Start here and expand over time

tests:
  # Top 3 Product Questions
  top_product_question_1:
    steps: ["[Most asked product question]"]
    expected_results: ["[Expected response]"]
    
  top_product_question_2:
    steps: ["[Second most asked]"]
    expected_results: ["[Expected response]"]
    
  top_product_question_3:
    steps: ["[Third most asked]"]
    expected_results: ["[Expected response]"]
  
  # Top 3 Policy Questions
  return_policy_question:
    steps: ["What's your return policy?"]
    expected_results: ["[Store's return policy]"]
    
  shipping_question:
    steps: ["How long does shipping take?"]
    expected_results: ["[Shipping timeframes]"]
    
  payment_question:
    steps: ["What payment methods do you accept?"]
    expected_results: ["[Payment options]"]
  
  # Top 2 Order Questions
  order_status_question:
    steps: ["Where is my order?"]
    expected_results: ["[How to check order status]"]
    
  order_modification_question:
    steps: ["Can I change my order?"]
    expected_results: ["[Order modification policy]"]
  
  # Top 2 Product-Specific Questions
  product_specific_1:
    steps: ["[Store-specific product question]"]
    expected_results: ["[Expected response]"]
    
  product_specific_2:
    steps: ["[Another store-specific question]"]
    expected_results: ["[Expected response]"]
```

## Tools & Resources

### Data Collection Template

Use this spreadsheet structure to collect questions:

| Question | Frequency | Category | Priority | Current Answer | Ideal Answer | Multi-Turn? | Notes |
|----------|-----------|----------|----------|----------------|--------------|-------------|-------|
| [Q1] | 50/month | Product | High | [Current] | [Ideal] | No | [Notes] |
| [Q2] | 30/month | Shipping | High | [Current] | [Ideal] | Yes | [Notes] |

### Test Naming Convention

Use consistent naming for easy organization:

```
[category]_[topic]_[variant]

Examples:
- product_availability_check
- shipping_time_domestic
- return_policy_damaged_item
- onepiece_deck_recommendation_beginner
- order_status_tracking_number
```

## Success Metrics

Track these metrics to measure test suite effectiveness:

1. **Coverage**: % of actual customer questions covered by tests
2. **Pass Rate**: % of tests passing consistently
3. **Business Impact**: Correlation between test improvements and customer satisfaction
4. **Maintenance**: Time spent updating tests vs. value gained

## Next Steps

1. **Schedule discovery meeting** with store owner
2. **Collect data** from all available sources
3. **Create initial 10-test suite** using the minimal template
4. **Run tests** and review results
5. **Iterate** based on findings
6. **Expand** to comprehensive suite over time

Your custom test suite will be a living document that evolves with your store and customer needs! 🎯