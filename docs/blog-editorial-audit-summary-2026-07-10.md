# Ainnc 全站博客编辑审查报告（2026-07-10）

> 后续规则更新：本文件记录的是早期修正过程，其中“补齐所有 TL;DR/FAQ/清单”的做法已被废止。当前有效的结构规则以 `docs/blog-content-guidelines.md` 和 `docs/blog-no-template-ending-audit-2026-07-10.md` 为准：这些模块全部按内容需要选择，文章只强制内容密度与真实收尾。

> 2026-07-11 FAQ 专项复查：实际 FAQ 覆盖从 28/71 收缩到 8/71，保留项均增加 `faqIntent`；详见 `docs/blog-faq-audit-2026-07-11.md`。

## 汇总

- 检查范围：`src/content/blog` 内 70 篇 Markdown 源文章，包含已发布与项目中可发现的全部文章；未发现独立维护的 HTML 文章源文件，`dist` 中 HTML 均由这些 Markdown 构建生成。
- 初次脚本结果：70 篇检查，0 篇通过，70 篇未通过。
- 初次结构问题：30 篇缺少 TL;DR；69 篇没有 FAQ，另 1 篇 FAQ 格式不合格；所有文章均已补齐或重构。
- 说明书腔：脚本标记 6 篇、6 个段落，均已改写成“场景 → 原因 → 判断 → 方法”的叙述；另对跨境电商文章中混在 FAQ 下的长段落做了人工重构。
- 补充人工检查：8 篇旧文章曾把问答直接塞进长段落，现已删除重复内嵌问答，只保留独立 FAQ 模块。
- 最终脚本结果：70 篇检查，70 篇通过，0 篇未通过。
- 解析失败：0 篇。

原始逐篇输出：

- [修改前原始输出](./blog-editorial-audit-initial-2026-07-10.txt)
- [修改后原始输出](./blog-editorial-audit-final-2026-07-10.txt)

## 说明书腔改写明细

- `ainnc-start.md`：1处：把四类栏目罗列改成20→200个账号的因果叙述。
- `client-offboarding-account-handoff.md`：1处：把六类交接对象改成7天接管验证流程。
- `cloud-phone-vs-browser.md`：1处：把三类环境定义改成6/40/15个账号的选择场景。
- `global-brand-voice-consistency.md`：1处：把三层规则改成10条内容、80%锁定比例的审核推理。
- `mcn-prove-value-with-data.md`：1处：把五项指标改成320个计划任务的续约叙述。
- `task-files-publishing.md`：1处：把版本/复用/追踪定义改成60/20/10个账号的素材流转场景。

## 逐篇结果

