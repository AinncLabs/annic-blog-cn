import type { CollectionEntry } from 'astro:content';

export type Locale = 'zh' | 'en';

export const SITE_COPY = {
	zh: {
		title: 'Ainnc 麦芽营销',
		description: '分享 Ainnc 麦芽营销的产品更新、社媒账号运营、素材管理和批量任务发布实践。',
		home: '首页',
		blog: '博客',
		about: '关于',
		officialSite: '进入官网',
		telegram: '加入 Telegram',
	},
	en: {
		title: 'Ainnc',
		description:
			'Product updates, social account operations, asset management, and bulk publishing workflows from Ainnc.',
		home: 'Home',
		blog: 'Blog',
		about: 'About',
		officialSite: 'Official Site',
		telegram: 'Join Telegram',
	},
} as const;

const EN_POSTS = {
	'ainnc-start': {
		title: 'The Ainnc Blog Is Live',
		description:
			'Product updates, social account operations, asset management, and bulk publishing practices from Ainnc.',
		category: 'Product Updates',
		tags: ['Ainnc', 'Product', 'Blog'],
		sections: [
			{
				paragraphs: [
					'Welcome to the Ainnc Blog.',
					'Here we will share product updates, social media operations guides, bulk task publishing practices, and lessons from building a scalable operations console.',
				],
			},
			{
				heading: 'What We Will Cover',
				paragraphs: [
					'Ainnc product updates and release notes.',
					'Account importing, grouping, device binding, and proxy IP setup.',
					'Video, image, and document asset management workflows.',
					'Bulk publishing practices for TikTok, Instagram, Reddit, X, and other social platforms.',
					'Usage limits, task status tracking, and execution review.',
				],
			},
		],
	},
	'account-device-proxy-guide': {
		title: 'Accounts, Devices, and Proxy IPs: Three Things to Prepare Before Bulk Operations',
		description:
			'Organize account groups, device bindings, and proxy IPs before entering the task center.',
		category: 'Tutorials',
		tags: ['Accounts', 'Proxy IP', 'Device Binding'],
		sections: [
			{
				paragraphs: [
					'Before publishing bulk tasks in Ainnc, it is worth organizing accounts, devices, and proxy IP resources first.',
					'Accounts define the task targets, devices define the execution environment, and proxy IPs affect login stability and platform access.',
				],
			},
			{
				heading: 'Recommended Preparation Flow',
				paragraphs: [
					'Import accounts and group them by region, platform, or business line.',
					'Bind devices so accounts can be scheduled by tasks.',
					'Configure proxy IPs and check abnormal proxies regularly.',
					'Once these relationships are stable, publishing tasks for TikTok, Instagram, Reddit, X, and other platforms becomes easier to manage and troubleshoot.',
				],
			},
		],
	},
	'task-files-publishing': {
		title: 'Turning Task Files Into Reusable Publishing Assets',
		description:
			'How to upload, group, and reuse video, image, and document assets in Ainnc.',
		category: 'Operations',
		tags: ['Assets', 'Task Publishing', 'Content Operations'],
		sections: [
			{
				paragraphs: [
					'Ainnc lets teams manage images, videos, and documents in one file module. After upload, these assets can be selected directly in task parameters.',
					'For bulk publishing, asset management is not just storage. It is the foundation for repeatable publishing workflows.',
				],
			},
			{
				heading: 'Recommended Grouping Methods',
				paragraphs: [
					'Group by platform, such as TikTok, Instagram, Reddit, and X.',
					'Group by content theme, such as product demos, campaign assets, and customer stories.',
					'Group by publishing cycle, such as weekly campaigns, test assets, and final assets.',
					'When assets, accounts, and task batches are aligned, reviewing task status and execution results becomes much clearer.',
				],
			},
		],
	},
	'peak-season-scaling': {
		title: 'Peak Season Is Coming: What to Prepare Before 50 Accounts Become 300',
		description:
			'Before expanding an account pool from 50 to 300, teams need capacity planning for devices, proxies, content, and monitoring.',
		category: 'Operations Playbook',
		tags: ['Peak Season', 'Account Matrix', 'Operations Playbook'],
		sections: [
			{
				paragraphs: [
					'Promotions, peak season, and new market launches can all push a team to scale its account pool quickly. Moving from 50 accounts to 300 looks like a number change, but operationally it is a different system.',
					'If the preparation order is wrong, the team may create the exact chaos it hoped to avoid: accounts waiting for devices, proxies being reused too aggressively, content pipelines falling behind, and abnormal accounts being discovered too late.',
				],
			},
			{
				heading: 'The Common Mistake: Add Accounts First, Fix Infrastructure Later',
				paragraphs: [
					'Many teams start by acquiring or registering more accounts, assuming the rest can be fixed while work is already running. That is risky.',
					'Devices and proxy IPs are not supporting details. They are the environment accounts live in. If they lag behind the account pool, new accounts start their lifecycle under resource pressure and repeated environment overlap.',
				],
			},
			{
				heading: 'First: Calculate Device and Proxy Capacity',
				paragraphs: [
					'Before importing the new accounts, estimate how many independent device environments and proxy resources the final account pool will need.',
					'Prepare capacity in batches so every new group of accounts can be assigned a real environment immediately instead of sitting in a queue while the team scrambles for resources.',
				],
			},
			{
				heading: 'Second: Build the Content Pipeline Early',
				paragraphs: [
					'When account volume grows sixfold, content demand usually grows at the same speed. If the team still creates and assigns content account by account, the bottleneck appears fast.',
					'Reusable assets, grouped file libraries, and planned publishing batches need to exist before the seasonal pressure arrives.',
				],
			},
			{
				heading: 'Third: Decide How Monitoring Will Work',
				paragraphs: [
					'At 50 accounts, someone can still manually check status. At 300 accounts, that approach breaks down.',
					'Task results, account status, abnormal proxies, and publishing failures need a shared review rhythm so issues are found by the team before clients or managers ask about them.',
				],
			},
			{
				heading: 'Where Ainnc Helps',
				paragraphs: [
					'Ainnc supports batch management of cloud phone environments, proxy IPs, accounts, files, tasks, and usage views.',
					'That lets teams prepare the operating foundation before the account pool expands, instead of trying to patch the system while peak season is already running.',
				],
			},
		],
	},
	'account-first-three-days': {
		title: 'The First Three Days of a Social Account Matter More Than Teams Think',
		description:
			'Why new accounts should not be pushed into publishing immediately, and how teams can manage new, growing, and stable accounts differently.',
		category: 'Platform Guides',
		tags: ['Account Warming', 'Account Safety', 'Platform Guides'],
		sections: [
			{
				paragraphs: [
					'The first few days of a new account often shape its long-term operating stability more than later content strategy does.',
					'Many teams focus on what to publish while treating brand-new accounts with the same rhythm as mature accounts. That is one of the easiest ways to create avoidable risk in bulk social operations.',
				],
			},
			{
				heading: 'Newness Is a Risk State',
				paragraphs: [
					'A new account has little history. Platforms judge it mainly by what happens next: login behavior, browsing patterns, interaction frequency, publishing rhythm, and environment consistency.',
					'If a new account quickly starts high-frequency publishing or repeated interactions, that behavior looks very different from a normal user learning a platform.',
				],
			},
			{
				heading: 'The First Goal Is Not Publishing',
				paragraphs: [
					'In the first three days, the account should build a normal usage record: login, browsing, light interaction, and gradual activity.',
					'This stage is not about output volume. It is about helping the account become recognizable as a normal user before asking it to carry operational work.',
				],
			},
			{
				heading: 'Treat New Accounts as Their Own Stage',
				paragraphs: [
					'A practical framework is to separate accounts into new, growing, and stable stages.',
					'New accounts focus on warming. Growing accounts can publish at low frequency while continuing interaction. Stable accounts gradually move toward the normal operating rhythm.',
				],
			},
			{
				heading: 'How Ainnc Supports This Workflow',
				paragraphs: [
					'Ainnc lets teams group accounts by lifecycle stage and run warming tasks separately from publishing tasks.',
					'That separation keeps teams from accidentally pushing new accounts into the same batch as mature accounts, especially when account volume is high.',
				],
			},
		],
	},
	'asset-library-reuse': {
		title: 'An Asset Library Solves Reuse, Not Just Storage',
		description:
			'For multi-account operations, an asset library is not a cloud drive. It is the layer that makes videos, images, and documents reusable across tasks.',
		category: 'Product Capabilities',
		tags: ['Asset Library', 'File Management', 'Product Capabilities'],
		sections: [
			{
				paragraphs: [
					'When teams first hear about an asset library, the common reaction is: we already have cloud storage.',
					'That response is understandable, but storage is not the main problem in bulk social operations. The harder problem is safe, repeatable reuse.',
				],
			},
			{
				heading: 'Cloud Drives Store Files. Operations Need Files to Be Usable.',
				paragraphs: [
					'A cloud drive is good at storing and sharing files. But once a team manages dozens of accounts and publishes many pieces of content each week, finding the right version becomes work by itself.',
					'Files get downloaded, edited, renamed, and reuploaded until no one is sure whether "final_v2_real_final.mp4" is actually the file that should be used.',
				],
			},
			{
				heading: 'One Asset Should Support Many Account Tasks',
				paragraphs: [
					'A product video may be used across multiple TikTok accounts with different titles and tags, adapted for Instagram, and referenced in Reddit posts.',
					'If every use requires finding the file, downloading it, and uploading it again, reuse becomes slow and error-prone.',
				],
			},
			{
				heading: 'Version Confusion Is a Real Risk',
				paragraphs: [
					'The cost of version confusion is not only wasted time. Teams can accidentally publish outdated assets, noncompliant copy, or content the client already asked to stop using.',
					'An asset library turns the current valid file into a system state rather than a memory game across chat messages and local folders.',
				],
			},
			{
				heading: 'How Ainnc Handles Assets',
				paragraphs: [
					'Ainnc supports batch uploading, grouping, and status control for videos, images, and documents.',
					'Once an asset is uploaded, operators can select it directly inside task parameters. The team works from one managed file record instead of many scattered copies.',
				],
			},
		],
	},
	'new-client-first-week': {
		title: 'What an Agency Should Do in the First Week After Signing a New Client',
		description:
			'A practical first-week sequence for importing accounts, binding devices and proxies, checking status, warming accounts, and launching the first publishing batch.',
		category: 'Product Capabilities',
		tags: ['Client Onboarding', 'Task Center', 'Product Capabilities'],
		sections: [
			{
				paragraphs: [
					'Signing a new client is exciting, but many agency problems begin immediately after the contract is signed.',
					'Accounts are not fully imported, devices and proxies are not assigned, and the client is already asking when the first posts will go live. If the order is wrong in week one, the team may spend the next month explaining avoidable issues.',
				],
			},
			{
				heading: 'The Scenario: 30 TikTok and Instagram Accounts',
				paragraphs: [
					'Imagine a Southeast Asia beauty brand brings 30 accounts: 20 TikTok accounts and 10 Instagram accounts. Some are semi-new and have not been operated consistently.',
					'The first instinct may be to build the content calendar. But the account foundation should come first.',
				],
			},
			{
				heading: 'Days 1-2: Import Accounts and Assign Environments',
				paragraphs: [
					'Import accounts into the system and group them by client, platform, and market. Avoid starting with a temporary spreadsheet that later becomes the real source of truth by accident.',
					'At the same time, assign cloud devices and proxy IPs. Every account should have an environment before the team starts publishing.',
				],
			},
			{
				heading: 'Day 3: Check Account Status Before Content',
				paragraphs: [
					'Semi-new accounts may not all be healthy. Some may already have abnormal prompts or login issues caused by previous use.',
					'Check the account pool first and separate abnormal accounts before bulk tasks begin.',
				],
			},
			{
				heading: 'Days 4-5: Warm Accounts Before Publishing',
				paragraphs: [
					'For accounts with uncertain activity history, warming is safer than aggressive immediate publishing.',
					'This may feel slower, especially when the client wants fast output, but early account problems usually cost more time than a short preparation window.',
				],
			},
			{
				heading: 'Days 6-7: Launch the First Controlled Batch',
				paragraphs: [
					'Once account status, environments, and assets are clear, the team can start the first publishing batch.',
					'Keep the first batch moderate, review execution feedback, then gradually move into the regular operating rhythm.',
				],
			},
			{
				heading: 'How Ainnc Supports the Sequence',
				paragraphs: [
					'Ainnc supports batch account import, grouping, device and proxy binding, separate login/warming/publishing tasks, and execution records.',
					'That gives the team a complete first-week operating view instead of relying on memory, chat updates, and temporary sheets.',
				],
			},
		],
	},
	'team-scale-chaos': {
		title: 'Why Hiring More Operators Can Make Account Management Messier',
		description:
			'When teams grow, account handoff, onboarding, and recordkeeping can become more chaotic unless the system grows with the team.',
		category: 'Operations Playbook',
		tags: ['Team Workflow', 'Account Management', 'Operations Playbook'],
		sections: [
			{
				paragraphs: [
					'Many agency leaders run into the same counterintuitive problem: account volume grows, the team hires more people, and account management becomes less clear than before.',
					'Handoffs fail more often, new employees take longer to onboard, and two operators may accidentally change the same client account in conflicting ways.',
				],
			},
			{
				heading: 'Hiring Shares Workload, Not Chaos',
				paragraphs: [
					'Hiring more operators can reduce the amount of manual work per person. It does not automatically create a shared account system.',
					'If account status lives in personal spreadsheets, notes apps, chat histories, and memory, every new hire adds another recording style to an already fragmented workflow.',
				],
			},
			{
				heading: 'Every Operator Has a Personal Method',
				paragraphs: [
					'One operator may track accounts in a sheet. Another may keep notes in an app. A third may rely on recent memory and chat messages.',
					'These habits may work individually, but they break when an account has to move between people because of leave, handoff, or temporary support.',
				],
			},
			{
				heading: 'Onboarding Gets Slower as the Team Grows',
				paragraphs: [
					'Mature teams should onboard faster because the workflow is clear. Fragmented teams onboard slower because new people have to learn everyone else’s private habits.',
					'The more people and accounts involved, the more oral handoff is repeated instead of being replaced by one shared system.',
				],
			},
			{
				heading: 'The System Needs to Scale, Not Just Headcount',
				paragraphs: [
					'A practical test is simple: how long does it take a new operator to independently manage a group of accounts?',
					'If the answer depends on shadowing an experienced employee for weeks, the team is relying on personal memory rather than operational records.',
				],
			},
			{
				heading: 'How Ainnc Fits In',
				paragraphs: [
					'Ainnc keeps account information, device binding, proxy binding, and operation records in one system.',
					'New team members learn the system instead of learning each operator’s private format. As the team grows, the operating record stays consistent.',
				],
			},
		],
	},
	'account-grouping-strategy': {
		title: 'How Should Teams Group Social Accounts?',
		description:
			'How to design account groups around platforms, clients, lifecycle stages, and markets so bulk tasks can select the right accounts directly.',
		category: 'Operations Playbook',
		tags: ['Account Grouping', 'Bulk Operations', 'Operations Playbook'],
		sections: [
			{
				paragraphs: [
					'Once a team manages enough accounts, grouping becomes unavoidable. The mistake is treating groups like labels that make the dashboard look tidy.',
					'A useful group is not decoration. It exists so the operator can start a bulk task and select the right batch immediately, without manually checking and excluding accounts one by one.',
				],
			},
			{
				heading: 'Groups Should Serve Operations, Not Neatness',
				paragraphs: [
					'The test is simple: when you launch a bulk task, can one group represent the exact accounts you need?',
					'If the operator still has to filter again, remove exceptions, or ask another teammate which accounts belong in the task, the grouping logic was probably designed from the wrong angle.',
				],
			},
			{
				heading: 'Common Grouping Dimensions',
				paragraphs: [
					'Platform-based grouping is the most direct starting point because TikTok, Instagram, Reddit, and X each have different operating habits and risk patterns.',
					'Client or project grouping is useful for agencies because reporting, billing, and delivery often happen by client. Lifecycle grouping separates new accounts, growing accounts, and stable accounts so teams do not run the same task on accounts with very different risk levels.',
					'Market-based grouping helps global teams plan by region and time zone. In practice, most teams combine several of these dimensions instead of relying on only one.',
				],
			},
			{
				heading: 'Start From the Task, Not the Taxonomy',
				paragraphs: [
					'It is easy to list every possible way to categorize accounts. A better question is: what bulk task does the team run most often?',
					'If the weekly routine is publishing the same content for all accounts under one client, client should probably be the primary grouping dimension. If the weekly routine is warming all accounts on one platform, platform should come first.',
					'The best grouping system follows the team’s highest-frequency operation, not the most theoretically complete classification model.',
				],
			},
			{
				heading: 'One Grouping System Usually Has One Primary Dimension',
				paragraphs: [
					'In many account systems, one account can belong to only one group at a time. That means groups alone cannot fully represent platform, market, lifecycle stage, and client all at once.',
					'A practical setup is to choose one primary grouping dimension and let filters handle the rest. For example, group by client, then use platform and status filters to find active TikTok accounts under that client.',
					'This avoids creating dozens of tiny cross-groups that are hard to maintain and harder for the team to understand.',
				],
			},
			{
				heading: 'Naming Rules Matter',
				paragraphs: [
					'When filters are not enough, group names can carry compressed information. A shared naming rule is better than improvised names like “group 1,” “temporary accounts,” or “pending.”',
					'For example, a group name like “US-TT-New” tells the team the market, platform, and lifecycle stage at a glance. The value is not formal naming for its own sake. The value is reducing follow-up questions during real operations.',
				],
			},
			{
				heading: 'A Real Example',
				paragraphs: [
					'One client environment had 155 accounts: 100 TikTok accounts in a “TK” group, 4 Instagram accounts in an “ins” group, and 51 accounts still ungrouped.',
					'The ratio itself tells a story. The team is clearly focusing most resources on TikTok while using Instagram as a smaller test channel. That is a common global growth pattern: go deep on the platform that is already moving before spreading the team thin across every channel.',
					'The 51 ungrouped accounts are not necessarily a failure. They may be newly imported accounts still under observation before the team decides where they belong.',
				],
			},
			{
				heading: 'Too Coarse and Too Fine Both Break',
				paragraphs: [
					'If hundreds of accounts sit in one or two broad groups, operators still have to manually select accounts during every task. The group exists, but it does not help.',
					'If the team creates too many tiny groups, the grouping system becomes another thing to manage. A good practical range is usually small enough that teammates can scan the groups and understand what each one means.',
				],
			},
			{
				heading: 'Environment Standards Still Matter',
				paragraphs: [
					'Grouping is only one layer of account management. The accounts behind each group also need consistent cloud environments, device settings, proxy assignments, and target-market context.',
					'Once the account pool reaches 100 or more, standardization determines whether the team is managing a batch of consistent assets or one hundred special cases.',
				],
			},
			{
				heading: 'The Real Warning Sign',
				paragraphs: [
					'The danger is not simply having no groups. It is having a grouping system that never changes after it is created.',
					'Clients change, account stages change, platform strategy changes, and the team’s most common tasks change. If the current groups can no longer select the right batch in one step, the grouping system should be updated instead of tolerated.',
				],
			},
			{
				heading: 'How Ainnc Supports Group Management',
				paragraphs: [
					'Ainnc supports custom account groups, bulk import, group adjustment, and group-based task selection inside the task center.',
					'When groups match the team’s real operating habits, bulk execution becomes much easier. The goal is not a tidy dashboard. The goal is making “select the right accounts” feel almost effortless.',
				],
			},
		],
	},
	'spreadsheets-break-50': {
		title: 'Why Spreadsheets Break After 50 Social Accounts',
		description:
			'The hidden cost of tracking accounts, logins, and content in sheets, plus what a living account record should contain.',
		category: 'Operations Playbook',
		tags: ['Spreadsheets', 'Account Operations', 'Operations Systems'],
		sections: [
			{
				paragraphs: [
					'Most social media teams start with spreadsheets. With a small account pool, that feels practical: username, password, platform, status, owner, and notes.',
					'The problem rarely appears with the first account. It appears once the account pool passes 50 and the spreadsheet stops being a system. It becomes a record that is always slightly out of date.',
				],
			},
			{
				heading: 'Where Spreadsheets Fail First',
				paragraphs: [
					'Status updates lag behind reality. Whether an account logged in, which device it used, which proxy was abnormal, and whether the latest task succeeded are all hard to keep fresh by hand.',
					'Context also becomes scattered. Credentials live in a sheet, assets live in a drive, task progress lives in chat, and error screenshots live on someone’s desktop.',
					'As the team grows, access control becomes another problem. A spreadsheet is not a safe place for everyone to copy full account details.',
				],
			},
			{
				heading: 'Accounts Need Living Records',
				paragraphs: [
					'A useful account record should show which device the account uses, which proxy is assigned, which tasks were executed, which assets were published, and what failed last time.',
					'When those events are captured automatically, the team no longer has to reconstruct the truth from memory and chat messages.',
				],
			},
			{
				heading: 'When to Move Beyond Sheets',
				paragraphs: [
					'Sheets can work for a few accounts. Once the workflow includes many operators, multiple platforms, proxies, devices, and repeated publishing tasks, account management needs to become an operating system.',
					'Ainnc turns accounts into operational objects that can be grouped, bound to devices, assigned resources, scheduled into tasks, and traced over time.',
				],
			},
		],
	},
	'real-social-ops-platform': {
		title: 'What a Real Social Media Operations Platform Should Look Like',
		description:
			'How teams move from scattered tools to one shared operating layer for accounts, assets, tasks, and data.',
		category: 'Operations Playbook',
		tags: ['Operations Platform', 'Team Workflow', 'Bulk Operations'],
		sections: [
			{
				paragraphs: [
					'Many teams think they already have a social media operations system because they use spreadsheets, cloud drives, proxy tools, browser environments, chat apps, and task boards.',
					'But having many tools is not the same as having one system. If the data does not connect, the team spends its day copying, checking, and explaining status.',
				],
			},
			{
				heading: 'A Platform Connects the Core Objects',
				paragraphs: [
					'The main objects in social operations are simple: accounts, devices, proxies, assets, tasks, and results.',
					'A real platform should let these objects reference each other. Accounts should know which device they run on. Tasks should know which assets they used. Results should flow back to the accounts and assets involved.',
				],
			},
			{
				heading: 'Teams Need One Shared View',
				paragraphs: [
					'Managers need to know which tasks succeeded, which accounts are abnormal, which assets have been used, and which clients need a review.',
					'Operators need to know what to do next and how to respond when a task fails. A shared operating view reduces repeated meetings and chat-based status checks.',
				],
			},
			{
				heading: 'Automation Is Only One Part',
				paragraphs: [
					'The larger value is stable records, clear ownership, traceable execution, and fast issue location.',
					'Ainnc gives teams a reliable layer where accounts, assets, and tasks are managed together instead of scattered across separate tools.',
				],
			},
		],
	},
	'task-center': {
		title: 'Task Center: Why One Button Should Not Do Everything',
		description:
			'How Ainnc turns login, publishing, warming, and profile updates into a traceable workflow for agencies, MCNs, and global teams running social accounts at scale.',
		category: 'Product Capabilities',
		tags: ['Task Center', 'Bulk Publishing', 'Account Operations', 'Product Capabilities'],
		sections: [
			{
				paragraphs: [
					'Many teams start by asking for one fully automatic button: choose the accounts, click once, and let the system handle the rest. The request sounds reasonable, especially when a team needs to manage many clients, hundreds of social accounts, and multiple publishing platforms every day.',
					'But in real operations, one black-box button often creates more confusion than efficiency. Social account work is not a single action. It includes login status, device environment, proxy IPs, asset selection, publishing parameters, account rhythm, failure reasons, and execution review.',
					'If every action is hidden inside one button, the team only sees success or failure. It cannot easily tell which account failed, which step failed, and what should be fixed first. This is why Ainnc separates work into task flows instead of hiding all complexity.',
				],
			},
			{
				heading: 'The Real Scenario: 80 Accounts Need to Publish Today',
				paragraphs: [
					'Imagine an agency team that needs to publish a batch of short videos for four clients. Each client has around 20 accounts across TikTok and Instagram. The operators have video assets, titles, tags, timing requirements, account lists, and client notes.',
					'In a traditional workflow, the team first filters accounts in a spreadsheet, checks login status, confirms devices, finds the right assets, assigns accounts to operators, publishes manually, takes screenshots, updates the sheet, and reports progress in chat.',
					'The time cost is not only the act of publishing. It is preparation before publishing, exceptions during publishing, and reporting after publishing. If 10 accounts fail, the team needs to know whether the cause is login, device binding, proxy status, missing assets, incomplete parameters, or platform restrictions.',
				],
			},
			{
				heading: 'Why One Large Button Is Not Enough',
				paragraphs: [
					'Ainnc separates bulk work into login, publishing, warming, and profile-update tasks because those actions fail in different ways and need different rhythms.',
					'If a login task fails, the account, device, or environment may need attention. If a publishing task fails, the issue may be the content, title, tags, or platform rule while the account itself remains healthy. If those actions are merged into one task, the team cannot quickly locate the failure.',
					'Publishing can happen in planned batches, but warming activity should be spread over time. Login checks should happen before publishing. Device binding and asset preparation should happen before task execution. Splitting the work makes the operating order visible.',
				],
			},
			{
				heading: 'The Problems the Task Center Solves',
				paragraphs: [
					'The Task Center gives operators a clear entry point for each type of work. Login tasks, publishing tasks, warming tasks, and profile-update tasks each have their own parameters and checks.',
					'It also helps teams filter risk before execution. Task cards can show key readiness signals such as device binding and account status so the team does not discover obvious failures only after launching a large batch.',
					'Most importantly, it connects accounts, devices, assets, and execution results. The task is not just an action. It becomes a record the team can inspect later.',
				],
			},
			{
				heading: 'Bulk Does Not Mean Copy and Paste',
				paragraphs: [
					'One of the easiest mistakes in bulk publishing is treating it as copy and paste. If 50 accounts publish the same video with the same title, tags, and cover, the result looks like one asset repeated 50 times instead of 50 accounts operating naturally.',
					'In real operations, the same asset can be reused, but the angle, tags, publishing time, and account grouping should vary. A North America account may use a direct product benefit, while a Southeast Asia account may use a more local scenario. A Reddit post may need a discussion-style title instead of a short-video hook.',
					'Ainnc keeps room for this variation in the parameter step. Bulk work should reduce repetitive manual effort, not make every account behave identically.',
				],
			},
			{
				heading: 'How Ainnc Handles It',
				paragraphs: [
					'Ainnc provides task layering, account selection, parameter configuration, readiness checks, and execution records inside one workflow.',
					'Operators can select accounts by group, platform, or status. They can configure assets, titles, tags, and other task parameters without relying on scattered spreadsheets. After execution, each task leaves a record with the batch, account, platform, device, status, and timing.',
					'This gives agencies, MCNs, and global teams a clearer way to answer operational questions: which accounts succeeded, which accounts failed, which platform produced the most issues, and what needs to be fixed before the next batch.',
				],
			},
			{
				heading: 'A Better Way to Run a Publishing Batch',
				paragraphs: [
					'A more reliable workflow starts by grouping accounts by client, market, platform, or project. Then the team checks device binding and account readiness before execution.',
					'Next, the team uploads assets into the file module, chooses the right publishing task, selects accounts, fills task parameters, and confirms the batch. After publishing, operators review results in the task list and pull failed accounts into a separate cleanup flow.',
					'In this setup, the Task Center is not only a place to start work. It becomes the operating layer that connects preparation, execution, and review.',
				],
			},
			{
				heading: 'Fewer Buttons Does Not Always Mean Simpler Operations',
				paragraphs: [
					'For five accounts, one large button may feel enough. For 50, 100, or more accounts, teams need visibility more than they need a hidden shortcut.',
					'The real goal is not to blindly trust automation. It is to make automation controllable, traceable, and reviewable. That is the role of Ainnc’s Task Center.',
				],
			},
		],
	},
	'mcn-prove-value-with-data': {
		title: 'How MCN Agencies Prove Value to Clients With Data',
		description:
			'Turning execution records into review-ready reports is one of the most underrated renewal tools for agency teams.',
		category: 'Operations Playbook',
		tags: ['MCN', 'Agency Operations', 'Client Reporting'],
		sections: [
			{
				paragraphs: [
					'For agency teams, the hardest part is not always doing the work. It is making the client clearly see what was done.',
					'Teams log in, organize assets, publish content, fix abnormal accounts, and follow up on results every day. But if the monthly review is only a few screenshots and a hand-built sheet, clients may not feel the value behind the work.',
				],
			},
			{
				heading: 'What Clients Actually Want to Know',
				paragraphs: [
					'Clients care about more than how many posts were published. They want to know whether accounts are healthy, whether publishing happened on schedule, whether issues were found in time, and whether the team can keep delivering at a larger scale.',
					'Those answers need execution data, not only verbal updates.',
				],
			},
			{
				heading: 'Turn Operations Into Review Assets',
				paragraphs: [
					'Every login task, publishing task, asset upload, and issue fix should leave a record.',
					'An agency can report on account pool status, task completion rate, failure reasons, asset usage, publishing rhythm, and abnormal account handling.',
				],
			},
			{
				heading: 'Data Makes Renewals Easier',
				paragraphs: [
					'Renewals are built before the renewal conversation. Each stable task and each resolved issue adds trust.',
					'Ainnc helps teams keep accounts, assets, tasks, and execution results in one workflow, turning internal operations into client-facing proof.',
				],
			},
		],
	},
	'cloud-phone-vs-browser': {
		title: 'Cloud Phones vs. Browsers: Which Is Safer for Accounts?',
		description:
			'Browser fingerprinting and cloud-phone isolation solve different problems. The right choice depends on account scale.',
		category: 'Product Capabilities',
		tags: ['Cloud Phones', 'Browser Fingerprints', 'Account Safety'],
		sections: [
			{
				paragraphs: [
					'Social account operators often ask whether they should use browser environments or cloud phones.',
					'The answer depends on the type of task and the risk layer you need to control. These two approaches are not interchangeable.',
				],
			},
			{
				heading: 'Browsers Are Better for Lightweight Work',
				paragraphs: [
					'Browser environments are fast to launch and useful for web-based management, login checks, and light operations.',
					'They mainly address session and fingerprint separation. They do not fully reproduce a mobile app environment.',
				],
			},
			{
				heading: 'Cloud Phones Are Closer to Real Devices',
				paragraphs: [
					'Cloud phones provide device-level isolation. Each account can run inside a more independent mobile environment, which is useful for app login, warming, publishing, and long-term account work.',
					'As the account pool grows, device relationships, proxy relationships, and task history become critical.',
				],
			},
			{
				heading: 'Choose Based on Scale and Task Type',
				paragraphs: [
					'For a few accounts and mostly web-based work, browsers may be enough. For multi-account, multi-platform, long-term mobile operations, cloud phones are usually a stronger foundation.',
					'Ainnc focuses on managing accounts, devices, proxies, and tasks together, because account safety comes from the whole operating environment.',
				],
			},
		],
	},
	'proxy-ip-types': {
		title: 'Static, Dynamic, and Mobile IPs: How to Choose a Proxy',
		description:
			'There is no single best proxy type. The right setup depends on account volume, market coverage, and risk tolerance.',
		category: 'Product Capabilities',
		tags: ['Proxy IP', 'Static IP', 'Mobile IP'],
		sections: [
			{
				paragraphs: [
					'Proxy IPs are often treated as a basic access tool, but for social account operations they are infrastructure.',
					'The long-term risk depends on IP type, location, reuse rules, and how clearly proxies are mapped to accounts and devices.',
				],
			},
			{
				heading: 'Static IPs Support Stable Account Relationships',
				paragraphs: [
					'Static IPs are useful when an account needs a consistent access environment. This is often better for long-term accounts and client-owned accounts.',
					'The risk is concentration: a low-quality IP or excessive sharing can affect multiple accounts.',
				],
			},
			{
				heading: 'Dynamic IPs Support Flexible Scheduling',
				paragraphs: [
					'Dynamic IPs are useful for testing, coverage, and flexible task allocation. But frequent changes in location and network pattern can also look abnormal.',
					'Dynamic does not mean random. It still needs operating rules.',
				],
			},
			{
				heading: 'Mobile IPs Fit Some Mobile-First Scenarios',
				paragraphs: [
					'Mobile IPs can be closer to real mobile traffic and may fit higher-risk mobile scenarios, but they often cost more and need stricter allocation.',
					'Ainnc treats proxies as trackable resources that can be assigned, checked, and connected to account and task records.',
				],
			},
		],
	},
	'one-workflow-five-tools': {
		title: 'From Content Creation to Publishing: One Workflow Instead of Five Tools',
		description:
			'A practical look at how one content asset moves from idea to publication across four platforms with less handoff friction.',
		category: 'Product Capabilities',
		tags: ['Content Workflow', 'Asset Management', 'Bulk Publishing'],
		sections: [
			{
				paragraphs: [
					'Content operations rarely fail because teams cannot create content. They fail because content has to pass through too many disconnected steps before it is published.',
					'A video may move from an editing tool to a drive, then into a spreadsheet, then to an operator, then into each platform manually.',
				],
			},
			{
				heading: 'More Tools Mean More Handoffs',
				paragraphs: [
					'Storage tools, account sheets, task chats, and publishing environments all have value. But when they do not share records, the team repeats the same questions: is this the final asset, which account should publish it, and did the task succeed?',
				],
			},
			{
				heading: 'A Workflow Should Cover the Full Path',
				paragraphs: [
					'A better flow starts with a shared asset library. Operators can select assets directly in task parameters, run publishing batches, and review results from the same workflow.',
					'Assets, accounts, and task results stay connected.',
				],
			},
			{
				heading: 'Less Handoff Means Fewer Errors',
				paragraphs: [
					'Many mistakes come from handoffs: wrong file versions, wrong accounts, missed platforms, and failures no one noticed.',
					'Ainnc connects content assets, account resources, and task execution so teams spend less time copying information and more time improving operations.',
				],
			},
		],
	},
	'tiktok-risk-guide': {
		title: 'How to Avoid Common Risk-Control Issues in Bulk TikTok Operations',
		description:
			'Account safety comes down to believable independence, natural operating rhythm, and a baseline of content originality.',
		category: 'Platform Guides',
		tags: ['TikTok', 'Risk Control', 'Account Safety'],
		sections: [
			{
				paragraphs: [
					'The biggest risk in bulk TikTok operations is not one account failing. It is a pattern that affects the whole account pool.',
					'A shared device, shared IP, or repeated behavior pattern can make many accounts unstable at the same time.',
				],
			},
			{
				heading: 'Keep Environments Independent',
				paragraphs: [
					'Accounts should avoid sharing too much environment context. Devices, proxy IPs, login habits, and usage patterns should be managed carefully.',
					'Long-term accounts are usually safer with more consistent device and proxy relationships.',
				],
			},
			{
				heading: 'Control the Operating Rhythm',
				paragraphs: [
					'Bulk operations should not mean every account does the same thing at the same time.',
					'Split tasks into batches, vary time windows, and avoid highly repetitive behavior across the account pool.',
				],
			},
			{
				heading: 'Avoid Over-Repeated Content',
				paragraphs: [
					'Even with good environment isolation, repeated content can reduce distribution and increase risk.',
					'Ainnc helps teams manage accounts, assets, devices, and tasks, but stable TikTok operations also need thoughtful content planning and execution rhythm.',
				],
			},
		],
	},
	'global-brand-scale': {
		title: 'Building Scalable Social Operations for Global Brands',
		description:
			'The common localization traps brands face when entering new markets, and the four layers scalable operations require.',
		category: 'Global Growth',
		tags: ['Global Brands', 'Global Growth', 'Localization'],
		sections: [
			{
				paragraphs: [
					'When a global brand enters a new market, social media operations are more complex than translating headquarters content.',
					'Accounts, content, publishing rhythm, and team collaboration all need to fit the local market.',
				],
			},
			{
				heading: 'Layer One: Account Infrastructure',
				paragraphs: [
					'Each market may need its own accounts, device environments, proxy strategy, and access rules.',
					'If ownership and device relationships are unclear early, scaling later becomes difficult.',
				],
			},
			{
				heading: 'Layer Two: Content Asset Management',
				paragraphs: [
					'Global brands often use headquarters assets, local assets, campaign assets, and test assets at the same time.',
					'Assets should be organized by market, platform, theme, and cycle so local teams can reuse them safely.',
				],
			},
			{
				heading: 'Layer Three and Four: Execution and Learning',
				paragraphs: [
					'Localized publishing depends on local holidays, active hours, platform habits, and review risk. Tasks need batch management, status tracking, and issue review.',
					'Ainnc helps brands manage accounts, assets, and tasks in one framework so local operations become repeatable instead of improvised.',
				],
			},
		],
	},
	'localization-how-deep': {
		title: 'How Deep Should Localization Go for Global Social Media?',
		description:
			'Translation helps audiences understand you. Localization makes them want to keep watching. Those are different jobs.',
		category: 'Global Growth',
		tags: ['Localization', 'Global Brands', 'Social Content'],
		sections: [
			{
				paragraphs: [
					'Many global teams treat localization as translation. Translation matters, but in social media it is only the first layer.',
					'Real localization adapts to local language habits, platform culture, buying psychology, and interaction style.',
				],
			},
			{
				heading: 'Language Is Only the First Layer',
				paragraphs: [
					'Translating copy helps people understand the message. It does not guarantee they will stop, watch, comment, or share.',
					'The same product benefit may need a direct functional angle in one market and a trust-building scenario in another.',
				],
			},
			{
				heading: 'Platform Habits Need Localization Too',
				paragraphs: [
					'TikTok, Instagram, Reddit, and X have different content cultures. A video hook that works on TikTok may feel unnatural on Reddit.',
					'Localization means adapting the format, not only the words.',
				],
			},
			{
				heading: 'Execution Should Match the Market',
				paragraphs: [
					'Publishing time, account persona, interaction rhythm, asset selection, and comment handling all need local context.',
					'Ainnc helps teams group accounts, assets, and tasks by market so localization can become a repeatable operating process.',
				],
			},
		],
	},
	'scaling-social-account-operations': {
		title: 'How Agencies Manage Hundreds of Social Accounts Without Losing Control',
		description:
			'Most agency teams hit the same wall between 20 and 50 accounts. Here is where things break and what a real operations system should look like.',
		category: 'Operations Playbook',
		tags: ['Scale', 'Social Accounts', 'Agencies', 'MCN', 'Global Brands'],
		sections: [
			{
				paragraphs: [
					'If you run a social media agency, MCN, or global brand team, the hard part is rarely publishing one post. The hard part is keeping hundreds or thousands of accounts logged in, healthy, traceable, and publishing consistently across TikTok, Instagram, Reddit, and X.',
					'When a team manages only a small number of accounts, spreadsheets, reminders, and spare devices can work for a while. Once the account pool reaches 50, 100, or more, the old workflow starts to break: logins get messy, devices and IPs overlap, assets are hard to find, tasks are missed, and abnormal accounts are discovered too late.',
				],
			},
			{
				heading: 'Where Operations Start to Break',
				paragraphs: [
					'Many teams begin with spreadsheets for usernames, passwords, platforms, and client ownership.',
					'They use multiple phones or browser environments to separate accounts, manually purchase and rotate proxy IPs, store creative assets in local folders, and track progress through chat messages or shared sheets.',
					'This can work for 10 accounts. At 50 accounts, maintaining the system itself becomes a job. At 100 or more, it becomes a risk to account safety, delivery stability, and team collaboration.',
				],
			},
			{
				heading: 'What a Real Operations System Needs',
				paragraphs: [
					'Each account needs an isolated operating environment so one account does not easily affect the rest of the pool.',
					'Proxy IPs should be centrally managed and assigned to accounts, devices, and tasks instead of being copied from another tool by hand.',
					'Assets should live in a shared file library so videos, images, copy, and task parameters can be reused.',
					'Repetitive actions such as login, warming, publishing, and status checks should become batch tasks that can be tracked from one dashboard.',
				],
			},
			{
				heading: 'Predictability Matters More Than Time Savings',
				paragraphs: [
					'Automation is often described as a time-saving story. For agencies, MCNs, and global teams, the larger value is predictability.',
					'Clients are not only paying someone to post content. They are paying for stable execution: active accounts, scheduled publishing, timely issue detection, and a team that can keep delivering as the account count grows.',
				],
			},
			{
				heading: 'How Ainnc Fits In',
				paragraphs: [
					'Ainnc brings social accounts, cloud environments, proxy IPs, content assets, bulk publishing, and execution results into one workflow.',
					'Teams can import and group accounts, bind devices, configure proxies, upload assets, and use the task center to run login, warming, and publishing workflows across TikTok, Instagram, Reddit, X, and other platforms.',
				],
			},
		],
	},
} as const;

export function isEnglishPath(pathname: string) {
	return pathname === '/en' || pathname.startsWith('/en/');
}

export function localizedPath(pathname: string, locale: Locale) {
	const cleanPath = pathname.endsWith('/') && pathname !== '/' ? pathname.slice(0, -1) : pathname;
	const withoutEnglish = isEnglishPath(cleanPath) ? cleanPath.replace(/^\/en/, '') || '/' : cleanPath;

	if (locale === 'zh') {
		return withoutEnglish === '/' ? '/' : `${withoutEnglish}/`;
	}

	return withoutEnglish === '/' ? '/en/' : `/en${withoutEnglish}/`;
}

export function getPostMeta(post: CollectionEntry<'blog'>, locale: Locale) {
	if (locale === 'en') {
		const english = EN_POSTS[post.id as keyof typeof EN_POSTS];
		if (english) {
			return {
				title: english.title,
				description: english.description,
				category: english.category,
				tags: [...english.tags],
			};
		}
	}

	return {
		title: post.data.title,
		description: post.data.description,
		category: post.data.category,
		tags: post.data.tags,
	};
}

export function getEnglishSections(postId: string) {
	return EN_POSTS[postId as keyof typeof EN_POSTS]?.sections ?? [];
}
