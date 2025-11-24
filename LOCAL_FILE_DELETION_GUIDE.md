# Local File Deletion Guide - Post-WebRCA Storage

## 🗑️ Data Retention & Deletion Requirements

### **⚠️ IMPORTANT REQUIREMENT**
After incident summaries are successfully saved to the **WebRCA database**, all locally stored analysis files **MUST be deleted** from individual machines to comply with data retention policies.

---

## 📋 Files That Must Be Deleted

### **Generated Analysis Files**
- `analysis_[channel]_[timestamp].json` - Complete incident analysis results
- `usage_metrics.jsonl` - Usage tracking logs
- `slack_disclaimer_demo.json` - Demo files (if present)

### **Temporary Processing Files** 
- Any cached Slack message data
- Intermediate analysis outputs
- Downloaded incident logs or exports

### **Files to KEEP**
✅ Source code files (.py, .md) - These contain no incident data  
✅ Configuration files - These contain no sensitive information  
✅ Documentation files - These are reference materials only  

---

## 🔄 Deletion Process Workflow

### **Step 1: Verify WebRCA Storage** ✅
Before deleting any local files:

1. **Confirm WebRCA Upload**: Verify incident summary is properly stored in WebRCA database
2. **Check Data Integrity**: Ensure all analysis data transferred correctly  
3. **Validate Access**: Confirm team can access summary in WebRCA
4. **Record Upload**: Document successful storage with incident ID and timestamp

### **Step 2: Identify Local Files** 🔍
```bash
# Find all analysis files in current directory
find . -name "analysis_*.json" -type f

# Find usage metrics files
find . -name "usage_metrics.jsonl" -type f

# Find any incident-related temporary files
find . -name "*incident*" -type f | grep -v ".py\|.md"
```

### **Step 3: Secure Deletion** 🗑️
```bash
# Securely delete analysis files (recommended method)
rm -f analysis_*.json
rm -f usage_metrics.jsonl
rm -f *incident*temp*

# For enhanced security (macOS/Linux)
find . -name "analysis_*.json" -exec shred -vfz -n 3 {} +
find . -name "usage_metrics.jsonl" -exec shred -vfz -n 3 {} +
```

### **Step 4: Verify Deletion** ✅
```bash
# Confirm no analysis files remain
ls -la analysis_*.json 2>/dev/null || echo "✅ Analysis files deleted"
ls -la usage_metrics.jsonl 2>/dev/null || echo "✅ Metrics files deleted"

# Check for any remaining incident data
find . -name "*incident*" -type f | grep -v ".py\|.md" || echo "✅ No incident data files found"
```

---

## 🤖 Automated Deletion Scripts

### **Quick Cleanup Script**
```bash
#!/bin/bash
# File: cleanup_incident_files.sh

echo "🗑️ Starting Claude Incident Analyzer file cleanup..."

# Check for analysis files
ANALYSIS_FILES=$(find . -name "analysis_*.json" -type f)
METRICS_FILES=$(find . -name "usage_metrics.jsonl" -type f)

if [[ -n "$ANALYSIS_FILES" || -n "$METRICS_FILES" ]]; then
    echo "📁 Found local incident files to delete:"
    echo "$ANALYSIS_FILES"
    echo "$METRICS_FILES"
    
    read -p "⚠️  Are these files safely stored in WebRCA? (yes/no): " confirm
    
    if [[ $confirm == "yes" ]]; then
        echo "🗑️ Deleting analysis files..."
        rm -f analysis_*.json
        rm -f usage_metrics.jsonl
        echo "✅ Local incident files deleted successfully"
        
        # Log deletion for audit trail
        echo "$(date): Deleted incident analysis files after WebRCA storage" >> deletion_log.txt
    else
        echo "❌ Deletion cancelled - Please verify WebRCA storage first"
        exit 1
    fi
else
    echo "✅ No local incident files found to delete"
fi

echo "🎯 Cleanup complete"
```

### **Scheduled Cleanup (Optional)**
```bash
#!/bin/bash
# File: weekly_cleanup.sh
# Add to crontab: 0 2 * * 1 /path/to/weekly_cleanup.sh

echo "🕒 Weekly scheduled cleanup - $(date)"

# Delete files older than 7 days (assuming WebRCA storage within 7 days)
find . -name "analysis_*.json" -type f -mtime +7 -delete
find . -name "usage_metrics.jsonl" -type f -mtime +7 -delete

echo "✅ Weekly cleanup completed - $(date)" >> weekly_cleanup.log
```

