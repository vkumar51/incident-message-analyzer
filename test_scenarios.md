# Slack Bot Test Scenarios

Copy and paste these realistic incident scenarios into your test channel to see how the bot analyzes different types of incidents.

## 🔥 Scenario 1: Database Performance Issue

```
API latency spiking to 4+ seconds across all regions
```

```
Checking database performance metrics now
```

```
Database connection pool at 98% utilization - critical threshold
```

```
Query response times increased 10x from normal baseline
```

```
Customer reports: checkout process timing out frequently
```

```
Impact assessment: approximately 70% of transactions affected
```

```
Scaling database connection pool from 100 to 200 connections
```

```
Applied database performance tuning configuration
```

```
Connection pool scaling complete - utilization now at 60%
```

```
API response times dropping - now averaging 800ms
```

```
Customer timeout reports decreasing significantly
```

```
All metrics back to baseline - latency under 300ms
```

```
Incident resolved - will monitor for next 30 minutes
```

```
Post-mortem scheduled for tomorrow 2 PM to review scaling policies
```

```
Great job team on the quick response! 👍
```

---

## 🚨 Scenario 2: Authentication Service Outage

```
Authentication service returning 500 errors for all login attempts
```

```
Login success rate dropped from 99.8% to 0% in last 2 minutes
```

```
Users completely unable to access the platform
```

```
Error logs showing "connection refused" to auth database
```

```
This is affecting 100% of our user base - critical outage
```

```
Severity: Complete service unavailability
```

```
Found root cause: auth database primary node is down
```

```
Database failover to secondary node initiated
```

```
Auth service connecting to backup database instance
```

```
Restarting authentication service pods to clear connection cache
```

```
Login functionality restored - success rate back to 99.5%
```

```
Users can now access platform normally
```

```
Primary database node brought back online
```

```
Switched back to primary database - all systems normal
```

```
Incident officially resolved - full service restored
```

```
RCA document created: database monitoring gaps identified
```

---

## ⚡ Scenario 3: Payment Processing Degradation

```
Payment processing latency increased from 200ms to 2+ seconds
```

```
Transaction success rate dropped from 98% to 85%
```

```
Payment gateway reporting increased timeout errors
```

```
Customer complaints about failed credit card transactions
```

```
Revenue impact: $50K in failed transactions in last hour
```

```
Regional analysis: issue isolated to US East region only
```

```
Found correlation: started right after payment-service v3.2.1 deployment
```

```
Memory usage spiked to 95% on payment service instances
```

```
Rolling back payment-service to stable version v3.1.8
```

```
Deployment rollback initiated for payment microservice
```

```
Payment processing latency improving - down to 500ms
```

```
Transaction success rate recovering - now at 96%
```

```
Memory usage normalized to 45% after rollback
```

```
Revenue impact contained - no further transaction failures
```

```
All payment metrics back to normal baselines
```

```
Follow-up action: memory leak investigation for v3.2.1
```

---

## 🌐 Scenario 4: CDN and Static Asset Issues

```
Website loading extremely slowly - 10+ second page loads
```

```
CDN cache hit ratio dropped from 95% to 20%
```

```
Static assets (CSS, JS, images) failing to load
```

```
User experience severely degraded across all regions
```

```
CDN provider reporting infrastructure issues in primary data centers
```

```
Geographic impact: Global outage affecting all customers
```

```
Switching traffic to backup CDN provider immediately
```

```
DNS records updated to point to secondary CDN
```

```
Page load times improving - now averaging 3 seconds
```

```
Cache hit ratio recovering with new CDN - up to 85%
```

```
Static asset delivery fully restored
```

```
Website performance back to normal (<2 second loads)
```

```
Incident contained - primary CDN provider issue resolved
```

```
Traffic gradually switching back to primary CDN
```

```
All performance metrics within acceptable ranges
```

---

## 🔧 Scenario 5: Kubernetes Infrastructure Issue

```
Multiple pod restarts detected across production cluster
```

```
Node resource exhaustion: CPU at 100% on 3 worker nodes
```

```
Application pods being evicted due to memory pressure
```

```
Service availability degraded - intermittent connection failures
```

```
Kubernetes cluster showing signs of resource contention
```

```
Impact scope: 40% of application instances affected
```

```
Cordoning affected nodes to prevent new pod scheduling
```

```
Draining pods from overloaded nodes for redistribution
```

```
Scaling cluster by adding 2 additional worker nodes
```

```
New nodes online - redistributing workload across cluster
```

```
Resource utilization balanced - CPU now averaging 60%
```

```
All application pods running stable - no more restarts
```

```
Service availability fully restored
```

```
Cluster health monitoring shows all green metrics
```

```
Infrastructure incident resolved - capacity planning review needed
```

---

## 📝 **How to Use These Scenarios**

1. **Copy each message line** and paste into your test channel
2. **Wait a few seconds** between messages to simulate real timing
3. **Watch the bot** analyze patterns and categorize messages
4. **After 20+ messages**, the bot should post a comprehensive analysis

## 🎯 **What to Test**

- **Category Detection**: Does it properly identify Diagnostics, Actions, Impact, Resolution?
- **Timeline Tracking**: Does it show logical incident progression?
- **Root Cause Analysis**: Does the AI identify the actual problem?
- **Action Item Extraction**: Does it track what was done vs what needs follow-up?
- **Executive Summary**: Is the summary clear and actionable?

## 🔄 **Testing Tips**

- Use different scenarios to test various incident types
- Mix up the order occasionally to test robustness
- Add some "noise" messages (like "thanks!" or "any updates?") to test filtering
- Try partial scenarios to see how it handles incomplete incidents

Pick a scenario and start testing! Let me know how the bot performs.