# Custom Test Suite - Quick Start

## 🎯 Goal
Create a test suite based on real customer questions from your store to ensure your AI agent handles actual use cases effectively.

## 📋 Process Overview

```
Discovery → Data Collection → Test Creation → Validation → Maintenance
   (1-2 hrs)    (1-3 days)      (2-4 hrs)     (1 hr)      (ongoing)
```

## 🚀 Quick Start (Minimum Viable Test Suite)

### Step 1: 30-Minute Store Owner Interview

Ask these 3 critical questions:

1. **"What are the top 10 questions customers ask most often?"**
2. **"What questions does your current system handle poorly?"**
3. **"What questions lead to the most sales?"**

### Step 2: Create Your First 10 Tests (1 hour)

Use the template file: `store_specific_tests_TEMPLATE.yml`

Replace the placeholders with actual questions:

```yaml
top_question_1:
  steps:
  - "Do you have the Luffy starter deck in stock?"  # Real question
  expected_results:
  - "Agent searches for Luffy starter deck"
  - "Agent provides availability status"
  - "Agent offers alternatives if out of stock"
```

### Step 3: Run Your Tests (5 minutes)

```bash
cd shopify-agent-evaluation
python -m agenteval.cli run --config store_specific_tests.yml
```

### Step 4: Review Results (30 minutes)

- ✅ **Passed tests**: Agent is handling these well
- ❌ **Failed tests**: Need to improve agent training or tools
- ⚠️ **Partial passes**: Work but could be better

## 📚 Complete Resources

### For Discovery Meeting:
- **`STORE_DISCOVERY_WORKSHEET.md`** - Comprehensive worksheet for store owner meeting
- Print this and bring it to your meeting

### For Test Creation:
- **`CREATING_CUSTOM_TEST_SUITE.md`** - Complete step-by-step guide
- **`store_specific_tests_TEMPLATE.yml`** - Ready-to-use test template

### For Running Tests:
- **`QUICK_START_GUIDE.md`** - How to run tests and interpret results

## 🎓 Recommended Approach

### Week 1: Foundation
- **Day 1**: Meet with store owner (use worksheet)
- **Day 2-3**: Collect data from chat logs, support tickets
- **Day 4**: Create initial 10-test suite
- **Day 5**: Run tests and review results

### Week 2: Expansion
- **Day 1**: Review results with store owner
- **Day 2-3**: Expand to 20-30 tests
- **Day 4**: Run comprehensive suite
- **Day 5**: Document findings and improvements

### Ongoing: Maintenance
- **Weekly**: Run high-priority tests
- **Monthly**: Add new tests based on recent questions
- **Quarterly**: Full review with store owner

## 💡 Pro Tips

### 1. Start Small
Don't try to create 100 tests immediately. Start with 10 high-impact tests.

### 2. Use Real Questions
Copy actual customer questions word-for-word. Don't paraphrase or "clean them up."

### 3. Prioritize by Impact
Focus on questions that:
- Are asked frequently (>10 times/month)
- Directly impact sales
- Currently handled poorly

### 4. Include Multi-Turn Scenarios
Real conversations aren't single questions. Include 2-3 multi-turn scenarios.

### 5. Test Edge Cases
Include 1-2 unusual or difficult questions to test agent's limits.

## 📊 Success Metrics

Track these to measure effectiveness:

- **Coverage**: % of actual customer questions covered by tests
- **Pass Rate**: % of tests passing (aim for >80%)
- **Business Impact**: Correlation with sales/satisfaction
- **Time Saved**: Reduction in support tickets

## 🔄 Iteration Cycle

```
Run Tests → Identify Failures → Improve Agent → Re-test → Repeat
  (5 min)      (30 min)          (varies)      (5 min)
```

## 📞 Getting Help

If you need assistance:

1. **Review the comprehensive guide**: `CREATING_CUSTOM_TEST_SUITE.md`
2. **Check example tests**: `comprehensive_tests.yml`
3. **Test your setup**: `python simple_final_test.py`

## 🎯 Example: One Piece Card Store

Here's a real example of converting store questions to tests:

**Real Customer Question:**
> "I'm new to One Piece TCG. Which starter deck should I buy?"

**Test Scenario:**
```yaml
beginner_deck_recommendation:
  steps:
  - "I'm new to One Piece TCG. Which starter deck should I buy?"
  - "What's the easiest deck to learn?"
  expected_results:
  - "Agent identifies customer is a beginner"
  - "Agent recommends beginner-friendly starter decks"
  - "Agent explains why these decks are good for learning"
  - "Agent offers to show specific deck details"
  max_turns: 4
  priority: high
  category: one_piece_cards
```

## ✅ Checklist

Before your store owner meeting:
- [ ] Print `STORE_DISCOVERY_WORKSHEET.md`
- [ ] Review current chat logs (if available)
- [ ] Prepare questions about common customer issues
- [ ] Schedule 1-2 hour meeting

After your meeting:
- [ ] Transfer top 10 questions to `store_specific_tests.yml`
- [ ] Define expected results for each test
- [ ] Run initial test suite
- [ ] Schedule results review meeting

## 🚀 Ready to Start?

1. **Print the worksheet**: `STORE_DISCOVERY_WORKSHEET.md`
2. **Schedule meeting** with store owner
3. **Bring this guide** to reference during meeting
4. **Start with 10 tests** - you can always add more later!

Your custom test suite will ensure your AI agent handles real customer needs effectively! 🎉