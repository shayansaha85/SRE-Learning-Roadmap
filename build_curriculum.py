#!/usr/bin/env python3
"""
Master Curriculum Builder
Assembles all parts into SRE_Python_NewRelic_Roadmap.md and performs automated quality checks.
"""
import sys
import re
from pathlib import Path

from curriculum_builder.part1_foundations import get_part1_content
from curriculum_builder.part2_python import get_part2_content
from curriculum_builder.part3_cloud_k8s import get_part3_content
from curriculum_builder.part4_newrelic import get_part4_content
from curriculum_builder.part5_sre_practices import get_part5_content
from curriculum_builder.part6_projects_chaos import get_part6_content
from curriculum_builder.part7_interviews import get_part7_content
from curriculum_builder.part8_design_capstone import get_part8_content

def build():
    parts = [
        get_part1_content(),
        get_part2_content(),
        get_part3_content(),
        get_part4_content(),
        get_part5_content(),
        get_part6_content(),
        get_part7_content(),
        get_part8_content()
    ]
    
    full_document = "\n\n---\n\n".join(parts)
    
    output_path = Path("SRE_Python_NewRelic_Roadmap.md")
    output_path.write_text(full_document, encoding="utf-8")
    
    file_size_kb = output_path.stat().st_size / 1024
    lines = full_document.splitlines()
    words = len(full_document.split())
    
    print(f"Successfully generated {output_path}")
    print(f"File Size: {file_size_kb:.2f} KB ({file_size_kb/1024:.2f} MB)")
    print(f"Total Lines: {len(lines):,}")
    print(f"Total Words: {words:,}")
    
    # Verification of All 50 Sections
    missing_sections = []
    for sec_num in range(1, 51):
        pattern = rf"^# {sec_num}\.\s"
        if not any(re.match(pattern, line) for line in lines):
            missing_sections.append(sec_num)
            
    if missing_sections:
        print(f"WARNING: Missing section headers: {missing_sections}")
        sys.exit(1)
    else:
        print("VERIFICATION PASSED: All 50 Sections (1 to 50) are present and verified!")

if __name__ == "__main__":
    build()
