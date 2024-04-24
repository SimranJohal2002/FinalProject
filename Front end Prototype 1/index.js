const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const fs = require('fs');

const app = express();
const port = 8000;

app.use(express.static('public'));

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Serve HTML page
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

// Handle form submission
app.post('/recommend', (req, res) => {
    const { title } = req.body,
        FILE_NAME = 'Prototype 2.ipynb',
        PY_SCRIPT_NAME = './temp/index.py';


    // Convert the .ipynb file to .py file
    exec(`python converter.py "${FILE_NAME}"`, (err, stdout, stderr) => {

        if (err) return res.status(500).send('Something went wrong!');


        // Now execute the Python code
        exec(`python ${PY_SCRIPT_NAME} "${title}"`, (err, stdout, stderr) => {
            fs.rm('./temp', { recursive: true }, (err) => { }); // remove temp folder


            if (err) return res.status(500).send({ error: stderr });


            res.status(200).send({
                result: convertToJson(stdout)
            });
        });
    });
});





// Handle form submission
app.post('/recommend1', (req, res) => {
    const { title } = req.body,
        FILE_NAME = 'Prototype 1.ipynb',
        PY_SCRIPT_NAME = './temp/index.py';


    // Convert the .ipynb file to .py file
    exec(`python converter.py "${FILE_NAME}"`, (err, stdout, stderr) => {

        if (err) return res.status(500).send('Something went wrong!');


        // Now execute the Python code
        exec(`python ${PY_SCRIPT_NAME} "${title}"`, (err, stdout, stderr) => {
            //fs.rm('./temp', { recursive: true }, (err) => { }); // remove temp folder


            if (err) return res.status(500).send({ error: stderr });


            res.status(200).send({
                result: convertToJson1(stdout)
            });
        });
    });
});


// Handle form submission
app.post('/recommend2', (req, res) => {
    const { title } = req.body,
        FILE_NAME = 'Book Prototype - Collaborative Filtering.ipynb',
        PY_SCRIPT_NAME = './temp/index.py';


    // Convert the .ipynb file to .py file
    exec(`python converter.py "${FILE_NAME}"`, (err, stdout, stderr) => {

        if (err) return res.status(500).send('Something went wrong!');


        // Now execute the Python code
        exec(`python ${PY_SCRIPT_NAME} "${title}"`, (err, stdout, stderr) => {
            //fs.rm('./temp', { recursive: true }, (err) => { }); // remove temp folder


            if (err) return res.status(500).send({ error: stderr });


            res.status(200).send({
                result: convertToJson2(stdout)
            });
        });
    });
 });




function convertToJson(str) {

    str = str.split('\n')
    str = str.filter((item) => item.length > 0)

    let data = [];
    for (let i = 1; i < str.length; i++) {
        let item = str[i];
        item = item.split('  ').filter((item) => item.length > 0 && item.trim() !== 'genres' && item.trim() !== 'title')
        if (!item.length) continue;
        let [id, title, genres] = item;

        if (!title) continue;

        data.push({ id, title, genres })
    }

    return { data }
}

// app.listen(port, () => {
//     console.log(`Server is running on port ${port}`);
// });


// function convertToJson1(strArray) {
//     let data = [];

//     for (let i = 0; i < strArray.length; i++) {
//         let title = strArray[i];

//         if (!title) continue; // Skip empty titles

//         // Assume genres are not provided in this format, so set it as an empty string
//         let genres = '';

//         // Create a unique ID for each entry, e.g., incrementing index
//         let id = i + 1;

//         data.push({ id, title, genres });
//     }

//     return { data };
// }

function convertToJson1(str) {
    // Remove square brackets and single or double quotes from the input string
    str = str.replace(/\[|\]|"|'/g, '');

    // Split the modified input string into an array of song names
    const songs = str.split(',');

    let data = [];
    // Iterate over each song name
    songs.forEach((song, index) => {
        // Create an object for each song with an id and the song title
        data.push({ id: index + 1, title: song.trim(), genres: "" });
    });

    return { data };
}


function convertToJson2(str) {

    str = str.split('\n')
    str = str.filter((item) => item.length > 0)

    let data = [];
    for (let i = 1; i < str.length; i++) {
        let item = str[i];
        item = item.split('  ').filter((item) => item.length > 0 && item.trim() !== 'genres' && item.trim() !== 'title')
        if (!item.length) continue;
        let [id, title, genres] = item;

        if (!title) continue;

        data.push({ id, title, genres })
    }

    return { data }
}

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});

