const express = require('express');
const axios = require('axios');
const app = express();
require('dotenv').config();

// Load the Twitter bearer token from the file
const bearerToken = process.env.bearerToken
console.log(bearerToken)
// Endpoint for making the API request
app.get('/', async (req, res) => {
  try {
    // Set the headers with the bearer token
    const headers = {
      Authorization: `Bearer ${bearerToken}`,
      'User-Agent': 'v2FilteredStreamJS',
    };

    // Set the query parameters
    const params = {
      query: 'Хөгжлийн банк',
      max_results: 10,
    };

    // Make the API request
    const response = await axios.get('https://api.twitter.com/2/tweets/search/recent', {
      headers,
      params,
    });

    res.json(response.data);
  } catch (error) {
    console.error(error);
    res.status(error.response.status).send(error.response.statusText);
  }
});

// Start the server
app.listen(3000, () => {
  console.log('Server listening on port 3000');
});
