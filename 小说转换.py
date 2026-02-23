# -*- coding: utf-8 -*-
"""
小说转换工具 / Novel-to-EPUB Converter
将纯文本 TXT 文件转换为 EPUB 电子书格式
Convert plain TXT files to EPUB ebook format

支持编码: UTF-8, GBK (常见的中文小说编码)
Supported encodings: UTF-8, GBK (common Chinese novel encodings)
"""

import os
from ebooklib import epub


def convert_txt_to_epub(txt_path, epub_path, book_title="未命名书籍", author="未知作者"):
    """
    Convert a TXT file to EPUB format
    
    参数 / Parameters:
        txt_path (str): TXT 文件路径 / Path to the TXT file
        epub_path (str): 输出 EPUB 文件路径 / Path to save the EPUB file
        book_title (str): 书籍标题 / Title of the book
        author (str): 作者名称 / Author name
    
    说明 / Notes:
        - 自动处理 UTF-8 和 GBK 编码 / Automatically handles UTF-8 and GBK encoding
        - 应用中文排版规范（段落缩进）/ Applies Chinese typography (paragraph indentation)
        - 生成单章节 EPUB / Generates single-chapter EPUB
    """
    
    # ========== 步骤 1: 初始化 EPUB 书籍信息 ==========
    # Step 1: Initialize EPUB book with metadata
    book = epub.EpubBook()
    book.set_title(book_title)  # 设置书籍标题 / Set book title
    book.set_language('zh')      # 设置语言为中文 / Set language to Chinese
    book.add_author(author)      # 添加作者信息 / Add author information

    # ========== 步骤 2: 读取 TXT 内容（编码容错处理）==========
    # Step 2: Read TXT content with encoding error handling
    content = ""
    try:
        # 优先尝试 UTF-8 编码（现代标准）
        # First try UTF-8 encoding (modern standard)
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # UTF-8 失败时退回到 GBK（传统中文小说常用编码）
        # Fall back to GBK when UTF-8 fails (legacy Chinese novel encoding)
        try:
            with open(txt_path, 'r', encoding='gbk') as f:
                content = f.read()
        except UnicodeDecodeError:
            print(f"警告: 无法识别 {txt_path} 的编码 / Warning: Cannot decode {txt_path}")
            return

    # ========== 步骤 3: 将文本转换为 HTML 段落格式 ==========
    # Step 3: Convert text to HTML paragraph format with Chinese typography
    html_content = ""
    for line in content.split('\n'):
        if line.strip():  # 过滤空行 / Skip empty lines
            # CSS 缩进：text-indent: 2em 实现首行缩进 2 个汉字
            # CSS indentation: text-indent: 2em indents first line by 2 characters
            html_content += f"<p style='text-indent: 2em;'>{line.strip()}</p>\n"

    # ========== 步骤 4: 创建章节并添加内容 ==========
    # Step 4: Create chapter and add content
    chapter = epub.EpubHtml(
        title='正文',              # 章节标题 / Chapter title
        file_name='content.xhtml', # 文件名 / File name
        lang='zh'                  # 语言 / Language
    )
    # 添加水印和书名标题 / Add watermark and book title
    watermark = '<p style="text-align: center; font-size: 0.8em; color: #999; margin-bottom: 2em;">' \
                'Converted by: <a href="https://github.com/oueifu/-Novel-to-EPUB-Converter">' \
                'https://github.com/oueifu/-Novel-to-EPUB-Converter</a></p>'
    chapter.content = f'{watermark}<h1>{book_title}</h1>{html_content}'
    book.add_item(chapter)

    # ========== 步骤 5: 生成目录和导航 ==========
    # Step 5: Generate table of contents and navigation
    book.toc = (chapter,)           # 设置目录 / Set table of contents
    book.add_item(epub.EpubNcx())   # 添加 NCX 导航文件 / Add NCX navigation file
    book.add_item(epub.EpubNav())   # 添加 Nav 导航文件 / Add Nav navigation file

    # ========== 步骤 6: 设置阅读顺序（书脊）==========
    # Step 6: Set reading order (spine)
    book.spine = ['nav', chapter]  # 定义阅读顺序 / Define reading order

    # ========== 步骤 7: 导出 EPUB 文件 ==========
    # Step 7: Export EPUB file
    epub.write_epub(epub_path, book, {})
    print(f"✓ 转换成功！/ Conversion successful!")
    print(f"  文件已保存至 / File saved to: {os.path.abspath(epub_path)}")


# ========== 主程序 / Main Program ==========
# 批量转换当前目录下的所有 TXT 文件
# Batch convert all TXT files in the current directory
if __name__ == "__main__":
    converted_count = 0
    
    # 遍历当前目录的所有文件 / Iterate through all files in current directory
    for filename in os.listdir('.'):
        if filename.endswith('.txt'):  # 只处理 TXT 文件 / Only process TXT files
            txt_path = filename
            # 获取不含扩展名的文件名作为书籍标题
            # Extract filename without extension as book title
            book_title = os.path.splitext(filename)[0]
            # 生成 EPUB 输出路径 / Generate EPUB output path
            epub_path = book_title + '.epub'
            
            print(f"正在转换 / Converting: {filename}...")
            convert_txt_to_epub(
                txt_path,
                epub_path,
                book_title=book_title,
                author="未知作者"  # 默认作者 / Default author: Unknown
            )
            converted_count += 1
    
    if converted_count == 0:
        print("⚠ 当前目录未找到 TXT 文件 / No TXT files found in current directory")
    else:
        print(f"\n✓ 完成！共转换 {converted_count} 个文件 / Done! Converted {converted_count} file(s)")