---

## 📚 Integration with User Workflow

### **Updated Post-Incident Process**

#### **Standard Workflow** (With Deletion)
1. **Incident Occurs** → Claude Analyzer generates summary
2. **Review & Validate** → Human review of AI-generated content  
3. **WebRCA Storage** → Save validated summary to WebRCA database
4. **Verify Storage** → Confirm successful WebRCA upload
5. **🗑️ DELETE LOCAL FILES** → Remove incident data from local machine
6. **Document Deletion** → Log deletion for compliance audit

#### **Compliance Checklist**
- [ ] Incident summary reviewed and validated by human expert
- [ ] Summary successfully uploaded to WebRCA database  
- [ ] WebRCA storage verified and accessible by team
- [ ] Local analysis files identified (`analysis_*.json`)
- [ ] Local usage logs identified (`usage_metrics.jsonl`)
- [ ] **Local files securely deleted from machine**
- [ ] Deletion logged for audit trail
- [ ] Source code and documentation files preserved (contain no incident data)

---

## 🔒 Security & Compliance

### **Why Deletion is Required**
- **Data Minimization**: Reduce exposure of incident data on individual machines
- **Centralized Storage**: WebRCA becomes single source of truth
- **Access Control**: WebRCA provides proper access controls and audit trails
- **Retention Policy**: Align with organizational data retention requirements
- **Risk Reduction**: Minimize risk of incident data exposure on laptops

### **Audit Requirements**
- **Document Deletion**: Log when files were deleted and by whom
- **Verify WebRCA Storage**: Confirm data exists in authorized system
- **Regular Cleanup**: Implement periodic cleanup processes
- **Training Compliance**: Ensure all users understand deletion requirements

### **Exception Handling**
**If WebRCA Storage Fails**:
1. **Do NOT delete local files** until WebRCA issue resolved
2. **Escalate immediately** to incident management team
3. **Temporary retention** until proper storage confirmed
4. **Alternative storage** as directed by incident commander

---

## 📞 Support for Deletion Process

### **Questions & Issues**
- **Technical Problems**: vkumar@redhat.com
- **WebRCA Access Issues**: [WebRCA Support Team]
- **Policy Questions**: [Incident Management Team]
- **Compliance Concerns**: [Security/Compliance Team]

### **Emergency Situations**
If you need to delete files immediately (security incident):
```bash
# Emergency deletion (all analysis files)
rm -rf analysis_*.json usage_metrics.jsonl
shred -vfz -n 3 /tmp/*incident* 2>/dev/null
echo "$(date): EMERGENCY DELETION completed" >> emergency_deletion.log
```

---

## 🎯 User Training & Communication

### **Key Messages for Users**
1. **Local files are temporary** - WebRCA is the permanent storage
2. **Deletion is mandatory** - Required after WebRCA storage
3. **Verify before delete** - Always confirm WebRCA upload first  
4. **Log deletions** - Maintain audit trail for compliance
5. **Ask for help** - Contact support if uncertain about deletion

### **Common Mistakes to Avoid**
❌ Deleting files before WebRCA confirmation  
❌ Keeping analysis files indefinitely on local machines  
❌ Deleting source code or documentation files  
❌ Not documenting deletion for audit purposes  
❌ Ignoring deletion requirements  

---

## ✅ Quick Reference Checklist

### **Post-Incident File Management**
```
□ Incident analysis completed by Claude Analyzer
□ AI-generated summary reviewed and validated by human expert  
□ Validated summary uploaded to WebRCA database
□ WebRCA storage confirmed and accessible
□ Local analysis files identified: analysis_*.json
□ Local usage files identified: usage_metrics.jsonl  
□ Files securely deleted from local machine
□ Deletion logged with timestamp and incident ID
□ Cleanup verified - no incident data remains locally
□ WebRCA remains accessible for team reference
```

### **Emergency Deletion Checklist**  
```
□ Immediate security concern identified
□ Files deleted using secure deletion method
□ Emergency deletion logged with reason
□ Incident management team notified
□ WebRCA storage status verified separately
□ Security team informed of deletion action
```

---

**Document Owner**: Vikas Kumar (vkumar@redhat.com)  
**Compliance Requirement**: Data retention and deletion policy  
**Review Frequency**: Quarterly with incident management updates  
**Related Policies**: WebRCA data management, incident response procedures  

---

*This guide ensures proper data management and compliance with organizational retention policies while maintaining incident analysis capabilities.*