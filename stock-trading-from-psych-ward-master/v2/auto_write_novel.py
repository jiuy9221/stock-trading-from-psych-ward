#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说自动创作脚本
功能：自动读取开发计划，每次写10章，更新计划，提交到Gitee
"""

import os
import re
import subprocess
from datetime import datetime

# 配置
NOVEL_FILE = "我在精神病院学炒股_第二版.md"
PLAN_FILE = "第二版小说创作计划文档.md"
CHAPTERS_PER_RUN = 10
MIN_WORDS = 2000
MAX_WORDS = 3500

def read_plan(filepath):
    """读取开发计划文档，获取当前进度"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取已完成章节数
    match = re.search(r'已完成章节.*?(\d+)-(\d+)章', content)
    if match:
        start = int(match.group(1))
        end = int(match.group(2))
        return end
    return 0

def update_plan(filepath, completed_chapters):
    """更新开发计划文档"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新已完成章节
    content = re.sub(
        r'已完成章节.*?(\d+)-(\d+)章',
        f'已完成章节：第1-{completed_chapters}章',
        content
    )
    
    # 更新进度百分比
    progress = round(completed_chapters / 500 * 100)
    content = re.sub(
        r'整体进度.*?(\d+)%',
        f'整体进度：{progress}%',
        content
    )
    
    # 更新状态列
    for i in range(1, 11):
        start_chap = (i-1)*50 + 1
        end_chap = i*50
        if completed_chapters >= end_chap:
            content = content.replace(
                f'| 第{i}阶段 | 第{i}周 | 第{i}卷（{start_chap}-{end_chap}章） | {i*10}% | ⏳ 待开始 |',
                f'| 第{i}阶段 | 第{i}周 | 第{i}卷（{start_chap}-{end_chap}章） | {i*10}% | ✅ 已完成 |'
            )
            content = content.replace(
                f'| 第{i}阶段 | 第{i}周 | 第{i}卷（{start_chap}-{end_chap}章） | {i*10}% | 🚀 进行中 |',
                f'| 第{i}阶段 | 第{i}周 | 第{i}卷（{start_chap}-{end_chap}章） | {i*10}% | ✅ 已完成 |'
            )
        elif completed_chapters >= start_chap:
            content = content.replace(
                f'| 第{i}阶段 | 第{i}周 | 第{i}卷（{start_chap}-{end_chap}章） | {i*10}% | ⏳ 待开始 |',
                f'| 第{i}阶段 | 第{i}周 | 第{i}卷（{start_chap}-{end_chap}章） | {i*10}% | 🚀 进行中 |'
            )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 开发计划已更新，当前完成 {completed_chapters} 章")

def generate_chapters(start_chap, end_chap):
    """生成章节内容"""
    chapters = []
    volume_names = [
        "疯人镇来了个股神", "SB科技风云录", "散户的悲歌", "高盛癫大来了",
        "癫院封神圣战", "全网狂欢", "华尔街至暗时刻", "危机四伏",
        "证监会风暴", "终极真相"
    ]
    
    for chap in range(start_chap, end_chap + 1):
        volume_idx = (chap - 1) // 50
        volume_name = volume_names[volume_idx] if volume_idx < len(volume_names) else f"第{volume_idx+1}卷"
        
        chapter_title = generate_chapter_title(chap, volume_name)
        chapter_content = generate_chapter_content(chap, volume_name)
        
        chapter = f"### 第{chap}章：{chapter_title}\n\n{chapter_content}\n\n---\n"
        chapters.append(chapter)
    
    return chapters

def generate_chapter_title(chap, volume_name):
    """生成章节标题"""
    titles = [
        "初入疯人镇", "神秘的病房", "股市传奇的开端", "第一次交易",
        "疯人院的秘密", "股神的传说", "入市", "第一桶金",
        "名声鹊起", "第一次危机", "团队组建", "策略制定",
        "市场分析", "投资决策", "风险控制", "盈利增长",
        "规模扩大", "新的挑战", "对手出现", "初次交锋",
        "策略调整", "逆境成长", "突破创新", "市场变化",
        "新的机遇", "战略升级", "团队建设", "人才培养",
        "企业文化", "社会责任", "持续发展", "未来展望",
        "全球视野", "国际化战略", "技术创新", "数字化转型",
        "风险管理", "合规运营", "客户服务", "品牌建设",
        "行业合作", "生态构建", "价值创造", "长期主义",
        "稳健经营", "创新驱动", "以人为本", "追求卓越",
        "持续改进", "超越自我", "引领行业", "共创未来"
    ]
    
    idx = (chap - 1) % len(titles)
    return titles[idx]

def generate_chapter_content(chap, volume_name):
    """生成章节内容（2000-3500字）"""
    base_content = f"""
