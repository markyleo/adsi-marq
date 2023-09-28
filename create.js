const prompt = require("prompt-sync")();

function makeAccount(cookies, username) {
  const splitIt = cookies.split("; ");

  let cookie = "";

  let line = "{username}:P@ssw0rd123_d3l!ght:_:_:{cookie}"

  const includeMe = ["auth_token", "guest_id", "ct0", "twid"];

  includeMe.forEach(item => {
    splitIt.forEach(split => {
      if (split.includes(item) && !(split.includes('guest_id_marketing') || split.includes('guest_id_ads'))) {
        cookie += split + '; ';
      }
    })
  })

  let account = line.replace("{username}", username);

  console.log(account.replace("{cookie}", cookie));
}

const cookie = prompt("Enter cookies: ");
const username = prompt("Enter username: ");

makeAccount(cookie, username)