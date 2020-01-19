How we address OWASP 9 based on [the top 10](https://owasp.org/www-project-top-ten/) document

### Injection
- All calls are going through SQL Alchemy, which handles injection attacks

### Broken Authentication
- JWT handles session

### Sensitive Data Exposure
- All user info behind tokenized decorator
- All sensitive data POSTED through JSON
- (when deployed) Pushed through to HTTPS (and port 443)

### XML External Entities (XXE)
- Not using XML, not concerned

### Broken Access Control
- ACL handled via JWT and token checker decorator
- All users have same level acces (not tiered)

### Security Misconfiguration
- SECRET KEY generated on server (passed in as ENV VAR)

### Cross-Site Scripting XSS

### Insecure Deserialization. 

### Using Components with Known Vulnerabilities
- Introduction of pyt and npm-audit

### Insufficient Logging & Monitoring
- Server-side logging to .log file ready for consumtion through logstash or file beat