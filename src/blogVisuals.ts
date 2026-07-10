const CATEGORY_TONES: Record<string, string> = {
	'运营方法论': 'ops',
	'操作教程': 'ops',
	'运营实践': 'ops',
	'Operations Playbook': 'ops',
	Tutorials: 'ops',
	Operations: 'ops',
	'产品能力解读': 'product',
	'产品更新': 'product',
	'Product Capabilities': 'product',
	'Product Updates': 'product',
	'平台专题': 'platform',
	'Platform Guides': 'platform',
	'出海观察': 'insights',
	'Global Growth': 'insights',
	'内容策略': 'insights',
	'Content Strategy': 'insights',
	'数据与增长': 'product',
	'Data & Growth': 'product',
	'团队协作': 'ops',
	'Team Collaboration': 'ops',
	'商业与交付': 'ops',
	'Business & Delivery': 'ops',
};

const TONE_PREFIXES: Record<string, string> = {
	ops: 'OPS',
	product: 'PRODUCT',
	platform: 'PLATFORM',
	insights: 'INSIGHTS',
	default: 'SYS',
};

const CATEGORY_PREFIXES: Record<string, string> = {
	'内容策略': 'CONTENT',
	'Content Strategy': 'CONTENT',
	'数据与增长': 'DATA',
	'Data & Growth': 'DATA',
	'团队协作': 'TEAM',
	'Team Collaboration': 'TEAM',
	'商业与交付': 'BIZ',
	'Business & Delivery': 'BIZ',
};

export function getCategoryTone(category: string) {
	return CATEGORY_TONES[category] ?? 'default';
}

export function getPostCode(category: string, index = 0) {
	const tone = getCategoryTone(category);
	const number = String(index + 1).padStart(2, '0');
	return `${CATEGORY_PREFIXES[category] ?? TONE_PREFIXES[tone]}-${number}`;
}
