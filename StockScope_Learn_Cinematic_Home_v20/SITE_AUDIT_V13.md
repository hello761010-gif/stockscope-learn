# StockScope Learn V13 — 审查记录

## 修改内容
- 使用用户指定的 Coverr 视频作为轮播第 7 段（最后一段）：“A trader making a call with his smartphone”。
- 保留 Coverr 原始素材页面链接。
- 前 6 段 Pexels 视频顺序不变；轮播仍是 7 段，约 3 秒/段、播放速度 1.3×、直接硬切。
- 保留原有左右滚动浮现、主页面滚动修复、课程内容与学习进度逻辑。
- 没有新增机构视频卡片或额外的视频播放器。

## 视频信息
- 来源页：https://coverr.co/videos/a-trader-making-a-call-with-his-smartphone-do8qjfv1ym
- 页面标注时长 14.7 秒、24 FPS、16:9，并显示 Free Commercial Rights；页面提供 Full HD 下载选项。
- 首页使用的 MP4 地址按 Coverr CDN 常规路径配置为：
  `https://cdn.coverr.co/videos/coverr-a-trader-making-a-call-with-his-smartphone-do8qjfv1ym/1080p.mp4`

## 检查
- Python 语法检查：通过。
- JavaScript 语法检查：通过。
- 视频数组：7 项；前 6 项 Pexels，最后 1 项 Coverr；列表数量和最后一项来源页与用户指定链接一致。
- 来源清单：包含新增 Coverr 原始页面链接。
- 真实浏览器播放：未验证。当前执行环境无法直接请求或播放远程 MP4；Coverr 的新视频页可能需要使用其页面/API提供的有效媒体 URL。如果该 CDN 路径未能播放，可从原素材页面下载 Full HD 视频后改用项目内的本地文件。
