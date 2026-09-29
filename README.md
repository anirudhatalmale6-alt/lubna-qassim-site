# lubnaqassim.com — draft design

Working draft of the personal website for Lubna Qassim — international lawyer, senior
policy leader and former senior diplomat.

**Draft:** https://anirudhatalmale6-alt.github.io/lubna-qassim-site/

Every page carries `noindex`, so nothing here appears in search results. This is a design
for review, not a publication.

## The positioning

The site is built around one idea rather than a list of posts: she has sat on **all four
sides of the same table** — private practice, the legislator's chair, the boardroom and
the diplomatic table — and the same questions look entirely different from each one.
The brief was explicit that it must not read as a CV.

## Pages

| Page | What it does |
| --- | --- |
| `index.html` | Name, strapline, the four chairs, three doors, recognition strip |
| `profile.html` | Three movements rather than a chronology, plus "at a glance" |
| `contribution.html` | Four areas of contribution — not a menu of services |
| `speaking.html` | Six themes and the formats line |
| `writing.html` | Two books, six essays, selected press |
| `essays/*.html` | Her own essays, republished in full |
| `recognition.html` | Six recognitions, dated |
| `mentorship.html` | One-to-one sessions; proceeds support girls' education |
| `gallery.html` | Selected photographs with a lightbox |
| `contact.html` | Enquiries |

## Build

    python3 tools/prep_images.py     # source photographs → docs/img
    python3 tools/build_site.py      # content → docs/*.html

Pages are generated from one script so the chrome stays identical across all of them and
a design revision is one edit rather than ten. The final build is WordPress with a
bespoke theme; this is the design prototype.

## Notes

- No framework and no build step in the browser: one stylesheet, one small script.
- Content lives in the HTML, so every page renders complete with JavaScript disabled.
  The reveal animation is gated on `html.js` and can never hide content.
- `prefers-reduced-motion` is respected.
- Essays are republished from the author's own blog, each credited to the publication
  that first carried it.
