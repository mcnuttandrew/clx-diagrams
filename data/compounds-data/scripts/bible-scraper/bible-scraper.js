const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;



const getAndParseFile = fileName => {
  console.log(`Parsing ${fileName}`)
  return new Promise((resolve, reject) => {
    // this char set might be wrong?
    fs.readFile(fileName, 'utf8', (error, text) => {
      const dom = new JSDOM(text);
      const bookName = (dom.window.document.querySelector('.textHeader h2') || {textContent: ''}).textContent;
      const chapterContents = (dom.window.document.querySelector('.textBody') || {textContent: ''}).textContent
      resolve([bookName, chapterContents].join('\n'));
    });
  });
}


const parseLanguage = languague => {
  fs.readdir(`../${languague}/`, (err, files) => {
    // construct an array of promises that grab all of the subdirectory names
    const listsOfFiles = files
      .filter(file => !isNaN(Number(file)))
      .sort((a, b) => Number(a) < Number(b) ? -1 : 1)
      .map(file => {
        return new Promise((resolve, reject) => {
          fs.readdir(`../${languague}/${file}/`, (err, subFiles) => {
            const organizedNames = subFiles
              .sort((a, b) => {
                return Number(a.split('.')[0]) < Number(b.split('.')[0]) ? -1 : 1
              })
              .map(fileName => `../${languague}/${file}/${fileName}`)
            resolve(organizedNames)
          });
        });
      })

    Promise.all(listsOfFiles)
      .then(results => results.reduce((acc, row) => acc.concat(row), []))
      .then(allFiles => Promise.all(allFiles.map(getAndParseFile)))
      .then(allContent => {
        // console.log(allContent.join('\n'))/
        fs.writeFile(`./${languague}-bible.txt`, allContent.join('\n'), (e, t) => console.log('written'));
      })
  })
}


parseLanguage('chinese');
// parseLanguage('thai');