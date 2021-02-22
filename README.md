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

1. Raise an issue [here](https://github.com/TrigonaMinima/dspods/issues/new) with as many of the following the details as possible about the podcast:
    - Title
    - Official website of the podcast
    - RSS feed of the podcast
    - Pocketcasts link
    - Spotify link
    - Apple podcast link
    - YouTube
2. Make the change or add a new file and submit a pull request. Each podcast is represented as a markdown file inside [`_posts`](_posts) directory with a yaml front matter with the Jekyll then uses to build the final website. The fields which you need to provide are: `title`, `categories`, `image`, `description`, `podurl`, `rss`, `pocketcasts`, `spotify`, `apple_pod`, and `youtube`. All the podcast images are present in the [`/assets/images/pods`](/assets/images/pods). Try to keep the resolution `1000 x 1000` pixels.
3. Add the podcast in the [podcasts.md](podcasts.md).
