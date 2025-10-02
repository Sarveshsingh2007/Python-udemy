// game.js - Tic Tac Toe client logic (human vs human, human vs computer)

const boardEl = document.getElementById('board');
const statusEl = document.getElementById('status');
const difficultyEl = document.getElementById('difficulty');
const restartBtn = document.getElementById('restart');
const symbolEl = document.getElementById('symbol');
const modeEl = document.getElementById('mode');
const diffLabel = document.getElementById('diff-label');

const WIN_LINES = [
  [0,1,2],[3,4,5],[6,7,8],
  [0,3,6],[1,4,7],[2,5,8],
  [0,4,8],[2,4,6]
];

let board = Array(9).fill('');
let human = 'X';         // when vs computer, this is player's symbol
let computer = 'O';
let currentPlayer = 'X'; // used for human vs human
let gameOver = false;

// Render board cells
function renderBoard() {
  boardEl.innerHTML = '';
  board.forEach((val, i) => {
    const cell = document.createElement('div');
    cell.className = 'cell' + (val ? ' disabled ' + val.toLowerCase() : '');
    cell.dataset.index = i;
    cell.textContent = val;
    cell.addEventListener('click', onCellClick);
    boardEl.appendChild(cell);
  });
}

// Determine winner and winning line (client-side)
function checkWinnerWithLine(b) {
  for (const line of WIN_LINES) {
    const [a,b1,c] = line;
    if (b[a] && b[a] === b[b1] && b[a] === b[c]) {
      return { winner: b[a], line };
    }
  }
  return { winner: null, line: null };
}

// On cell click behavior (handles both modes)
function onCellClick(e) {
  if (gameOver) return;
  const idx = parseInt(e.currentTarget.dataset.index);
  if (board[idx] !== '') return;

  if (modeEl.value === 'human') {
    // Human vs Human: alternate currentPlayer
    board[idx] = currentPlayer;
    renderBoard();
    const res = checkWinnerWithLine(board);
    if (res.winner) {
      endGameWithWinner(res.winner, res.line);
      return;
    }
    if (board.every(c => c !== '')) {
      endGameDraw();
      return;
    }
    currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
    statusEl.textContent = `${currentPlayer}'s turn`;
  } else {
    // Human vs Computer
    board[idx] = human;
    renderBoard();

    // check immediate local result (player may have won)
    let res = checkWinnerWithLine(board);
    if (res.winner) {
      endGameWithWinner(res.winner, res.line);
      return;
    }
    if (board.every(c => c !== '')) {
      endGameDraw();
      return;
    }

    // send board to server for computer move
    sendBoardToServer();
  }
}

// Highlight winning cells and finish
function endGameWithWinner(winner, line) {
  gameOver = true;
  // add 'win' class to winning cells
  line.forEach(i => {
    const cell = boardEl.querySelector(`.cell[data-index='${i}']`);
    if (cell) cell.classList.add('win', winner.toLowerCase());
  });
  // set status text with color cues
  if (modeEl.value === 'human') {
    statusEl.textContent = (winner === 'X' ? "Player X wins! 🎉" : "Player O wins! 🎉");
  } else {
    statusEl.textContent = (winner === human) ? "You win! 🎉" : "Computer wins 🤖";
  }
}

// Draw
function endGameDraw() {
  gameOver = true;
  statusEl.textContent = "It's a draw 🤝";
}

// Update board UI from server response and handle result
function applyServerBoard(newBoard) {
  board = newBoard.slice();
  renderBoard();
  const res = checkWinnerWithLine(board);
  if (res.winner) {
    endGameWithWinner(res.winner, res.line);
    return true;
  }
  if (board.every(c => c !== '')) {
    endGameDraw();
    return true;
  }
  return false;
}

// Send board to backend for computer move
async function sendBoardToServer() {
  statusEl.textContent = 'Computer is thinking...';
  try {
    const resp = await fetch('/computer_move', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        board,
        difficulty: difficultyEl.value,
        computer // the symbol the computer plays
      })
    });
    const data = await resp.json();
    if (data.move === null) {
      // no moves left
      if (!applyServerBoard(data.board)) {
        statusEl.textContent = "No moves left";
      }
      return;
    }
    // update from returned board
    const finished = applyServerBoard(data.board);
    if (!finished) {
      statusEl.textContent = 'Your turn';
    }
  } catch (err) {
    console.error('Error:', err);
    statusEl.textContent = 'Error contacting server';
  }
}

// Restart/reset game
function restart() {
  board = Array(9).fill('');
  human = symbolEl.value;
  computer = (human === 'X') ? 'O' : 'X';
  currentPlayer = 'X';
  gameOver = false;
  // Show/hide difficulty label depending on mode
  diffLabel.style.display = (modeEl.value === 'computer') ? 'inline-block' : 'none';
  statusEl.textContent = (modeEl.value === 'human') ? `${currentPlayer}'s turn` : 'Your turn';
  renderBoard();
}

// Event listeners
restartBtn.addEventListener('click', restart);
symbolEl.addEventListener('change', restart);
modeEl.addEventListener('change', () => {
  // hide difficulty for human mode
  diffLabel.style.display = (modeEl.value === 'computer') ? 'inline-block' : 'none';
  restart();
});
difficultyEl.addEventListener('change', () => {
  statusEl.textContent = `Difficulty: ${difficultyEl.value}`;
});

// initialize
restart();
