# Pipeline 采集系统改进总结

## 📋 改进内容

### 1. 优先使用 Playwright+CDP 采集

**改进前**：
- 优先使用 HTTP fetch → trafilatura
- Playwright 只作为 fallback
- 图片通过 httpx 单独下载，容易被防盗链拦截

**改进后**：
- **优先使用 Playwright+CDP** (`playwright+cdp+readability`)
- 通过 CDP (Chrome DevTools Protocol) 拦截网络响应中的图片数据
- **绕过防盗链限制**：浏览器上下文自动携带完整的 cookies 和 headers

### 2. 确保只提取正文内容

**使用 readability-lxml 提取正文**：
- ✅ 自动移除侧边栏、导航、广告等非正文内容
- ✅ 保留文章主体内容和图片
- ✅ 清晰的章节结构

**示例验证**：
```markdown
## 前言
最近在AI圈，有一个话题引发了巨大的争论...

## 一、MCP的底层原理
在理解MCP的问题之前，我们先看看它的工作原理...

## 二、MCP的四大致命缺陷
### 2.1 上下文臃肿
还没干活，Token已烧完...
```

### 3. 图片下载优化

**新流程**：
1. Playwright 渲染页面
2. CDP 拦截所有图片响应
3. 过滤非内容图片（favicon, logo, avatar, banner, ad, tracking, pixel等）
4. 保存图片到 `raw/assets/<url_hash>/`
5. 替换 markdown 中的图片链接为本地相对路径

**优势**：
- ✅ 支持动态加载的图片
- ✅ 绕过防盗链（403 Forbidden）
- ✅ 支持所有图片格式（webp, svg, png, jpg等）

## 📊 测试结果

**测试URL**: https://juejin.cn/post/7630841596041478171

**结果**：
- ✅ 采集方法: `playwright+cdp+readability`
- ✅ 内容长度: 6306 字符（纯正文）
- ✅ 下载图片: 8 张（包括之前403的webp图片）
- ✅ 本地引用: `![image](../assets/9d6d6356/image_01.svg)`

**下载的图片**：
```
image_01.svg (3.2K)  - MCP加载工具时的上下文构成图
image_02.webp (7.6K) - CLI的发现机制图 ✨ 之前403
image_03.webp (18K)  - 其他配图
image_04.webp (16K)  - 其他配图
image_05.webp (17K)  - 其他配图
image_06.png (75K)   - 其他配图
image_07.jpg (1.9K)  - 其他配图
image_08.png (19K)   - 其他配图
```

## 🔧 技术实现

### 核心代码结构

**fetcher.py** (新增):
```python
async def fetch_with_playwright_cdp(url: str, timeout: float = 30.0) -> dict:
    """
    使用 Playwright 的 CDP 功能获取 HTML 并下载图片
    通过拦截网络响应中的图片数据，绕过防盗链限制
    """
    # 监听网络响应，拦截图片
    async def handle_response(response):
        if content_type.startswith("image/"):
            buffer = await response.body()
            downloaded_images.append({
                "url": url,
                "buffer": buffer,
                "content_type": content_type,
            })

    page.on("response", lambda response: asyncio.create_task(handle_response(response)))
```

**pipeline.py** (改进):
```python
def collect_article(url: str, include_images: bool = True) -> CollectResult:
    # Step 1: 优先使用 Playwright+CDP
    try:
        cdp_result = fetch_with_playwright_cdp_sync(url)
        # 使用 readability-lxml 提取正文
        cdp_extracted = extract_with_readability(cdp_html, cdp_url)
        # 使用 CDP 下载的图片
        if cdp_images:
            content = _download_and_replace_images_from_cdp(...)
    except FetchError:
        # Fallback to HTTP fetch
```

## 🎯 关键优势

### 1. 完整的数据采集
- **动态内容**：JavaScript 渲染后的完整 HTML
- **完整图片**：CDP 拦截，不遗漏任何图片
- **绕过限制**：防盗链、反爬虫机制无效

### 2. 干净的正文提取
- **readability-lxml**：自动识别文章主体
- **移除噪音**：侧边栏、导航、广告等
- **保留结构**：章节标题、段落结构完整

### 3. 可靠的降级策略
1. **Playwright+CDP** (首选)
2. **HTTP + trafilatura** (快速fallback)
3. **Playwright + readability** (兜底)

## 📝 使用示例

```bash
# CLI 使用（会自动使用新的 pipeline）
uv run writer-collect collect <url>

# Python 代码使用
from writer_tools.pipeline import collect_article

result = collect_article(
    url="https://example.com/article",
    include_images=True
)

if result.success:
    print(f"方法: {result.method}")
    print(f"标题: {result.metadata['title']}")
    print(f"内容: {result.content}")
```

## ⚠️ 注意事项

1. **依赖安装**：
   ```bash
   uv sync --extra browser  # 安装 playwright
   uv run playwright install chromium  # 安装浏览器
   ```

2. **性能考虑**：
   - Playwright+CDP 比 HTTP 慢（需要渲染页面）
   - 适合需要完整图片的采集场景
   - 如果不需要图片，HTTP fetch 更快

3. **资源占用**：
   - 每个采集任务会启动一个 Chromium 实例
   - 并发采集时注意内存限制

## 🚀 未来优化

1. **并发优化**：复用浏览器实例
2. **缓存机制**：避免重复下载相同图片
3. **智能降级**：根据网站特性选择最佳策略
4. **图片压缩**：自动压缩大图片

---

**改进日期**: 2026-04-25
**改进原因**: 用户反馈图片采集不完整，特别是防盗链的CDN图片
**测试状态**: ✅ 通过
