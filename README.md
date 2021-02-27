DSPods
===


DSPods is an Open Source collection of podcasts about Data Science. The [website](https://dspods.netlify.app/) just adds a few bells and whistles around this podcasts list to make it easy for perusal. What are those bells and whistles?

1. Find all Data Science podcasts here. No need to trawl search engine results and blog posts.
2. The list is community created and curated, thus has a good signal-to-noise ratio.
3. Easily find the active podcasts; avoid the heartbreak when you realise that the podcast you liked so much is no longer releasing any new episodes.
4. Since the details of the podcasts are updated daily, it's never static.


When I first started listening to podcasts and wanted to find a few on Data Science I looked up on Google. Google gave me many blog posts recommending the podcasts. I subscribed to a few, removed a few which I didn't like, and added some more later from other blogs. This whole process took time and various iterations to come to a set of podcasts I listen to now. The static information of the podcast meant that I also had to check the podcasts which were no longer active.

The considered definition of Data Science is pretty loose: it can be about technology, programming languages, data engineering, AI, ML, DL, ethics and philosophy in AI, visualization, research around the AI and Data Science fields. The idea behind keeping the definition of Data Science broad is because a person might only be interested in a subset of the topics. **My hope is to create a single place to discover all such podcasts instead of searching and going through various blog posts.**


## Podcasts

List of podcasts are in [podcasts.md](podcasts.md).


## Technical Details

- The website is built using [Jekyll](https://jekyllrb.com) static website generator.
- The website is designed with [Bootstrap](https://getbootstrap.com/). The [Mediumish Jekyll Theme](https://www.wowthemes.net/mediumish-free-jekyll-template/) was modified significantly for the current design, but it was the starting point.
- GitHub actions
- Hosted using [Netlify](https://www.netlify.com/).


## Contribute

You can contribute in multiple ways:

- If you're a host of a Data Science podcast, please consider adding your podcast here.
- If you listen to a podcast not mentioned here, please consider adding that podcast here. It'll help others discover that podcast and give the podcast creators much needed promotion.
- If you (host, or a listener) think that some information about a podcast is wrong, then you can help too.
- If you have any suggestion then I'd like to hear about it as well.

You can provide help in two ways:

1. Raise an issue [here](https://github.com/TrigonaMinima/dspods/issues/new). Select the "New Podcast" issue template and just fill the details asked there
2. Make the change or add a new file and submit a pull request. Each podcast is represented as a markdown file inside [`_posts`](_posts) directory with a yaml front matter. Jekyll uses this file to build the final website. Here is a checklist to be followed:

    - Git pull (and rebase) to pull in the new changes before you push your commits and a PR.
    - Add title.
    - Add categories you think best describe the podcast.
    - Add description.
    - Add podcast image with at least 600x600 pixels (preferably `webp` format). Reduce the size of the image using the [tinypng.com](https://tinypng.com/). All the podcast images are present in the [`/assets/images/pods`](/assets/images/pods)
    - Add podcast website URL.
    - Add RSS feed link.
    - Add one or more of Pocketcasts, Spotify, Apple Podcasts (don't use iTunes URL), YouTube.
    - Add the podcast entry in the [./podcasts.md](https://github.com/TrigonaMinima/dspods/blob/gh-pages/podcasts.md).
    - Commit message is as follows: `Add: New podcast - <podcast_name>`.
    - Keep everything related to a podcast within a single commit.
