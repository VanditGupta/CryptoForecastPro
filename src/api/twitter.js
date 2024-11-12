// Import required modules
import { Rettiwt } from 'rettiwt-api';
import dotenv from 'dotenv';

// Load environment variables from .env file
dotenv.config();
// const API_KEY = "a2R0PTBoSjFiQzZLcmN5ckhqZVFORGhkSkNaaUJCZ1kzZVZsaTNJMnlTWXA7YXV0aF90b2tlbj1lMGM5NjQ2NjU2YThhMTg5MWIxNzFlYWVlZDgyZWVjMDgyODA2YzQ1O2N0MD02MzdiODZmNTFmOTI2NzhjYTZiY2Y3MzE0OGNiYWM3ZTAyZDczYWI1ZjY3ZTFhZDhhZTY1ZjgwY2Y1MTkxNzhmYmIzNjk1MWRiY2RiYzY5ZGU2Y2VmNzE5OTg1MTEyNzdiZDczYWRmMjVmMmNkZjUzNjAzYzhiZThkYjBjMmU2ZDYwMDY1MjZlN2JmNzI3YWQ2YjFhNjUzOTc0MWI5MGE1O3R3aWQ9dSUzRDE1NDMzMDg2MzI4MDAyMzk2MjE7"

// Access the API_KEY environment variable
const API_KEY = process.env.API_KEY;
// console.log("Loaded API_KEY:", API_KEY);
const rettiwt = new Rettiwt({ apiKey: API_KEY });

/**
 * 1. Search for Tweets by Filter
 * @param {Object} filter - The filter criteria (e.g., { words: ['Bitcoin'] })
 * @param {number} count - The number of tweets to fetch (up to 20)
 */
async function searchTweets(filter, count = 5) {
    try {
        const result = await rettiwt.tweet.search(filter, count);
        console.log('Search Results:', result);
    } catch (err) {
        console.error('Error in searchTweets:', err);
    }
}

/**
 * 2. Get the Tweet Timeline of a User
 * @param {string} userId - The Twitter user ID
 * @param {number} count - The number of timeline items to fetch (up to 20)
 */
async function getUserTimeline(userId, count = 20) {
    try {
        const result = await rettiwt.user.timeline(userId, count);
        console.log('User Timeline:', result);
    } catch (err) {
        console.error('Error in getUserTimeline:', err);
    }
}

/**
 * 3. Get the Media Timeline of a User
 * @param {string} userId - The Twitter user ID
 * @param {number} count - The number of media items to fetch (up to 100)
 */
async function getUserMediaTimeline(userId, count = 100) {
    try {
        const result = await rettiwt.user.media(userId, count);
        console.log('User Media Timeline:', result);
    } catch (err) {
        console.error('Error in getUserMediaTimeline:', err);
    }
}

/**
 * 4. Stream Filtered Tweets in Pseudo-Real-Time
 * @param {Object} filter - The filter criteria (e.g., { fromUsers: ['user1'] })
 * @param {number} interval - Polling interval in milliseconds (default 60000 ms)
 */
async function streamTweets(filter, interval = 1000) {
    try {
        for await (const tweet of rettiwt.tweet.stream(filter, interval)) {
            console.log('Streamed Tweet:', tweet.fullText);
        }
    } catch (err) {
        console.error('Error in streamTweets:', err);
    }
}

/**
 * 5. Get the Details of a Tweet
 * @param {string} tweetId - The ID of the tweet
 */
async function getTweetDetails(tweetId) {
    try {
        const result = await rettiwt.tweet.details(tweetId);
        console.log('Tweet Details:', result);
    } catch (err) {
        console.error('Error in getTweetDetails:', err);
    }
}

/**
 * 6. Get the Details of a User
 * @param {string} userIdOrUsername - The Twitter user ID or username
 */
async function getUserDetails(userIdOrUsername) {
    try {
        const result = await rettiwt.user.details(userIdOrUsername);
        console.log('User Details:', result);
    } catch (err) {
        console.error('Error in getUserDetails:', err);
    }
}

/**
 * Find a Tweet ID by Search Filter
 * @param {Object} filter - The filter criteria (e.g., { words: ['Bitcoin'] })
 * @returns {string} - The ID of the first tweet found that matches the filter
 */
async function findTweetIdBySearch(filter) {
    try {
        const result = await rettiwt.tweet.search(filter, 1); // Fetch 1 tweet based on filter
        const tweetId = result.list[0]?.id;
        console.log('Found Tweet ID:', tweetId);
        return tweetId;
    } catch (err) {
        console.error('Error in findTweetIdBySearch:', err);
    }
}

// Example Usage
(
    
    async () => {
    // 1. Find a tweet ID by search and get its details
    const tweetId = findTweetIdBySearch({ words: ['#BTC'] });
    if (tweetId) {
        await getTweetDetails(tweetId);
    }

    // 2. Get the tweet timeline of a user
    // await getUserTimeline('1234567890', 10);

    // 3. Get the media timeline of a user
    // await getUserMediaTimeline('1234567890', 10);

    // 4. Stream tweets in pseudo real-time
    // streamTweets({ words: ['#Ethereum'] }, 5000);

    // 5. Get details of a user
    // await getUserDetails('elonmusk');
})();
