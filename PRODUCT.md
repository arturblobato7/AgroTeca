# Product

## Register

product

## Users

**Primary:** Members of the rural Quilombola community of Jutaiteua (Pará, Brazilian Amazon). Mixed ages, including a meaningful share of elderly residents and people with varied literacy. They access the site on a range of devices, often older Android phones over slow connections, sometimes reading the screen aloud together in groups.

**Secondary:** Curators and educators within the community who approve submitted knowledge before it becomes public, and occasional external visitors (extension workers, students, researchers) who consult the archive.

**Context of use:** A site visit is rarely solitary or hurried. Someone is reading to a parent. A teacher is showing students the technique for preparing soil. A grandmother is dictating a recipe while a grandchild types it in. The interface must hold up under that kind of attention, in good light or bad, on a 5-inch screen or a community-center tablet.

## Product Purpose

AgroTeca is a living archive of community knowledge: planting techniques, harvests, traditional recipes, oral histories, and care for the land. Anyone in the community can submit knowledge; curators review and approve before publishing; everyone can browse the resulting catalog of texts, audio, video, and printable booklets.

Success has three equal dimensions:
1. **Submission** — community members actually contribute their knowledge (the Enviar flow must feel welcoming, not bureaucratic).
2. **Curation** — moderators can process, edit, and approve submissions efficiently (the admin flow must be fast and accurate).
3. **Browsing** — the resulting archive becomes a daily reference (technique pages, videos, cartilhas, and community info must reward repeated visits).

The project is non-commercial, accessibility-first, and rooted in the dignity of traditional knowledge transmission.

## Brand Personality

Educational, welcoming, encouraging: the interface should feel like a generous teacher who values what the learner already knows. Three words: **patient · communal · grounded**.

- *Patient* — pages take their time. Nothing rushes the reader. Type is generous, language is plain, decisions are reversible.
- *Communal* — the design honors contribution. Author names are visible. Curator review is presented as care, not gatekeeping. Tone is "nós" (we), not "o usuário" (the user).
- *Grounded* — references print culture and field manuals more than apps. Numerals, hairline rules, italic eyebrows, a quiet paper surface. Confident, never flashy.

**Voice:** Plain Brazilian Portuguese, short sentences, active verbs, no jargon. Names like "Cartilhas" and "Acervo" are kept because they belong to the audience. Avoid corporate Portuguese ("usuário", "plataforma", "experiência"), prefer concrete words ("morador", "site", "uso").

## Anti-references

The interface must explicitly NOT feel like a **government or institutional portal** (the gov.br aesthetic): cold blue masthead bars, dense bureaucratic forms, "Acesso à informação" rails, banner stacks, microcopy that sounds like a circular. AgroTeca is community-owned, not state-owned, and that distinction should be felt on first glance.

Also avoid:
- Generic SaaS dashboards (gradient cards, hero-metric tiles, friendly-sans-everywhere).
- Childish/cartoon illustrations of "farmers" or "rural life" that condescend to the audience.
- Trendy decoration (animated backgrounds, glassmorphism, glowing CTAs) that signals "this is a tech product" louder than the content.

The reference register is closer to a community-archive publication, a field manual, or a local cooperative's printed bulletin than to any digital category.

## Design Principles

1. **Honor the contributor.** Author names, dates, and provenance are first-class content, not metadata footnotes. The site exists because someone shared something.
2. **Plain over polished.** When a typographic choice and a decorative choice both work, take the typographic one. Confident silence beats decorated noise.
3. **Reachable from a feature phone, dignified on a desktop.** Performance budgets and touch sizing assume the harder context first; the desktop view inherits the benefits.
4. **Curation visible, not hidden.** The review pipeline is shown to contributors as a sign of care ("um curador aprova antes da publicação"), not concealed as friction. The admin tools mirror that care: fast, specific, never destructive without a confirmation.
5. **Never rush the reader.** No autoplay, no countdown banners, no skeleton flicker, no animated decoration. Motion only when it clarifies (a row highlights on hover, a confirm step arms inline).

## Accessibility & Inclusion

**Target:** WCAG 2.1 AA across all surfaces, with practical bias toward AAA where it costs little (contrast on body text, focus visibility, motion sensitivity).

**Concrete commitments shaped by this audience:**

- **Older users with declining eyesight.** Body type at 17px minimum (`--type-md`), fluid scale via `clamp()`. Body text contrast at or above 5:1, never below WCAG AA 4.5:1. Focus rings 3px and high-contrast (brand orange), never relying on subtle color shifts.
- **Lower literacy / read-aloud groups.** Plain Brazilian Portuguese, short labels ("Enviar", "Voltar", "Salvar"), one idea per sentence in helper text. Form fields say what they want in concrete examples ("Ex: Dona Maria, Seu José"). Error messages name what to fix, not error codes.
- **Low-bandwidth and older devices.** First paint under reasonable budgets on slow 3G: lightweight CSS, no heavy JS frameworks, fonts narrowed to needed axes, FontAwesome async-loaded. Functional without JavaScript (forms post and reload; JS adds the inline-confirm progressive enhancement).
- **Keyboard and screen-reader users.** Skip-link to `#main`. Every form input associated with its label. All icon-only buttons have `aria-label`. Decorative icons `aria-hidden`. Per-page `<title>`. Two-step destructive actions confirm inline (not in modals), with `Escape` and click-outside disarming.
- **Reduced-motion + forced-colors.** Honor both system preferences explicitly in CSS.

The brand colors (blue + warm orange) are part of AgroTeca's identity and will not change; downstream design work treats them as fixed inputs and ensures contrast/usage stays within these accessibility commitments.
