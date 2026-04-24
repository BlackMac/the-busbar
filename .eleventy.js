const rssPlugin = require("@11ty/eleventy-plugin-rss");

module.exports = function (eleventyConfig) {
  eleventyConfig.addPlugin(rssPlugin);

  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy({ "CNAME": "CNAME" });
  // about.html is now src/about.njk — processed through Eleventy for correct path rewriting

  eleventyConfig.addCollection("editions", (api) =>
    api.getFilteredByGlob("src/editions/*.md")
       .sort((a, b) => b.date - a.date)
  );

  eleventyConfig.addFilter("englishDate", (dateVal) => {
    const months = ["January","February","March","April","May","June",
                    "July","August","September","October","November","December"];
    const d = dateVal instanceof Date ? dateVal : new Date(dateVal);
    return `${months[d.getUTCMonth()]} ${d.getUTCDate()}, ${d.getUTCFullYear()}`;
  });

  eleventyConfig.addFilter("isoDate", (dateVal) => {
    const d = dateVal instanceof Date ? dateVal : new Date(dateVal);
    return d.toISOString().slice(0, 10);
  });

  eleventyConfig.addFilter("englishMonth", (dateVal) => {
    const months = ["January","February","March","April","May","June",
                    "July","August","September","October","November","December"];
    const d = dateVal instanceof Date ? dateVal : new Date(dateVal);
    return `${months[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
  });

  // Amazon affiliate links via VoltPlan's /api/go redirect.
  // OneLink + tag rewrite happens on voltplan.app at click time.
  const AFFILIATE_GO_BASE = "https://voltplan.app/api/go";
  const buildGoUrl = (params, sourceSuffix) => {
    const source = sourceSuffix ? `busbar_${sourceSuffix}` : "busbar";
    const search = new URLSearchParams({ ...params, source });
    return `${AFFILIATE_GO_BASE}?${search.toString()}`;
  };
  eleventyConfig.addFilter("amazonGo", (query, sourceSuffix) =>
    query ? buildGoUrl({ q: query }, sourceSuffix) : null
  );
  eleventyConfig.addFilter("amazonGoId", (productId, sourceSuffix) =>
    productId ? buildGoUrl({ p: productId }, sourceSuffix) : null
  );

  eleventyConfig.setNunjucksEnvironmentOptions({
    autoescape: true,
    throwOnUndefined: false,
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
    templateFormats: ["njk", "md", "html"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    pathPrefix: "/",
  };
};
