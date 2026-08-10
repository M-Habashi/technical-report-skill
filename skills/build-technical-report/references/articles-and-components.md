# Articles and components

## Registry

`data/report-config.json` is the single article registry:

```json
{
  "brand": "Dynamics Lab",
  "title": "Actuator–specimen study",
  "accent": "#39BF5E",
  "articles": [
    {
      "id": "article-1",
      "label": "Evidence report",
      "summary": "Measured behavior, figures, and conclusions.",
      "component": "components/article-overview.html"
    }
  ]
}
```

The shell builds the drawer from this array and loads every component. Do not duplicate this registry in JavaScript or HTML.

## Article contract

Every component must use:

```html
<article class="report-article" id="article-1" data-article="article-1" hidden>
  <div class="report-intro">...</div>
  <div class="report-layout">
    <aside class="toc-rail">...</aside>
    <main>...</main>
  </div>
</article>
```

The first article may omit `hidden`; the shell normalizes visibility after loading.

Section links must target globally unique ids:

```html
<a href="#overview-results"><span class="nav-index">02</span><span>Results</span></a>
...
<section id="overview-results">...</section>
```

Prefix ids with an article-specific word. Never reuse `results`, `method`, or `conclusion` across multiple articles.

## Direct hashes

The shell accepts:

- `#article-2` to open an article;
- a section hash such as `#method-model` to open the owning article and scroll to that section.

`app-shell.js` discovers ownership from the section element after all components load. No prefix table is required.

## Safe extension pattern

To add an article:

1. Duplicate the component closest to the desired structure.
2. Assign the next stable article id.
3. Prefix every section id uniquely.
4. Add one registry entry.
5. During the report's first build, validate and test direct hashes. For later article additions, skip verification unless the user explicitly requests it.

To remove an article, delete its registry entry first, then its component. Do not leave dead components in the template.

## Separation of concerns

- Component HTML owns semantics and article-local navigation.
- `report-config.json` owns metadata and article order.
- `app-shell.js` owns shell navigation, progress, printing, reveal states, and active section tracking.
- Plot modules own only their plot containers.
- CSS owns all visual values. Avoid inline styles except root theme tokens derived from configuration.

