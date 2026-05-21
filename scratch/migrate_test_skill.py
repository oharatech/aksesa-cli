import re
from pathlib import Path

path = Path("tests/core/test_skill.py")
content = path.read_text(encoding="utf-8")

# 1. Change KIMI_SHARE_DIR to AKSESA_SHARE_DIR
content = content.replace('KIMI_SHARE_DIR', 'AKSESA_SHARE_DIR')

# 2. Remove redundant test cases:
# - test_find_user_skills_dirs_brand_group_prefers_aksesa_over_kimi
# - test_find_project_skills_dirs_brand_prefers_aksesa
content = re.sub(
    r'@pytest\.mark\.asyncio\s+async def test_find_user_skills_dirs_brand_group_prefers_aksesa_over_kimi\(.*?\):.*?(?=\n\n@pytest|\n\ndef|\Z)',
    '',
    content,
    flags=re.DOTALL
)

content = re.sub(
    r'@pytest\.mark\.asyncio\s+async def test_find_project_skills_dirs_brand_prefers_aksesa\(.*?\):.*?(?=\n\n@pytest|\n\ndef|\Z)',
    '',
    content,
    flags=re.DOTALL
)

# 3. Perform other replacements
content = content.replace(".kimi", ".aksesa")
content = content.replace("kimi_dir", "aksesa_dir")
content = content.replace("kimi deploy", "aksesa deploy")
content = content.replace("kimi wins", "aksesa wins")
content = content.replace("kimi_idx", "aksesa_idx")
content = content.replace("kimi-idx", "aksesa-idx")

# Update test names and descriptions
content = content.replace("prefers_kimi_over_claude", "prefers_aksesa_over_claude")
content = content.replace("brand_prefers_kimi", "brand_prefers_aksesa_over_claude")
content = content.replace("prefers_kimi", "prefers_aksesa_over_claude")
content = content.replace("merge_brands_kimi_and_claude", "merge_brands_aksesa_and_claude")
content = content.replace("kimi_and_claude", "aksesa_and_claude")
content = content.replace("same_skill_kimi_wins", "same_skill_aksesa_wins")
content = content.replace("kimi first", "aksesa first")
content = content.replace("kimi before claude", "aksesa before claude")
content = content.replace("[kimi, claude, codex]", "[aksesa, claude, codex]")
content = content.replace("prefers kimi", "prefers aksesa")
content = content.replace("kimi", "aksesa")
content = content.replace("Kimi", "Aksesa")

path.write_text(content, encoding="utf-8")
print("Migration completed successfully!")
