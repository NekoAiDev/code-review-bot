#!/usr/bin/env python3
"""
代码审核机器人 - 主入口
对提交的代码进行安全、合规、Bug 检测，生成审核报告
"""

import os
import sys
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

def get_event_payload():
    """读取 GitHub Actions 事件 payload"""
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        return None
    with open(event_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_issue_content():
    """获取 Issue 中的代码内容"""
    payload = get_event_payload()
    if not payload:
        return None, None
    
    # 从 Issue 正文获取内容
    if "issue" in payload:
        title = payload["issue"].get("title", "")
        body = payload["issue"].get("body", "")
        return title, body
    return None, None

def extract_code_from_markdown(text):
    """从 Markdown 中提取代码块"""
    import re
    code_blocks = re.findall(r"```(\w*)\n(.*?)```", text, re.DOTALL)
    return code_blocks

def run_security_check(code_path):
    """运行安全检查（bandit）"""
    try:
        result = subprocess.run(
            ["bandit", "-f", "json", "-r", code_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.stdout:
            return json.loads(result.stdout)
        return {"results": []}
    except Exception as e:
        return {"error": str(e), "results": []}

def run_compliance_check(code_path):
    """运行合规检查（ruff）"""
    try:
        result = subprocess.run(
            ["ruff", "check", "--format=json", code_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.stdout.strip():
            return json.loads(result.stdout)
        return []
    except Exception as e:
        return [{"error": str(e)}]

def run_bug_detection(code_path):
    """运行 Bug 检测（pylint）"""
    try:
        result = subprocess.run(
            ["pylint", "--output-format=json", code_path],
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.stdout.strip():
            return json.loads(result.stdout)
        return []
    except Exception as e:
        return [{"error": str(e)}]

def check_malicious_patterns(code_content):
    """检查恶意代码模式"""
    dangerous_patterns = [
        (r"os\.system\s*\(", "危险函数: os.system"),
        (r"subprocess\.run\s*\(", "危险函数: subprocess.run"),
        (r"subprocess\.Popen\s*\(", "危险函数: subprocess.Popen"),
        (r"eval\s*\(", "危险函数: eval"),
        (r"exec\s*\(", "危险函数: exec"),
        (r"__import__\s*\(", "危险函数: __import__"),
        (r"getattr\s*\(\s*.*\s*,\s*['\"]__", "危险操作: 动态属性访问"),
        (r"open\s*\(\s*['\"]/[^'\"]*['\"]", "危险操作: 直接文件操作"),
        (r"requests\.get\s*\(\s*['\"]http", "网络请求: requests.get"),
        (r"socket\.", "网络操作: socket"),
    ]
    
    import re
    findings = []
    for pattern, desc in dangerous_patterns:
        if re.search(pattern, code_content, re.MULTILINE):
            findings.append(desc)
    return findings

def generate_report(security_results, compliance_results, bug_results, malicious_findings):
    """生成审核报告"""
    report = []
    report.append("## 🔍 代码审核报告")
    report.append("")
    report.append(f"**审核时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**审核机器人**: Code Review Bot v1.0.0")
    report.append("")
    
    # 恶意代码检查
    report.append("### 🔒 安全检查")
    if malicious_findings:
        report.append("**⚠️ 发现潜在危险操作:**")
        for finding in malicious_findings:
            report.append(f"- ❌ {finding}")
    else:
        report.append("✅ 未发现明显的恶意代码模式")
    report.append("")
    
    # 安全扫描结果（bandit）
    if security_results and "results" in security_results:
        if security_results["results"]:
            report.append("**Bandit 安全扫描:**")
            for issue in security_results["results"][:5]:  # 最多显示5个
                report.append(f"- ⚠️ {issue.get('issue_text', 'Unknown')} (行 {issue.get('line_number', '?')})")
        else:
            report.append("✅ Bandit 安全扫描通过")
    report.append("")
    
    # 合规检查
    report.append("### 📋 合规检查")
    if compliance_results:
        report.append("**Ruff 代码风格检查:**")
        errors = [r for r in compliance_results if r.get("type") == "E"]
        warnings = [r for r in compliance_results if r.get("type") == "W"]
        
        if errors:
            report.append(f"- ❌ {len(errors)} 个错误")
            for err in errors[:3]:
                report.append(f"  - 行 {err.get('location', {}).get('row', '?')}: {err.get('message', '')}")
        if warnings:
            report.append(f"- ⚠️ {len(warnings)} 个警告")
        if not errors and not warnings:
            report.append("✅ 代码风格检查通过")
    else:
        report.append("✅ 代码风格检查通过")
    report.append("")
    
    # Bug 检测
    report.append("### 🐛 Bug 检测")
    if bug_results:
        errors = [r for r in bug_results if r.get("type") == "error"]
        warnings = [r for r in bug_results if r.get("type") == "warning"]
        
        if errors:
            report.append(f"**❌ {len(errors)} 个错误:**")
            for err in errors[:5]:
                report.append(f"- {err.get('message', '')} (行 {err.get('line', '?')})")
        if warnings:
            report.append(f"**⚠️ {len(warnings)} 个警告:**")
            for warn in warnings[:3]:
                report.append(f"- {warn.get('message', '')} (行 {warn.get('line', '?')})")
        if not errors and not warnings:
            report.append("✅ 未发现明显 Bug")
    else:
        report.append("✅ 未发现明显 Bug")
    report.append("")
    
    # 总结
    report.append("### 📝 审核总结")
    total_issues = len(malicious_findings) + len(security_results.get("results", [])) + len(compliance_results) + len([r for r in bug_results if r.get("type") == "error"])
    
    if total_issues == 0:
        report.append("✅ **审核通过** - 代码质量良好，未发现明显问题。")
    elif total_issues < 5:
        report.append("⚠️ **审核通过（有警告）** - 发现少量问题，建议修复后合并。")
    else:
        report.append("❌ **审核未通过** - 发现较多问题，请修复后重新提交。")
    
    report.append("")
    report.append("---")
    report.append("*此报告由 Code Review Bot 自动生成*")
    
    return "\n".join(report)

def main():
    """主函数"""
    # 获取 Issue 内容
    title, body = get_issue_content()
    
    if not body:
        print("未找到代码内容")
        sys.exit(1)
    
    # 提取代码
    code_blocks = extract_code_from_markdown(body)
    
    if not code_blocks:
        print("未在 Issue 中找到代码块")
        sys.exit(1)
    
    # 创建临时目录存放代码
    with tempfile.TemporaryDirectory() as tmpdir:
        for i, (lang, code) in enumerate(code_blocks):
            ext = {"python": ".py", "javascript": ".js", "java": ".java"}.get(lang.lower(), ".txt")
            code_file = Path(tmpdir) / f"code_{i}{ext}"
            code_file.write_text(code, encoding="utf-8")
            
            # 运行检查
            security_results = run_security_check(str(code_file))
            compliance_results = run_compliance_check(str(code_file))
            bug_results = run_bug_detection(str(code_file))
            malicious_findings = check_malicious_patterns(code)
            
            # 生成报告
            report = generate_report(security_results, compliance_results, bug_results, malicious_findings)
            
            # 保存报告
            report_file = Path("review_report.md")
            report_file.write_text(report, encoding="utf-8")
            print(f"审核报告已生成: {report_file}")
            break  # 只处理第一个代码块

if __name__ == "__main__":
    main()
