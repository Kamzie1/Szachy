let input = document.getElementById("search");
input.addEventListener("input", async function () {
  let response = await fetch("/search?q=" + input.value);
  let shows = await response.json();
  let html = "";
  for (let show of shows) {
    const statsLink = `/stats${show.id}`;
    const chatLink = `/chat${show.chat}`;
    html += '<div class="user-holder">';
    html += `<p class='user-name'>${show.name}</p>`;
    html += `<p class='user-elo'>${show.elo}</p>`;
    html += `<div class="button-container">
                <a class="player-button" href="${statsLink}"></a>
                <a class="player-button" href="${chatLink}"></a>
                <a class="player-button" onClick="invite(${show.chat})"></a>
              </div>`;
    html += "</div>";
  }
  document.getElementById("user-list").innerHTML = html;
});

window.addEventListener("load", async function () {
  let response = await fetch("/search?q=");
  let shows = await response.json();
  let html = "";
  for (let show of shows) {
    const statsLink = `/stats${show.id}`;
    const chatLink = `/chat${show.chat}`;
    html += '<div class="user-holder">';
    html += `<p class='user-name'>${show.name}</p>`;
    html += `<p class='user-elo'>${show.elo}</p>`;
    html += `<div class="button-container">
                <a class="player-button" href="${statsLink}"></a>
                <a class="player-button" href="${chatLink}"></a>
                <a class="player-button" onClick="invite(${show.chat})"></a>
                </div>`;
    html += "</div>";
  }
  document.getElementById("user-list").innerHTML = html;
});

if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}
const socket = io();
const cancel = document.getElementById("cancel");

document.getElementById("find-game").addEventListener("click", function () {
  if (cancel.className == "cancel-button-inactive") {
    socket.emit("find_game");
    cancel.className = "cancel-button-active";
  }
});

socket.on("disconnect");
function disconnect() {
  cancel.className = "cancel-button-inactive";
}

socket.on("start_game", ({ room_id }) => {
  console.log("starting the game!");
  window.location.href = `/game<${room_id}>`;
});

document.getElementById("cancel").addEventListener("click", function () {
  socket.emit("cancel");
  cancel.className = "cancel-button-inactive";
});

function shortRoomId(length = 6) {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  return Array.from(crypto.getRandomValues(new Uint8Array(length)))
    .map((x) => chars[x % chars.length])
    .join("");
}

confetti({
  angle: 70,
  particleCount: 300,
  spread: 360,
  ticks: 100,
  gravity: 0,
  decay: 0.94,
  startVelocity: 30,
  origin: { x: 0.5 },
  origin: { y: 0.4 },
});
