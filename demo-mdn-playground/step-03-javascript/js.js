const buttons = document.querySelectorAll(".filter");
const cards = document.querySelectorAll(".card");
const status = document.querySelector("#status");

buttons.forEach((button) => {
  button.addEventListener("click", () => {
    const selectedRuntime = button.dataset.filter;
    let visibleCount = 0;

    buttons.forEach((item) => {
      const isSelected = item === button;
      item.classList.toggle("is-active", isSelected);
      item.setAttribute("aria-pressed", isSelected);
    });

    cards.forEach((card) => {
      const matches =
        selectedRuntime === "all" || card.dataset.runtime === selectedRuntime;

      card.hidden = !matches;
      if (matches) visibleCount += 1;
    });

    status.textContent = `${visibleCount} tecnologie visibili`;
  });
});

