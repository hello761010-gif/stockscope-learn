# StockScope Learn V16 — 修复记录

## 本次针对用户反馈
- 从首页删除 `用数据、纪律和复盘支持判断` 这一脚注，以及其下方整段 Pexels / Coverr 背景视频素材链接列表。
- 移除 `show_data_warning()` 中的 `st.code(error)` 代码样式错误输出；API/网络请求失败时只保留简短的用户提示。
- 移除真实公司摘要失败时 `st.code(lookup["error"])` 技术信息框，避免页面出现突兀的 Python/代码框。
- 页面不再把异常信息以代码块样式呈现。

## 静态检查
- Python compile check: pass
- Homepage source-note text absent: pass
- `st.code(...)` visible output calls: none
- Existing video list and lesson content retained: pass

## Limitation
本环境未运行 Streamlit 浏览器端；以上为代码静态检查和文件打包检查。
