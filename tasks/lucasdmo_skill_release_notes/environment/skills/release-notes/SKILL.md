# Release notes

Create the customer-facing release notes from `/app/release_data.json` and save
them as `/app/RELEASE_NOTES.md`. Do not edit `release_data.json` or create any
other files.

The output must use this exact layout:

```markdown
# <product> <version>

## Added
- [#<issue>] <summary>

## Changed
- [#<issue>] <summary>

## Fixed
- [#<issue>] <summary>
```

Use the `product` and `version` values from the JSON heading. Include only
changes whose `customer_visible` value is `true`. Create sections in this fixed
order: `Added`, `Changed`, then `Fixed`; omit a section when it has no included
changes. Within each section, order entries by ascending numeric `issue`.

Each bullet must use the issue number and summary from its change object exactly
as shown above. Put one blank line between the heading, sections, and bullets'
next section. The file must end with exactly one newline.