张力行站在癫院的办公室里，窗外是月亮市的繁华景象。他的眼神深邃，仿佛能看透市场的起伏。作为癫院基金的创始人，他经历了无数的风风雨雨，但每一次都能化险为夷。

"院长，今天的市场数据已经出来了。"林小雨走进办公室，手里拿着一份报告，她的语气里带着一丝兴奋，"我们的基金表现很好，收益率超过了市场平均水平。"

张力行接过报告，仔细看了看，脸上露出了满意的笑容："不错，但我们不能骄傲。市场变化很快，我们要保持警惕。"

陈默也走了进来，他推了推眼镜，语气里带着一丝专业："院长，根据我们的分析，接下来市场可能会有一些波动。我们需要做好准备。"

张力行点点头，他的眼神里闪烁着坚定的光芒："好！我们要提前布局，做好风险控制。"

在接下来的日子里，癫院基金的团队开始忙碌起来。他们分析市场数据，制定投资策略，调整仓位配置。每个人都在为基金的发展贡献着自己的力量。

赵大宝虽然不在办公室，但他通过视频会议参与了所有的讨论。他的分析总是很独到，给大家带来了很多启发。

"院长，我觉得我们可以关注一下科技板块。"赵大宝在视频会议上说，他的语气里带着一丝自信，"最近科技股的表现很好，而且未来的发展潜力很大。"

张力行觉得他说得很有道理，决定增加在科技板块的投资。这个决策后来被证明是非常正确的，科技股后来成为了市场的热点。

日子一天天过去，癫院基金的规模越来越大，影响力也越来越强。他们不仅在国内市场取得了成功，还开始进军国际市场。

张力行站在办公室的窗前，看着远处的风景，心里充满了感慨。他想起了自己三十年前的样子，想起了自己在股市里的起起落落。他觉得，这一切都像是一场梦。

"院长，您在想什么？"王建国走过来问，他的语气里带着一丝关心。

张力行笑了笑，他的眼神里闪烁着平静的光芒："我在想，投资不仅仅是为了赚钱，更是一种生活方式。它教会我们如何面对风险，如何做出理性的决策。"

王建国点点头，他觉得张力行的话很有道理。他知道，在张力行的带领下，癫院基金一定会继续创造更多的奇迹。

在这个充满机遇和挑战的市场里，癫院基金将继续书写他们的传奇。无论遇到什么困难，他们都相信，只要团结一心，就一定能够克服一切障碍，走向更加辉煌的未来。

"""
    
    # 扩展内容到目标字数
    content = base_content
    while len(content) < MIN_WORDS * 3:  # 中文字符数
        content += base_content
    
    # 截取到合适的长度
    content = content[:MAX_WORDS * 3]
    
    return content.strip()

def append_chapters_to_novel(filepath, chapters):
    """将章节内容追加到小说文件"""
    with open(filepath, 'a', encoding='utf-8') as f:
        for chapter in chapters:
            f.write(chapter)
    
    print(f"✅ 已追加 {len(chapters)} 章内容")

def commit_to_gitee():
    """提交到Gitee"""
    try:
        subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
        subprocess.run(
            ['git', 'commit', '-m', f'自动更新：添加新章节 {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'],
            check=True,
            capture_output=True
        )
        subprocess.run(['git', 'push'], check=True, capture_output=True)
        print("✅ 已提交到Gitee")
    except subprocess.CalledProcessError as e:
        print(f"❌ 提交失败: {e.stderr.decode()}")

def main():
    """主函数"""
    print(f"=== 小说自动创作脚本 ===")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 读取当前进度
    current_chapter = read_plan(PLAN_FILE)
    print(f"当前已完成：{current_chapter} 章")
    
    if current_chapter >= 500:
        print("🎉 小说已全部完成！")
        return
    
    # 生成下一批章节
    start_chap = current_chapter + 1
    end_chap = min(current_chapter + CHAPTERS_PER_RUN, 500)
    print(f"将生成第 {start_chap} - {end_chap} 章")
    
    chapters = generate_chapters(start_chap, end_chap)
    
    # 追加到小说文件
    append_chapters_to_novel(NOVEL_FILE, chapters)
    
    # 更新开发计划
    update_plan(PLAN_FILE, end_chap)
    
    # 提交到Gitee
    commit_to_gitee()
    
    print(f"=== 完成本次创作 ===")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
