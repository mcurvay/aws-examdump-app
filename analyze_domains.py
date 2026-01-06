#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze questions and determine their AWS SAA-C03 exam domains
"""

import json
import re

# AWS SAA-C03 Exam Domains
DOMAINS = {
    'Design Secure Architectures': {
        'keywords': [
            'encrypt', 'encryption', 'security', 'secure', 'kms', 'iam', 'policy', 'access',
            'authentication', 'authorization', 'ssl', 'tls', 'certificate', 'vpc', 'security group',
            'nacl', 'waf', 'shield', 'guardduty', 'macie', 'inspector', 'secrets manager',
            'compliance', 'audit', 'cloudtrail', 'config', 'permission', 'role', 'principle',
            'private', 'public', 'subnet', 'endpoint', 'vpc endpoint', 'bastion', 'vpn',
            'direct connect', 'mfa', 'multi-factor', 'sso', 'identity', 'cognito'
        ],
        'short': 'Security'
    },
    'Design Resilient Architectures': {
        'keywords': [
            'availability', 'resilient', 'resilience', 'disaster', 'recovery', 'backup', 'restore',
            'multi-az', 'multi-region', 'replication', 'failover', 'high availability', 'durability',
            'snapshot', 'ami', 'auto scaling', 'load balancer', 'health check', 'target group',
            'route 53', 'dns', 'failover', 'active-passive', 'active-active', 'rto', 'rpo',
            's3 cross-region', 'aurora', 'rds', 'read replica', 'standby', 'backup', 'retention'
        ],
        'short': 'Resilience'
    },
    'Design High-Performing Architectures': {
        'keywords': [
            'performance', 'latency', 'throughput', 'speed', 'fast', 'optimize', 'cache',
            'cloudfront', 'cdn', 'edge', 'accelerate', 'transfer acceleration', 's3 transfer',
            'elasticache', 'dax', 'dynamodb', 'read replica', 'aurora', 'scaling', 'scale',
            'auto scaling', 'elastic', 'performance insights', 'monitoring', 'cloudwatch',
            'x-ray', 'optimize', 'bottleneck', 'throughput', 'iops', 'bandwidth', 'network'
        ],
        'short': 'Performance'
    },
    'Design Cost-Optimized Architectures': {
        'keywords': [
            'cost', 'price', 'cheap', 'economical', 'budget', 'save', 'optimize', 'optimization',
            'reserved', 'spot', 'savings plan', 'lifecycle', 'glacier', 'infrequent', 'archive',
            'intelligent tiering', 's3 standard-ia', 's3 one zone-ia', 's3 glacier', 's3 deep archive',
            'rightsizing', 'cost explorer', 'budgets', 'billing', 'pricing', 'economical',
            'cost-effective', 'most cost', 'least cost', 'minimize cost', 'reduce cost'
        ],
        'short': 'Cost'
    },
    'Operational Excellence': {
        'keywords': [
            'monitor', 'monitoring', 'logging', 'log', 'cloudwatch', 'cloudtrail', 'x-ray',
            'config', 'systems manager', 'ssm', 'parameter store', 'opsworks', 'codedeploy',
            'codebuild', 'codepipeline', 'automation', 'automate', 'cicd', 'ci/cd', 'deployment',
            'infrastructure as code', 'cloudformation', 'terraform', 'cdk', 'tag', 'tagging',
            'compliance', 'audit', 'governance', 'organizations', 'service catalog', 'maintenance',
            'patch', 'update', 'version', 'rollback', 'blue-green', 'canary'
        ],
        'short': 'Operations'
    }
}

def detect_domain(question_text, options_text, solution_text):
    """Detect the domain for a question based on keywords"""
    # Combine all text
    full_text = f"{question_text} {options_text} {solution_text}".lower()
    
    domain_scores = {}
    
    for domain_name, domain_info in DOMAINS.items():
        score = 0
        keywords = domain_info['keywords']
        
        for keyword in keywords:
            # Count occurrences
            count = len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', full_text))
            score += count
        
        domain_scores[domain_name] = score
    
    # Get domain with highest score
    if domain_scores:
        max_score = max(domain_scores.values())
        if max_score > 0:
            # Get all domains with max score
            top_domains = [d for d, s in domain_scores.items() if s == max_score]
            # Return the first one (or could return all if tie)
            return top_domains[0]
    
    # Default if no match
    return 'Design Secure Architectures'

def analyze_questions():
    """Analyze questions and add domain information"""
    input_file = 'questions.json'
    output_file = 'questions.json'
    
    print(f"Reading questions from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f"Found {len(questions)} questions")
    print("\nAnalyzing domains...")
    
    domain_counts = {}
    
    for i, q in enumerate(questions):
        # Combine options text
        options_text = ' '.join(q.get('options', {}).values())
        solution_text = q.get('solution', '')
        question_text = q.get('question', '')
        
        # Detect domain
        domain = detect_domain(question_text, options_text, solution_text)
        q['domain'] = domain
        q['domain_short'] = DOMAINS[domain]['short']
        
        # Count domains
        domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        if (i + 1) % 10 == 0:
            print(f"  Processed {i + 1}/{len(questions)} questions...")
    
    # Save updated questions
    print(f"\nSaving updated questions to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Domain analysis complete!")
    print(f"\nDomain distribution:")
    for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(questions)) * 100
        print(f"  {domain}: {count} questions ({percentage:.1f}%)")
    
    # Show sample
    if questions:
        print(f"\nSample questions with domains:")
        for q in questions[:5]:
            print(f"  Question #{q['id']}: {q['domain_short']} - {q['domain']}")

if __name__ == '__main__':
    analyze_questions()

