const path = require("path");
const { argv, exit, env, stdin, stdout } = require("process");
const express = require("express");
const app = express();
const { exec } = require('child_process');
const bodyParser = require("body-parser");
const portNumber = 5000;
stdin.setEncoding("utf-8");
app.set("views", path.resolve(__dirname, "templates"));
app.set("view engine", "ejs");
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.get("/", (req, res) => {
    res.render("index");
});

app.post("/processFile", (req, res) => {
const csvFile = req.body.csvFile
const pythonScript = 'test.py'
let outputData = "Update this later"


exec(`python ${pythonScript} ${csvFile}`, (error, stdout, stderr) => {
  console.log("Error")
  console.log(error)
  console.log("Standard output")
  console.log(stdout)
  console.log("Standard error")
  console.log(stderr)
  if (error) {
    console.error(`Error: ${error.message}`);
    res.status(500).send('Error executing script');
    return;
  }
  // stdout = stdout.toString();
  // console.log(std)
  const variables = {
    outputData: stdout
  }
  res.render("process", variables)
});
//console.log(stdout)
  // Process the output and send it as the response
 
  

})


//Server stuff
app.listen(portNumber);
console.log(`Web server started and running at http://localhost:${portNumber}`);
const prompt = "Type stop to shutdown the server: ";
process.stdout.write(prompt);
process.stdin.on("readable", function () {
  let dataInput = process.stdin.read();
  if (dataInput !== null) {
    let command = dataInput.trim();
    if (command === "stop") {
      process.stdout.write("Shutting down the server\n");
      process.exit(0);
    } else {
      process.stdout.write(`Invalid command: ${command}\n`);
    }
    process.stdout.write(prompt);
    process.stdin.resume();
  }
});
