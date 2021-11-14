// https://www.npmjs.com/package/newman#api-reference

const newman = require('newman');

newman.run({
    // URL to smoke test collection
    collection: "https://api.getpostman.com/collections/18014860-42e12872-4a89-4ae3-ab2a-4b929a56038b?apikey=PMAK-618a1ad33905f200528b1615-09736c7b9267c537d82c280ecd5b9d064d",
    // URL to smoke test environment variables
    environment: "https://api.getpostman.com/environments/10470697-17589157-9fd3-4efa-a564-d3b11ae30429?apikey=PMAK-618a1ad33905f200528b1615-09736c7b9267c537d82c280ecd5b9d064d",
    reporters: ['cli']

}, (error, summary) => {
    if (error || summary.error) {
        // smoke tests fail
        console.error(error);
        console.error(summary.error);
    } else {
        // smoke tests pass
        console.log("Completed API smoke tests.");
    }
});