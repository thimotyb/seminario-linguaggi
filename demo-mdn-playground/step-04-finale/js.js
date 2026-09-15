const state = {
  runtime: "all",
  query: "",
  darkTheme: false,
};

const cards = [...document.querySelectorAll(".card")];
const filterButtons = [...document.querySelectorAll(".filter")];
const searchInput = document.querySelector("#search");
const status = document.querySelector("#status");
const themeButton = document.querySelector("#theme");

function render() {
  let visibleCount = 0;

  cards.forEach((card) => {
    const matchesRuntime =
      state.runtime === "all" || card.dataset.runtime === state.runtime;
    const matchesQuery = card.textContent.toLowerCase().includes(state.query);
    const isVisible = matchesRuntime && matchesQuery;

    card.hidden = !isVisible;
    if (isVisible) visibleCount += 1;
  });

  filterButtons.forEach((button) => {
    const isSelected = button.dataset.filter === state.runtime;
    button.classList.toggle("is-active", isSelected);
    button.setAttribute("aria-pressed", isSelected);
  });

  document.documentElement.dataset.theme = state.darkTheme ? "dark" : "light";
  themeButton.textContent = state.darkTheme ? "Tema chiaro" : "Tema scuro";
  themeButton.setAttribute("aria-pressed", state.darkTheme);
  status.textContent = `${visibleCount} tecnologie visibili`;
}

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    state.runtime = button.dataset.filter;
    render();
  });
});

searchInput.addEventListener("input", (event) => {
  state.query = event.target.value.trim().toLowerCase();
  render();
});

themeButton.addEventListener("click", () => {
  state.darkTheme = !state.darkTheme;
  render();
});

document.querySelector("#reset").addEventListener("click", () => {
  state.runtime = "all";
  state.query = "";
  searchInput.value = "";
  render();
  searchInput.focus();
});

render();

