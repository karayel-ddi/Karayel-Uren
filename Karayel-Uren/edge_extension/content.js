function scrapeTweets() {
    const tweets = document.querySelectorAll('div[data-testid="tweetText"]');
    const tweetTexts = Array.from(tweets).map(tweet => tweet.innerText);
    console.log(tweetTexts);
    alert("Scraped Tweets: \n" + tweetTexts.join("\n\n"));

    fetch('http://127.0.0.1:5000/post_tweets', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ tweets: tweetTexts })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
