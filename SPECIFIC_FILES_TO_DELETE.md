# Specific Files to Delete After WebRCA Storage

## 🎯 Exact Files Created by Claude Incident Analyzer

Based on the actual code analysis, here are the **specific files** that contain incident data and must be deleted after WebRCA storage:

---

## 📁 Files That MUST Be Deleted

### **1. Analysis Result Files** (Contains Incident Data)
These files are created each time the Slack bot analyzes an incident:

```
analysis_[channel-name]_[timestamp].json
```

**Examples**:
- `analysis_demo_test_20250908_075347.json`
- `analysis_demo_test_20250902_215626.json` 
- `analysis_demo_test_20250907_210038.json`

**Contains**: Complete incident analysis, message categorization, summaries, action items

### **2. Usage Metrics Log** (Contains Usage Data)
```
usage_metrics.jsonl
```
**Contains**: Timestamps, channel names, success/error logs, analysis metadata

### **3. Batch Analysis Files** (If Used)
```
incident_analysis.json
incident_comprehensive_summary.json
```
**Contains**: Batch-processed incident data and comprehensive summaries

### **4. Demo/Test Files** (If Present)
```
demo_incident_analysis.json
slack_disclaimer_demo.json
```
**Contains**: Test incident data (delete if contains real incident info)

---

## 🔍 How to Identify These Files

### **Find Analysis Files**
```bash
# List all analysis files in current directory
ls -la analysis_*.json

# Find with timestamps to see creation dates
find . -name "analysis_*.json" -exec ls -la {} \;
```

### **Find Usage Metrics**
```bash
# Check if usage metrics file exists
ls -la usage_metrics.jsonl

# See file size and last modified
stat usage_metrics.jsonl
```

### **Find Batch Analysis Files**
```bash
# Check for batch analysis outputs
ls -la incident_analysis.json incident_comprehensive_summary.json
```

---

## 🗑️ Specific Deletion Commands

### **Delete Analysis Files**
```bash
# Delete all analysis result files
rm -f analysis_*.json

# Secure deletion (recommended)
find . -name "analysis_*.json" -exec shred -vfz -n 3 {} +
```

### **Delete Usage Metrics**
```bash
# Delete usage tracking file
rm -f usage_metrics.jsonl

# Secure deletion
shred -vfz -n 3 usage_metrics.jsonl
```

### **Delete Batch Files** 
```bash
# Delete batch analysis files
rm -f incident_analysis.json incident_comprehensive_summary.json

# Secure deletion
shred -vfz -n 3 incident_analysis.json incident_comprehensive_summary.json
```

### **Complete Cleanup Script**
```bash
#!/bin/bash
# cleanup_incident_data.sh

echo "🗑️ Deleting Claude Incident Analyzer data files..."

# Confirm WebRCA storage first
read -p "⚠️  Confirm: Are all summaries safely stored in WebRCA? (yes/no): " confirm

if [[ $confirm != "yes" ]]; then
    echo "❌ Deletion cancelled - Verify WebRCA storage first"
    exit 1
fi

# Delete specific incident data files
echo "Deleting analysis files..."
rm -f analysis_*.json

echo "Deleting usage metrics..."  
rm -f usage_metrics.jsonl

echo "Deleting batch analysis files..."
rm -f incident_analysis.json incident_comprehensive_summary.json

echo "Deleting demo files..."
rm -f demo_incident_analysis.json slack_disclaimer_demo.json

# Verify deletion
echo "✅ Verification:"
ls -la analysis_*.json 2>/dev/null || echo "  ✓ Analysis files deleted"
ls -la usage_metrics.jsonl 2>/dev/null || echo "  ✓ Usage metrics deleted"  
ls -la incident_*.json 2>/dev/null || echo "  ✓ Batch files deleted"

echo "🎯 Incident data cleanup complete!"
echo "$(date): Incident data files deleted after WebRCA storage" >> deletion_log.txt
```

---

## 🔒 Files to KEEP (DO NOT Delete)

### **Source Code Files** (No Incident Data)
```
✅ slack_bot.py - Bot source code
✅ message_analyzer.py - Analysis logic  
✅ summary_generator.py - Summary generation
✅ batch_analyzer.py - Batch processing
✅ demo_disclaimer.py - Demo script
```

### **Documentation Files** (No Incident Data)
```
✅ README.md - Project documentation
✅ USER_GUIDE.md - User instructions
✅ MONITORING_FRAMEWORK.md - Monitoring docs
✅ requirements.txt - Dependencies
```

### **Configuration Files** (No Incident Data)
```
✅ .gitignore - Git configuration
✅ feedback_form.html - Form template
✅ weekly_review_template.md - Review template  
```

---

## 📋 File Identification Checklist

### **Before Deletion - Verify Files**
- [ ] List all `.json` files: `ls -la *.json`
- [ ] Check file contents to confirm incident data: `head -20 filename.json`
- [ ] Verify WebRCA storage of corresponding summaries
- [ ] Confirm files are not source code or documentation

### **Files Containing Incident Data** (DELETE)
- [ ] `analysis_[channel]_[timestamp].json` - Real incident analysis
- [ ] `usage_metrics.jsonl` - Usage logs with channel names
- [ ] `incident_analysis.json` - Batch analysis results
- [ ] `incident_comprehensive_summary.json` - Summary outputs

### **Files NOT Containing Incident Data** (KEEP)
- [ ] All `.py` files - Source code only
- [ ] All `.md` files - Documentation only  
- [ ] `requirements.txt` - Dependencies only
- [ ] `feedback_form.html` - Template only

---

## ⚠️ Important Notes

### **What Each File Contains**

**`analysis_[channel]_[timestamp].json`**:
- Slack message analysis results
- Incident categorization
- Executive summaries  
- Action items
- Channel and user information

**`usage_metrics.jsonl`**:
- Analysis timestamps
- Channel names
- Success/error status
- User activity logs

**`incident_analysis.json` / `incident_comprehensive_summary.json`**:
- Batch analysis results
- Complete incident summaries
- Historical incident data

### **Why These Files Must Be Deleted**
- Contain actual incident communication data
- Include sensitive technical information
- May contain customer impact details
- Store user and channel information
- Required for data minimization compliance

---

## 🚨 Emergency Deletion

If immediate deletion is required (security incident):

```bash
# Emergency cleanup - deletes ALL incident data files
rm -f analysis_*.json usage_metrics.jsonl incident*.json demo*.json
echo "$(date): EMERGENCY DELETION - All incident data files removed" >> emergency_deletion.log
```

---

**Summary**: The Claude Incident Analyzer creates specific JSON files containing incident data that must be deleted after WebRCA storage. The main files are `analysis_*.json` (analysis results) and `usage_metrics.jsonl` (usage logs). All source code and documentation files should be preserved as they contain no incident data.