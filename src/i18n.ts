import type { CollectionEntry } from 'astro:content';

export type Locale = 'zh' | 'en';

export const SITE_COPY = {
	zh: {
		title: 'Ainnc 麦芽营销博客',
		description: '分享 Ainnc 麦芽营销的产品更新、社媒账号运营、素材管理和批量任务发布实践。',
		home: '首页',
		blog: '博客',
		about: '关于',
		officialSite: '进入官网',
		telegram: '加入 Telegram',
	},
	en: {
		title: 'Ainnc Blog',
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
