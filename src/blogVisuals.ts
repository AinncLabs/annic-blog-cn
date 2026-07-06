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
};

const TONE_PREFIXES: Record<string, string> = {
	ops: 'OPS',
	product: 'PRD',
	platform: 'PLT',
	insights: 'GLB',
	default: 'SYS',
};

export function getCategoryTone(category: string) {
	return CATEGORY_TONES[category] ?? 'default';
}

export function getPostCode(category: string, index = 0) {
	const tone = getCategoryTone(category);
	const number = String(index + 1).padStart(2, '0');
	return `${TONE_PREFIXES[tone]}-${number}`;
}
