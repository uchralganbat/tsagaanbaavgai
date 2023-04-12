const https = require('https');

const options = {
  hostname: 'api.twitter.com',
  port: 443,
  path: '/2/users/by/username?username=KhNyambaatar&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,url,username,verified,withheld&expansions=pinned_tweet_id',
  method: 'GET',
  headers: {
    Authorization: 'Bearer AAAAAAAAAAAAAAAAAAAAAPQQlgEAAAAAxzgXweyLKXtT%2FBWuLY1v53yzk4U%3DKGMwJAIJXuJe53JE6G8YdGXA16RWKSht1TVMx8m8NYFIExuGHj'
  }
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  res.on('end', () => {
    console.log(data);
  });
});

req.on('error', (error) => {
  console.error(error);
});

console.log(req)

req.end();
