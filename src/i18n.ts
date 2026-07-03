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
	'scaling-social-account-operations': {
		title: 'Practical Methods for Scaling Social Account Operations',
		description:
			'For agencies, MCNs, and global brands managing hundreds or thousands of accounts across TikTok, Instagram, Reddit, and X.',
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
