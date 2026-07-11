import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const blog = defineCollection({
	// Load Markdown and MDX files in the `src/content/blog/` directory.
	loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
	// Type-check frontmatter using a schema
	schema: ({ image }) =>
		z.object({
			title: z.string(),
			description: z.string(),
			author: z.string().optional(),
			pubDate: z.coerce.date(),
			updatedDate: z.coerce.date().optional(),
			category: z.string(),
			tags: z.array(z.string()).default([]),
			tldr: z.array(z.string()).default([]),
			faqIntent: z.string().min(12).optional(),
			faq: z
				.array(
					z.object({
						question: z.string(),
						answer: z.string(),
					}),
				)
				.default([]),
			featured: z.boolean().default(false),
			draft: z.boolean().default(false),
			heroImage: z.optional(image()),
		}),
});

export const collections = { blog };
