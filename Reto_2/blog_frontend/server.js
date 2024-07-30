const express = require('express');
const axios = require('axios');
const app = express();
const port = 3000;

app.set('view engine', 'ejs');
app.use(express.static('public'));

app.get('/', async (req, res) => {
  try {
    const response = await axios.get('http://posts.internal-deepsec.com/posts');
    const posts = response.data;
    res.render('index', { posts });
  } catch (error) {
    res.send('Error fetching posts');
  }
});

app.get('/post', async (req, res) => {
  const { url } = req.query;
  if (!url) {
    return res.status(400).send('URL parameter is required');
  }
  try {
    const response = await axios.get(url);
    const post = response.data;
    res.render('post', { post });
  } catch (error) {
    res.status(500).send('Error fetching the post');
  }
});

app.get('/proxy', async (req, res) => {
  const { url } = req.query;
  if (!url) {
    return res.status(400).send('URL parameter is required');
  }
  try {
    const response = await axios.get(url);
    res.send(response.data);
  } catch (error) {
    res.status(500).send('Error fetching the URL');
  }
});

app.listen(port, () => {
  console.log(`Run Laboratory :D`);
});



