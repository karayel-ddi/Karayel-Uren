document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('scrape-tweets').addEventListener('click', () => {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            chrome.runtime.sendMessage({ action: 'scrapeTweets', tabId: tabs[0].id }, (response) => {
                if (response && response.status) {
                    console.log(response.status);
                    fetchTweets();
                } else {
                    console.error('No response or response.status is undefined');
                }
            });
        });
    });

    fetchTweets();
});

function fetchTweets() {
    fetch('http://127.0.0.1:5000/get_tweets')
        .then(response => response.json())
        .then(data => {
            const tweetsDiv = document.getElementById('tweets');
            tweetsDiv.innerHTML = '';
            data.tweets.forEach((tweet, index) => {
                const tweetElement = document.createElement('div');
                tweetElement.textContent = `${index + 1}: ${tweet}`;
                tweetsDiv.appendChild(tweetElement);
            });
        })
        .catch((error) => {
            console.error('Error fetching tweets:', error);
        });
}