| 文章 | 初次脚本结果 | 说明书腔修改 | 最终结果 |
|---|---:|---|---|
| `account-device-proxy-guide.md`<br>账号、设备和代理 IP：批量运营前要先整理的三件事 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `account-first-three-days.md`<br>账号前3天：决定它下半生的养号窗口期 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `account-grouping-strategy.md`<br>账号分组到底该按什么维度来分 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `agency-contract-responsibility-boundaries.md`<br>代运营合同最该写清的，不是每月发多少条 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `agency-pricing-models.md`<br>代运营报价怎么定：按账号数量还是按效果收费 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `ainnc-start.md`<br>Ainnc 博客正式上线 | 1段 / 2项结构问题 | 1处：把四类栏目罗列改成20→200个账号的因果叙述 | ✓ 通过 |
| `asset-library-adoption.md`<br>素材库越建越大，为什么没人愿意用 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `asset-library-reuse.md`<br>素材库解决的不是存储问题，是复用问题 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `automatic-task-retry-risk.md`<br>自动重试是效率功能，还是错误放大器 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `batch-publish-stop-conditions.md`<br>批量发布前，为什么必须先写好暂停条件 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `blunt-client-communication.md`<br>客户天天催进度，团队为什么不能有话直说 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `client-content-approval-deadline.md`<br>客户迟迟不批内容，代运营团队该不该继续等 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `client-group-chat-still-misses-requests.md`<br>每个客户都建了群，为什么团队还是会漏需求 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `client-offboarding-account-handoff.md`<br>客户终止合作时，账号和素材应该怎么交接 | 1段 / 1项结构问题 | 1处：把六类交接对象改成7天接管验证流程 | ✓ 通过 |
| `client-rush-request-triage.md`<br>客户临时插单，团队该说能做还是不能做 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `cloud-phone-vs-browser.md`<br>云手机与浏览器，哪个更适合账号安全 | 1段 / 2项结构问题 | 1处：把三类环境定义改成6/40/15个账号的选择场景 | ✓ 通过 |
| `cloud-phone-vs-emulator.md`<br>多账号运营选云手机还是模拟器？优缺点对比 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `content-idea-meeting-no-one-says-no.md`<br>选题会上没人说不，通常不是团队达成了共识 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `content-portfolio-not-every-account-chase-trends.md`<br>账号矩阵越大，越不能让每个账号都追热点 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `cross-border-ecommerce-social-accounts.md`<br>跨境电商如何批量注册和管理海外社媒账号 | 0段 / 4项结构问题 | 0处 | ✓ 通过 |
| `daily-posting-promise-hurts-renewal.md`<br>承诺每天都发，为什么反而让代运营更难续约 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `dashboard-should-help-stop-work.md`<br>真正有用的数据看板，应该告诉团队停止做什么 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `device-account-limit.md`<br>一台设备能登录几个社媒账号？现实运营中的安全上限 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `employee-offboarding-account-access.md`<br>员工离职后，社媒账号权限应该怎么收回 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `engagement-up-business-flat.md`<br>互动率一直上涨，为什么业务结果却没有变化 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `fewer-posts-better-content.md`<br>内容发得少了，为什么账号反而可能更健康 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `global-brand-scale.md`<br>为全球品牌搭建可规模化的社媒运营体系 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `global-brand-voice-consistency.md`<br>全球品牌统一语气，为什么不等于所有市场说同样的话 | 1段 / 1项结构问题 | 1处：把三层规则改成10条内容、80%锁定比例的审核推理 | ✓ 通过 |
| `global-content-calendar-desync.md`<br>为什么全球内容日历应该允许不同市场不同步 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `headquarters-vs-local-publish-authority.md`<br>总部和本地团队，谁应该拥有最终发布权 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `hiring-tool-vs-account-judgment.md`<br>招聘运营时，会用工具和懂账号完全是两码事 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `instagram-multi-account-content-overlap.md`<br>多个Instagram账号发相似内容，会不会互相抢受众 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `legacy-account-audit.md`<br>接手一批老账号，怎么判断这些账号还能不能用 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `localization-how-deep.md`<br>出海社媒运营，本地化到底该做到多细 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `low-price-client-management-cost.md`<br>报价最低的客户，为什么常常消耗最高的管理成本 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `mcn-prove-value-with-data.md`<br>MCN代运营机构如何用数据向客户证明价值 | 1段 / 2项结构问题 | 1处：把五项指标改成320个计划任务的续约叙述 | ✓ 通过 |
| `monthly-report-trust.md`<br>为什么月报越详细，客户反而越不信任 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `multi-account-ab-test-errors.md`<br>多账号做A/B测试，最容易犯的不是样本太少 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `multi-platform-device-management.md`<br>同一台设备能不能同时登录TikTok和Instagram账号 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `new-client-first-week.md`<br>新客户签进来的第一周，代运营团队应该做什么 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `no-disagreement-in-review-meeting.md`<br>复盘会上没人反对，可能是最危险的结果 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `one-workflow-five-tools.md`<br>从内容生产到发布：一个工作流取代五个工具 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `operations-handoff-loses-judgment.md`<br>运营交接最容易丢的不是密码，而是判断依据 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `operations-team-efficiency.md`<br>一个运营能带多少个账号？别只看账号数量 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `overseas-social-tools-checklist.md`<br>海外社媒批量运营，团队通常需要哪些工具 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `peak-season-scaling.md`<br>旺季来了，账号从50个涨到300个，团队要先做哪三件事 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `proxy-ip-types.md`<br>静态IP、动态IP、移动IP：代理该怎么选 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `real-social-ops-platform.md`<br>真正的社媒运营平台应该是什么样子 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `reddit-brand-advertising-tone.md`<br>品牌做Reddit，为什么越像广告越没人理 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `scaling-social-account-operations.md`<br>代运营机构如何管理上百个社媒账号而不失控 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `shared-password-risk.md`<br>客户把账号密码发到群里，为什么看似省事却最危险 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `should-agency-guarantee-follower-growth.md`<br>客户要结果，代运营团队该不该保证涨粉 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `small-language-market-translator-vs-operator.md`<br>进入小语种市场，应该先找翻译还是先找运营 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `spreadsheets-break-50.md`<br>为什么表格在超过50个账号后就会失控 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `standardization-trap.md`<br>团队总想着标准化流程，但标准化过头会杀死内容的灵气 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `task-center.md`<br>任务中心：为什么不能一个按钮把所有事都做完 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `task-files-publishing.md`<br>如何把任务素材整理成可复用的发布资产 | 1段 / 2项结构问题 | 1处：把版本/复用/追踪定义改成60/20/10个账号的素材流转场景 | ✓ 通过 |
| `team-scale-chaos.md`<br>为什么招的人越多，账号反而管得越乱 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `tiktok-account-banned.md`<br>TikTok账号被封号后，批量账号团队该怎么做 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `tiktok-rate-limit.md`<br>TikTok账号被限流了怎么办？批量账号排查思路 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `tiktok-risk-guide.md`<br>TikTok账号批量运营，如何避开常见风控雷区 | 0段 / 2项结构问题 | 0处 | ✓ 通过 |
| `tiktok-vs-instagram-same-video.md`<br>TikTok和Instagram Reels能不能直接发同一条视频 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `too-professional-to-share.md`<br>内容越专业，为什么有时越没人愿意转发 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `unlimited-revisions-content-rhythm.md`<br>改稿次数越多，代运营服务就越好吗 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `useful-social-ops-audit-log.md`<br>什么样的操作记录，出问题以后才真的有用 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `viral-content-across-account-matrix.md`<br>一条内容爆了，要不要立刻复制到所有账号 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `viral-content-slowdown.md`<br>一个账号突然爆火，团队最该做的不是复制，是紧急减速 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `viral-small-sample-not-growth-model.md`<br>一条内容爆了，为什么还不能叫增长模型 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `when-to-end-client-project.md`<br>什么情况下，代运营团队应该主动结束一个项目 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
| `x-scheduling-real-time.md`<br>X适合提前排期吗？实时平台为什么不能只靠内容日历 | 0段 / 1项结构问题 | 0处 | ✓ 通过 |
