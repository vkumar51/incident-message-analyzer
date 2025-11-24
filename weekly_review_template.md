# Weekly Review Template - Claude Incident Analyzer

**Week of**: [DATE]  
**Reviewed by**: [NAME]  
**Review Date**: [DATE]

---

## 📈 Quick Usage Check (2 minutes)

**Total Analyses This Week**: ___  
**Success Rate**: ___%  
**Error Count**: ___

*Command to check*: 
```bash
# Count successful analyses
grep '"success": true' usage_metrics.jsonl | grep "$(date -v-7d +%Y-%m-)" | wc -l

# Count total analyses  
grep "$(date -v-7d +%Y-%m-)" usage_metrics.jsonl | wc -l
```

---

## ⭐ User Feedback Review (3 minutes)

**New Google Form Responses**: ___  
**Average Rating**: ___/5  
**Feedback Response Rate**: ___%

### Key Feedback Points:
**Positive**:
- 
- 

**Concerns/Issues**:
- 
- 

**Feature Requests**:
- 
- 

---

## 🚨 Issues & Alerts

### Critical Issues (Need immediate action):
- [ ] None
- [ ] Issue: ________________

### Minor Issues (Monitor next week):
- [ ] None  
- [ ] Issue: ________________

### Performance Check:
- [ ] ✅ Average rating ≥ 4.0/5.0
- [ ] ✅ Error rate ≤ 5%
- [ ] ✅ No user complaints about accuracy
- [ ] ⚠️  Something needs attention: ________________

---

## ✅ Actions Taken This Week

- 
- 

## 🎯 Focus for Next Week

- 
- 

---

## 📊 Trends (Optional - 1 minute)

**Usage Trend**: ⬆️ Increasing / ➡️ Stable / ⬇️ Decreasing  
**User Satisfaction Trend**: ⬆️ Improving / ➡️ Stable / ⬇️ Declining

---

**Total Review Time**: ~10 minutes  
**Next Review Due**: [DATE + 1 week]