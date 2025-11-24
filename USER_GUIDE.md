# Claude Incident Analyzer - User Guide

## 📚 Welcome to the Claude Incident Analyzer

**Version**: 2.0  
**Last Updated**: November 2024  
**Document Type**: Internal User Guide  

---

## 🤖 AI Functionality Notice

**⚠️ IMPORTANT**: This tool uses **Artificial Intelligence (AI)** functionality powered by Claude 3.5 Haiku via Google Vertex AI. All analysis, categorization, and summaries are generated using AI technology and require human review before use.

---

## 📞 Support & Contact Information

### **Primary Contact**
**Name**: Vikas Kumar  
**Role**: AI Tools Administrator & Technical Lead  
**Email**: vkumar@redhat.com  
**Response Time**: 24-48 hours for support requests  

### **Support Channels**
- **Questions & Support**: Email vkumar@redhat.com
- **Feedback**: [Google Feedback Form](https://docs.google.com/forms/d/e/1FAIpQLScs50MAteC0TZ2YefvXJHtKw1PZUeqSRy3PDpuiGXk6FIMnqw/viewform)
- **Technical Issues**: Create GitHub issue at [incident-message-analyzer](https://github.com/vkumar51/incident-message-analyzer)

---

## 🎯 Tool Purpose & Scope

### **Primary Purpose**
The Claude Incident Analyzer is designed **specifically** to:
- **Analyze incident communication** in Slack channels
- **Categorize incident messages** (diagnostics, actions, impact, resolution)
- **Generate executive summaries** of incident response activities
- **Extract action items** from incident discussions
- **Provide timeline analysis** of incident events

### **Approved Use Cases**
✅ **Incident response analysis**  
✅ **Post-incident review preparation**  
✅ **Communication pattern analysis**  
✅ **Executive incident reporting**  
✅ **Action item extraction**  

### **Prohibited Uses**
❌ **Personal communication analysis**  
❌ **Performance evaluation of individuals**  
❌ **Legal or compliance decision making**  
❌ **Financial or business-critical decisions**  
❌ **Any purpose other than incident analysis**  

---

## 🚨 Critical Disclaimer

### **⚠️ AI-Generated Content Warning**

> **All results from the Claude Incident Analyzer should NOT be relied upon without human review.**

**Key Limitations**:
- AI may **miss critical information**
- AI may **misinterpret context** or severity
- AI may **incorrectly categorize** messages
- AI may **generate inaccurate summaries**
- AI may **overlook technical nuances**

**Required Actions**:
1. ✅ **Always review** AI-generated content before use
2. ✅ **Verify accuracy** against actual incident data
3. ✅ **Cross-check** with subject matter experts
4. ✅ **Validate** action items and recommendations

---

## 📋 How to Use the Tool

### **Step 1: Setup & Access**
1. Ensure you have access to the monitored Slack channels
2. Verify the Claude Incident Analyzer bot is present in your channel
3. Start or participate in incident communication

### **Step 2: Trigger Analysis**
The analysis automatically triggers when:
- **20+ messages** have been posted, OR
- **30 minutes** have passed since last analysis

### **Step 3: Review AI Output**
When the bot posts a summary:
1. **Read the disclaimer** at the top of every summary
2. **Review categorization** of significant messages
3. **Validate executive summary** accuracy
4. **Check action items** for completeness and accuracy
5. **Verify timeline** matches actual events

### **Step 4: Human Validation**
- Compare AI analysis with your understanding of the incident
- Consult with incident commander or technical lead
- Validate technical details with subject matter experts
- Correct any inaccuracies before sharing with stakeholders

---

## 🛠️ Best Practices for Compliant Usage

### **Before Using AI Output**

#### ✅ **Do**
- **Read the full disclaimer** on every summary
- **Cross-reference** with actual incident logs
- **Validate technical details** with engineering teams  
- **Review with incident commander** before sharing
- **Use as a starting point**, not final document
- **Provide feedback** on accuracy via the feedback form

#### ❌ **Don't**
- **Use without review** by human experts
- **Share directly** with customers or executives without validation
- **Make critical decisions** based solely on AI output
- **Assume completeness** of the analysis
- **Use for purposes** other than incident analysis

### **Accuracy Validation Process**

1. **Technical Review**: Have an engineer verify technical categorizations
2. **Timeline Validation**: Cross-check with monitoring logs and timestamps
3. **Impact Assessment**: Confirm customer impact statements with support teams
4. **Action Items**: Validate recommendations with incident response team
5. **Executive Summary**: Review with incident commander before stakeholder communication

### **How to Override Inaccurate AI Content**

#### **When AI Categorization is Wrong**
1. **Identify the error**: Note which messages were incorrectly categorized
2. **Manual correction**: Recategorize based on actual incident flow
3. **Document the issue**: Use feedback form to report categorization errors
4. **Share corrected version**: Distribute human-reviewed summary

#### **When AI Summary is Inaccurate**
1. **Review original messages**: Go back to source Slack conversation
2. **Rewrite summary sections**: Correct any misinterpretations or omissions
3. **Validate with team**: Confirm accuracy with incident participants
4. **Note corrections**: Document what AI missed or got wrong
5. **Submit feedback**: Help improve future AI performance

#### **When Action Items are Incomplete**
1. **Compare with incident notes**: Check against manual action item tracking
2. **Add missing items**: Include overlooked or implied actions
3. **Correct priorities**: Adjust urgency levels based on actual impact
4. **Verify ownership**: Confirm action item assignments with team members

---

## 🎯 Quality Assurance Guidelines

### **Minimum Review Standards**
Before using any AI-generated content:

| **Component** | **Required Validation** | **Reviewer** |
|---|---|---|
| Message Categorization | Technical accuracy check | Engineering Team |
| Timeline Analysis | Cross-reference with logs | Incident Commander |
| Impact Assessment | Validate with monitoring data | SRE/Support Team |
| Action Items | Confirm with incident participants | All Stakeholders |
| Executive Summary | Overall accuracy and completeness | Incident Commander |

### **Red Flags - Immediate Human Review Required**
- 🚨 **Security incident details**
- 🚨 **Customer data mentions**  
- 🚨 **High severity impact statements**
- 🚨 **Root cause analysis**
- 🚨 **Regulatory compliance issues**

---

## 📊 Feedback & Continuous Improvement

### **How to Provide Feedback**

#### **Feedback Form** (Recommended)
- **URL**: [Google Feedback Form](https://docs.google.com/forms/d/e/1FAIpQLScs50MAteC0TZ2YefvXJHtKw1PZUeqSRy3PDpuiGXk6FIMnqw/viewform)
- **Purpose**: Rate accuracy, usefulness, and suggest improvements
- **Response Time**: Reviewed weekly by AI team

#### **Direct Contact**
- **Email**: vkumar@redhat.com
- **Subject**: "Claude Incident Analyzer Feedback"
- **Include**: Incident ID, specific issues, suggestions for improvement

### **What Feedback Helps Us Improve**
- **Accuracy issues**: When AI missed or misinterpreted information
- **Missing categories**: Types of messages AI doesn't handle well
- **Usability problems**: Interface or workflow issues
- **Feature requests**: Additional analysis capabilities needed

---

## 🔒 Privacy & Security Considerations

### **Data Handling**
- **Input**: Slack messages are processed temporarily by Claude AI
- **Output**: Analysis results saved locally as JSON files
- **Storage**: No permanent storage of message content in external systems
- **Access**: Only authorized team members can view analysis results

### **Compliance Notes**
- **Data Residency**: Processing occurs within approved cloud regions
- **Retention**: Analysis files retained according to incident retention policies
- **Access Control**: Limited to incident response team members
- **Audit Trail**: All analyses are logged with timestamps and user information

---

## 🆘 Troubleshooting & Common Issues

### **Analysis Not Triggering**
- **Check**: Are there 20+ messages or has 30+ minutes passed?
- **Verify**: Is the bot present in the channel?
- **Confirm**: Are messages during business hours (bot may have downtime)?

### **Poor Analysis Quality**
- **Review**: Was the incident discussion clear and structured?
- **Consider**: Complex technical discussions may be harder for AI to categorize
- **Action**: Provide detailed feedback about specific inaccuracies

### **Missing Action Items**
- **Common Cause**: Action items mentioned implicitly rather than explicitly
- **Solution**: Manually extract and add missing items
- **Prevention**: Use clear action item language in incident channels

---

## 📈 Success Metrics

### **How We Measure Tool Effectiveness**
- **Accuracy Rate**: % of AI categorizations validated as correct
- **Time Savings**: Reduced time for post-incident summary creation
- **User Satisfaction**: Feedback scores from users
- **Error Reduction**: Fewer missed action items in incident follow-ups

### **Your Role in Success**
- **Provide honest feedback** about accuracy and usefulness
- **Report issues** promptly via feedback channels
- **Follow review guidelines** to ensure compliance
- **Suggest improvements** based on your incident response experience

---

## 📞 Emergency Support

### **Critical Issues**
If you encounter:
- **Incorrect security-related analysis**
- **Potential data exposure concerns**
- **Service disruption due to the bot**

**Immediate Contact**: vkumar@redhat.com  
**Subject**: "URGENT - Claude Incident Analyzer Issue"  
**Expected Response**: Within 4 hours during business hours

---

## 🗑️ Required File Deletion After WebRCA Storage

### **⚠️ MANDATORY DATA CLEANUP**
After incident summaries are successfully saved to the **WebRCA database**, all locally stored analysis files **MUST be deleted** from your machine to comply with data retention policies.

### **Specific Files to Delete**
**Analysis Result Files** (Contains incident data):
```
analysis_[channel-name]_[timestamp].json
usage_metrics.jsonl
incident_analysis.json  
incident_comprehensive_summary.json
```

### **Deletion Process**
1. **Verify WebRCA Storage**: Confirm summary is properly stored in WebRCA
2. **Identify Local Files**: Run `ls -la analysis_*.json usage_metrics.jsonl`
3. **Delete Files**: Run `rm -f analysis_*.json usage_metrics.jsonl`
4. **Document Deletion**: Log deletion with incident ID and timestamp

### **Quick Deletion Script**
```bash
# After confirming WebRCA storage
rm -f analysis_*.json usage_metrics.jsonl incident*.json
echo "$(date): Files deleted after WebRCA storage" >> deletion_log.txt
```

### **Files to KEEP** (No incident data)
✅ All `.py` files (source code)  
✅ All `.md` files (documentation)  
✅ `requirements.txt` and configuration files  

**See**: `SPECIFIC_FILES_TO_DELETE.md` for complete deletion guide

---

## 📚 Additional Resources

### **Training Materials**
- **Video Tutorial**: [Coming Soon]
- **Best Practices Guide**: This document
- **File Deletion Guide**: `SPECIFIC_FILES_TO_DELETE.md`
- **FAQ**: Available at [Internal Wiki Page]

### **Related Tools**
- **WebRCA**: Central incident storage system  
- **Incident Management**: PagerDuty integration documentation
- **Monitoring**: How to correlate with observability data  
- **Reporting**: Integration with incident metrics dashboards

---

## ✅ Compliance Checklist

Before using Claude Incident Analyzer output:

- [ ] ✅ **Read AI disclaimer** at top of summary
- [ ] ✅ **Validated technical accuracy** with engineering team  
- [ ] ✅ **Confirmed timeline** with incident logs
- [ ] ✅ **Reviewed action items** with all stakeholders
- [ ] ✅ **Cross-checked impact statements** with monitoring data
- [ ] ✅ **Obtained incident commander approval** before sharing
- [ ] ✅ **Documented any corrections** made to AI output
- [ ] ✅ **Submitted feedback** on analysis quality

---

**Document Owner**: Vikas Kumar (vkumar@redhat.com)  
**Review Cycle**: Quarterly  
**Next Review**: February 2025  
**Version History**: Available in Git repository

---

*This user guide ensures compliant and effective use of AI-powered incident analysis while maintaining human oversight and quality standards.*