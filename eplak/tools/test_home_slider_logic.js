// Simulate 4 slides in track: [B_clone, A, B, A_clone]
let current = 1; // start at A
const total = 4;

function swipeLeft() {
  current++;
  console.log("Swiped Left -> current index:", current);
  checkEnd();
}

function swipeRight() {
  current--;
  console.log("Swiped Right -> current index:", current);
  checkEnd();
}

function checkEnd() {
  if (current === 3) {
    current = 1;
    console.log("   (transitionend: silent snap to index 1)");
  } else if (current === 0) {
    current = 2;
    console.log("   (transitionend: silent snap to index 2)");
  }
}

console.log("Starting at A (index 1)");
swipeLeft(); // should be B (index 2)
swipeLeft(); // should be A_clone (index 3) -> snaps to 1 (A)
swipeLeft(); // should be B (index 2)
swipeRight(); // should be A (index 1)
swipeRight(); // should be B_clone (index 0) -> snaps to 2 (B)
swipeRight(); // should be A (index 1)
console.log("All transitions looped seamlessly!");
